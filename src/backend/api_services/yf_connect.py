import yfinance as yf
import random
import pandas as pd
import time
from sqlalchemy.exc import IntegrityError
from backend.database.db_functions import create_yf_pricing_entry, create_yf_price_history_entry, create_yf_company_from_info
from backend.data_model import TICKERS

stock_list = TICKERS
all_data = {}

def download_yf_pricing_raw(tickers_to_download :list, startdate : str, enddate : str, interval : str):
    for t in tickers_to_download:
        print(f"Lade Daten für {t} ...")

        df = yf.download(
            t, 
            start="2024-01-01",
            end="2025-01-01",
            interval="1d",
            auto_adjust=False,
            group_by="column",
        )

        all_data[t] = df

        if not df.empty:
            # MultiIndex-Spalten abflachen
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df = df.reset_index()

            df = df.rename(columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume",
            })

            print("Spalten nach Umbenennen:", df.columns)

            for _, row in df.iterrows():
                create_yf_pricing_entry(
                    symbol=t,
                    date=row["date"],
                    open=row["open"] if pd.notna(row["open"]) else None,
                    high=row["high"] if pd.notna(row["high"]) else None,
                    low=row["low"] if pd.notna(row["low"]) else None,
                    close=row["close"] if pd.notna(row["close"]) else None,
                    volume=row["volume"] if pd.notna(row["volume"]) else None,
                )

        time.sleep(30)

    print("\nFertig! Daten geladen und in DB gespeichert.\n")

def download_price_history(
    tickers_to_download: list,
    start: str = "1995-01-01",
    end: str = "2025-01-01",
    batch_size: int = 25,
    sleep_between_batches: int = 30,
):
    """
    Lädt historische Yahoo-Finance-Daten für viele Ticker in Batches
    und speichert sie über create_yf_pricing_entry() in die Datenbank.

    - tickers_to_download: Liste von Ticker-Symbolen (z.B. ["AAPL", "MSFT", ...])
    - start / end: Datumsbereich als "YYYY-MM-DD"
    - batch_size: Anzahl Ticker pro Request (z.B. 20–50)
    - sleep_between_batches: Pause in Sekunden nach jedem Batch
    """

    total = len(tickers_to_download)
    print(f"Starte Download für {total} Ticker, "
          f"Zeitraum {start} bis {end}, Batchgröße = {batch_size}")

    for i in range(0, total, batch_size):
        batch = tickers_to_download[i:i + batch_size]
        batch_num = i // batch_size + 1
        print(f"\n🔹 Batch {batch_num}: lade {len(batch)} Ticker: {batch}")

        try:
            df = yf.download(
                batch,
                start=start,
                end=end,
                interval="1d",
                auto_adjust=False,      # Rohdaten
                group_by="column",
                progress=False,
            )
        except Exception as e:
            print(f"⚠️ Fehler beim Download von Batch {batch_num}: {e}")
            time.sleep(sleep_between_batches)
            continue

        if df.empty:
            print(f"⚠️ Batch {batch_num}: leerer DataFrame, überspringe.")
            time.sleep(sleep_between_batches)
            continue

        # --- DataFrame in "long" Format mit symbol + date bringen ---

        if isinstance(df.columns, pd.MultiIndex):
            # yfinance MultiIndex: Ebene0 = Price (Open, High,...), Ebene1 = Ticker
            df_long = df.stack(level=1).reset_index()

            # Je nach Version heißt die Ticker-Spalte "Ticker" oder "level_1"
            rename_map = {
                "Date": "date",
                "Ticker": "symbol",
                "level_1": "symbol",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
            df_long = df_long.rename(columns=rename_map)

        else:
            # Fallback: falls doch kein MultiIndex zurückkommt (z.B. 1 Ticker)
            df_long = df.reset_index().rename(columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            })
            # ein Ticker = gleiche Symbol-Spalte für alle Zeilen
            df_long["symbol"] = batch[0]

        # nur die Spalten, die wir wirklich brauchen
        wanted_cols = ["symbol", "date", "open", "high", "low", "close", "volume"]
        df_long = df_long[wanted_cols]

        # Datum in YYYY-MM-DD bringen
        df_long["date"] = pd.to_datetime(df_long["date"]).dt.date

        print(f"Batch {batch_num}: {len(df_long)} Zeilen nach Umwandlung.")

        # --- In DB schreiben: jede Zeile über deine Funktion ---

        for _, row in df_long.iterrows():
            create_yf_price_history_entry(
                symbol=row["symbol"],
                date=row["date"],
                open=row["open"] if pd.notna(row["open"]) else None,
                high=row["high"] if pd.notna(row["high"]) else None,
                low=row["low"] if pd.notna(row["low"]) else None,
                close=row["close"] if pd.notna(row["close"]) else None,
                volume=row["volume"] if pd.notna(row["volume"]) else None,
            )

        print(f"✔ Batch {batch_num} in DB gespeichert.")
        time.sleep(sleep_between_batches)

    print("\n🎉 Fertig! Alle Batches geladen und in DB gespeichert.\n")

def download_yf_company_info(
    tickers: list,
    base_sleep: float = 5.0,      # Grundwartezeit (vorsichtig)
    jitter: float = 2.0,          # Zusatz durch zufällige Variation
    max_retries: int = 2          # Anzahl Wiederholungsversuche
):
    """
    Lädt vorsichtig die Unternehmensinformationen (ticker.info)
    für alle Ticker in der Liste und speichert sie in der DB.

    Speichert über: create_yf_company_from_info(info)
    """

    for t in tickers:
        print(f"\n=== Verarbeite Unternehmensdaten für: {t} ===")

        success = False

        for attempt in range(1, max_retries + 1):
            try:
                ticker = yf.Ticker(t)
                info = ticker.info or {}

                # Falls Yahoo kein symbol returnt → eigenes
                if "symbol" not in info or not info["symbol"]:
                    info["symbol"] = t

                # In Datenbank speichern
                create_yf_company_from_info(info)

                print(f"✔ Unternehmensinfo gespeichert: {t}")
                success = True
                break  # raus aus Retry-Loop

            except IntegrityError as e:
                print(f"⚠️ DB-Fehler für {t}: {e}")
                break  # kein Retry (würde immer wieder fehlschlagen)

            except Exception as e:
                print(f"⚠️ Fehler bei {t} (Versuch {attempt}/{max_retries}): {e}")

                # wenn wir den letzten Versuch erreicht haben → abbrechen
                if attempt == max_retries:
                    print(f"❌ Maximalversuche erreicht — {t} wird übersprungen.")
                    break

                # Ansonsten erneuter Versuch mit Wartezeit
                sleep_time = base_sleep + random.uniform(0, jitter)
                print(f"🔁 Warte {sleep_time:.2f}s und versuche erneut ...")
                time.sleep(sleep_time)

        # Wartezeit vor dem nächsten Ticker (Vorsicht!)
        if success:
            sleep_time = base_sleep + random.uniform(0, jitter)
            print(f"⏳ Warte {sleep_time:.2f}s vor nächstem Ticker ...")
            time.sleep(sleep_time)

    print("\n✅ Fertig! Alle Unternehmensinformationen verarbeitet.\n")

download_yf_company_info(tickers=stock_list)