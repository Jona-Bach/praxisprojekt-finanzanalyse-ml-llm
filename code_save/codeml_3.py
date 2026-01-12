import os
from datetime import datetime
import streamlit as st
from backend.data_processing.alphavantage_processed import get_processed_table
import numpy as np
import pandas as pd
from backend.database.users_database import get_user_table, list_user_tables
from backend.database.db_functions import get_all_yf_price_history, get_yf_pricing_raw, get_config_dict
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    ConfusionMatrixDisplay,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import joblib

# __________________________ Konfiguration __________________________

MODEL_DIR = "saved_models"
os.makedirs(MODEL_DIR, exist_ok=True)

ALPHAVANTAGE_TABLES = [
    "alphavantage_pricing_processed",
    "alphavantage_processed_kpi",
]

ALPHA_PRICING_TABLE = "alphavantage_pricing_processed"
ALPHA_KPI_TABLE = "alphavantage_processed_kpi"

# Trainings-Grenzen

max_rows_config = get_config_dict("ml_max_rows_for_model")
if max_rows_config is not None:
    MAX_ROWS_FOR_MODEL = int(max_rows_config["Value"])
else:
    MAX_ROWS_FOR_MODEL = 20000

min_rows_config = get_config_dict("ml_min_rows_for_model")
if min_rows_config is not None:
    MIN_ROWS_FOR_MODEL = int(min_rows_config["Value"])
else:
    MIN_ROWS_FOR_MODEL = 50  # Minimum an Zeilen für sinnvolles Training

# __________________________Header____________________________

st.set_page_config(
    page_title="ML Studio",
    page_icon="🧠",
    layout="wide"
)


# ---------------------- Helper-Funktionen ----------------------

def _try_parse_numeric_series(s: pd.Series) -> pd.Series | None:
    """
    Versucht, eine String-Serie robust in floats umzuwandeln.
    Unterstützt z.B.:
      - "1.234,56"  -> 1234.56
      - "12,3%"     -> 12.3
      - "  100 "    -> 100.0
    Gibt eine Serie zurück, wenn >=50% der Werte plausibel numerisch sind, sonst None.
    """
    s = s.astype(str).str.strip()
    # Leere oder Platzhalter als NaN
    s = s.replace({"": np.nan, "-": np.nan, "NA": np.nan, "NaN": np.nan})

    # Wenn kaum Ziffern vorkommen, ist die Spalte wahrscheinlich kategorial
    frac_digit = s.str.contains(r"\d", regex=True).mean()
    if frac_digit < 0.5:
        return None

    # Prozent / Währungszeichen / Leerzeichen entfernen
    s_clean = (
        s.str.replace("%", "", regex=False)
         .str.replace("€", "", regex=False)
         .str.replace("$", "", regex=False)
         .str.replace(" ", "", regex=False)
    )

    # Variante 1: Standard-Konvertierung (Punkt als Dezimaltrenner)
    cand1 = pd.to_numeric(s_clean, errors="coerce")

    # Variante 2: Deutsche Schreibweise: 1.234,56 -> 1234.56
    s_de = s_clean.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    cand2 = pd.to_numeric(s_de, errors="coerce")

    ratio1 = cand1.notna().mean()
    ratio2 = cand2.notna().mean()

    best_ratio = max(ratio1, ratio2)
    if best_ratio < 0.5:
        return None

    return cand1 if ratio1 >= ratio2 else cand2


def auto_convert_numeric_and_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Läuft einmal über alle Spalten und:
    - konvertiert String-Spalten, die nach Zahlen aussehen, in float
    - konvertiert typische Datums-/Zeitspalten in datetime
    """
    df = df.copy()

    for col in df.columns:
        col_series = df[col]

        # Numerisch oder bereits datetime → nichts tun
        if pd.api.types.is_numeric_dtype(col_series) or np.issubdtype(col_series.dtype, np.datetime64):
            continue

        col_lower = col.lower()

        # Potenzielle Zeit-/Datums-Spalten erkennen
        if any(k in col_lower for k in ["date", "time", "timestamp"]):
            dt = pd.to_datetime(col_series, errors="coerce")
            if dt.notna().mean() > 0.5:
                df[col] = dt
                continue  # schon als Datum erkannt

        # Versuch: String-Spalte in Float umwandeln
        parsed = _try_parse_numeric_series(col_series)
        if parsed is not None:
            df[col] = parsed

    return df


@st.cache_data
def load_data_from_source(
    source: str,
    symbol: str = None,
    table_name: str = None,
):
    """
    Lädt Daten je nach ausgewählter Quelle mit deinen bestehenden Funktionen
    und konvertiert anschließend String-Spalten bestmöglich in numerische / Datums-Typen.
    """
    if source == "Entire Yahoo Finance Pricing Table":
        df = get_all_yf_price_history()

    elif source == "Yahoo Finance Pricing Single Stock":
        if not symbol:
            return pd.DataFrame()
        df = get_yf_pricing_raw(symbol)

    elif source == "Alphavantage":
        if not table_name:
            return pd.DataFrame()
        df = get_processed_table(table_name)

    elif source == "Alphavantage (Combined)":
        df_price = get_processed_table(ALPHA_PRICING_TABLE)
        df_kpi = get_processed_table(ALPHA_KPI_TABLE)

        if "symbol" not in df_price.columns or "symbol" not in df_kpi.columns:
            return pd.DataFrame()

        if "timestamp" in df_price.columns:
            df_price["timestamp"] = pd.to_datetime(df_price["timestamp"])
        else:
            return pd.DataFrame()

        if "timestamp" in df_kpi.columns:
            df_kpi["timestamp"] = pd.to_datetime(df_kpi["timestamp"])
        else:
            return pd.DataFrame()

        join_cols = ["symbol", "timestamp"]

        df = pd.merge(
            df_price,
            df_kpi,
            on=join_cols,
            how="inner",
            suffixes=("_price", "_kpi"),
        )

    elif source == "User Tables":
        if not table_name:
            return pd.DataFrame()
        df = get_user_table(table_name)

    else:
        df = pd.DataFrame()

    # automatische Konvertierung von String → float / datetime
    if df is not None and not df.empty:
        df = auto_convert_numeric_and_datetime(df)

    return df


def detect_time_column(df: pd.DataFrame):
    """
    Versucht automatisch die Zeitspalte zu identifizieren.
    Priorität:
    1. Spalte mit Namen 'date'
    2. Spalten mit datetime64 dtype
    3. Spaltennamen, die 'date', 'time', 'timestamp' oder 'jahr' enthalten
    """
    cols = df.columns.tolist()

    # 1. explizit "date"
    if "date" in cols:
        return "date"

    # 2. echte Datetime-Spalten
    datetime_cols = [c for c in cols if np.issubdtype(df[c].dtype, np.datetime64)]
    if datetime_cols:
        return datetime_cols[0]

    # 3. heuristisch nach Namen
    keywords = ["date", "time", "timestamp", "jahr"]
    for c in cols:
        if any(k in c.lower() for k in keywords):
            # Versuch, diese Spalte in datetime zu casten
            try:
                converted = pd.to_datetime(df[c], errors="coerce")
                if converted.notna().mean() > 0.5:
                    df[c] = converted
                    return c
            except Exception:
                continue

    return None


def make_future_target(df: pd.DataFrame, time_col: str, target_col: str, horizon_label: str):
    """
    Erzeugt ein zukünftiges Target auf Basis einer Zeitspalte.
    y_future(t) = y(t + delta) wird auf die Zeile mit Zeitpunkt t gemappt.
    """
    df = df.copy()
    if not np.issubdtype(df[time_col].dtype, np.datetime64):
        df[time_col] = pd.to_datetime(df[time_col])

    df = df.sort_values(time_col)

    if horizon_label == "1 Tag":
        delta = pd.DateOffset(days=1)
        suffix = "1d"
    elif horizon_label == "3 Wochen":
        delta = pd.DateOffset(weeks=3)
        suffix = "3w"
    elif horizon_label == "3 Monate":
        delta = pd.DateOffset(months=3)
        suffix = "3m"
    elif horizon_label == "1 Jahr":
        delta = pd.DateOffset(years=1)
        suffix = "1y"
    else:
        # Kein Shift → nichts verändern
        return df, target_col

    future_col = f"{target_col}_future_{suffix}"

    tmp = df[[time_col, target_col]].copy()
    tmp[time_col] = tmp[time_col] - delta
    tmp = tmp.rename(columns={target_col: future_col})

    merged = df.merge(tmp, on=time_col, how="left")
    merged = merged.dropna(subset=[future_col])

    return merged, future_col


def make_lag_features(df: pd.DataFrame, time_col: str, base_col: str, n_lags: int):
    """
    Erzeugt Lag-Features aus einer Basis-Spalte.
    Beispiel: base_col = 'close', n_lags = 3
    → close_lag_1, close_lag_2, close_lag_3
    """
    df = df.copy()

    if time_col not in df.columns:
        raise ValueError(f"Zeitspalte '{time_col}' nicht im DataFrame gefunden.")

    if base_col not in df.columns:
        raise ValueError(f"Basis-Spalte '{base_col}' nicht im DataFrame gefunden.")

    if not np.issubdtype(df[time_col].dtype, np.datetime64):
        df[time_col] = pd.to_datetime(df[time_col])

    df = df.sort_values(time_col)

    df[base_col] = pd.to_numeric(df[base_col], errors="coerce")

    lag_cols = []
    for lag in range(1, n_lags + 1):
        col_name = f"{base_col}_lag_{lag}"
        df[col_name] = df[base_col].shift(lag)
        lag_cols.append(col_name)

    return df, lag_cols


def preprocess_features_target_regression(df: pd.DataFrame, feature_cols, target_col, scale: bool):
    """
    Preprocessing für Regression:
    - Target -> float
    - numerische Feature-Spalten (auch String -> float)
    - One-Hot-Encoding für echte Kategoricals
    - optionales Scaling
    """
    df = df.copy()

    if target_col not in df.columns:
        raise ValueError(f"Target-Spalte '{target_col}' nicht im DataFrame gefunden.")

    df[target_col] = pd.to_numeric(df[target_col], errors="coerce")

    missing_features = [c for c in feature_cols if c not in df.columns]
    if missing_features:
        raise ValueError(f"Folgende Feature-Spalten fehlen im DataFrame: {missing_features}")

    X_raw = df[feature_cols].copy()

    numeric_feature_cols = []
    categorical_feature_cols = []

    for col in X_raw.columns:
        s = X_raw[col]
        if pd.api.types.is_numeric_dtype(s):
            numeric_feature_cols.append(col)
        else:
            # Versuch, nachträglich zu konvertieren (falls noch Strings übrig sind)
            converted = _try_parse_numeric_series(s)
            if converted is not None:
                X_raw[col] = converted
                numeric_feature_cols.append(col)
            else:
                categorical_feature_cols.append(col)

    X_num = X_raw[numeric_feature_cols] if numeric_feature_cols else pd.DataFrame(index=df.index)
    X_cat = X_raw[categorical_feature_cols] if categorical_feature_cols else pd.DataFrame(index=df.index)

    if not X_cat.empty:
        X_cat_dummies = pd.get_dummies(X_cat, drop_first=True)
    else:
        X_cat_dummies = X_cat

    X_full = pd.concat([X_num, X_cat_dummies], axis=1)

    data = pd.concat([X_full, df[target_col]], axis=1)
    data = data.dropna()
    if data.empty:
        raise ValueError("Nach dem Bereinigen (NaNs entfernen) sind keine Datenzeilen mehr übrig.")

    y_clean = data[target_col]
    X_clean = data.drop(columns=[target_col])

    scaler = None
    if scale and not X_clean.empty:
        scaler = StandardScaler()
        X_used = scaler.fit_transform(X_clean)
    else:
        X_used = X_clean.values

    return X_used, y_clean, X_clean, scaler


def preprocess_features_target_classification(df: pd.DataFrame, feature_cols, target_col, scale: bool):
    """
    Preprocessing für Klassifikation (Logistische Regression):
    - Target als Klassen (LabelEncoder)
    - Features analog wie bei Regression (numerisch/kategorial)
    """
    df = df.copy()

    if target_col not in df.columns:
        raise ValueError(f"Target-Spalte '{target_col}' nicht im DataFrame gefunden.")

    missing_features = [c for c in feature_cols if c not in df.columns]
    if missing_features:
        raise ValueError(f"Folgende Feature-Spalten fehlen im DataFrame: {missing_features}")

    X_raw = df[feature_cols].copy()

    numeric_feature_cols = []
    categorical_feature_cols = []

    for col in X_raw.columns:
        s = X_raw[col]
        if pd.api.types.is_numeric_dtype(s):
            numeric_feature_cols.append(col)
        else:
            converted = _try_parse_numeric_series(s)
            if converted is not None:
                X_raw[col] = converted
                numeric_feature_cols.append(col)
            else:
                categorical_feature_cols.append(col)

    X_num = X_raw[numeric_feature_cols] if numeric_feature_cols else pd.DataFrame(index=df.index)
    X_cat = X_raw[categorical_feature_cols] if categorical_feature_cols else pd.DataFrame(index=df.index)

    if not X_cat.empty:
        X_cat_dummies = pd.get_dummies(X_cat, drop_first=True)
    else:
        X_cat_dummies = X_cat

    X_full = pd.concat([X_num, X_cat_dummies], axis=1)

    y_raw = df[target_col].astype(str)
    data = pd.concat([X_full, y_raw.rename(target_col)], axis=1)
    data = data.dropna()
    if data.empty:
        raise ValueError("Nach dem Bereinigen (NaNs entfernen) sind keine Datenzeilen mehr übrig.")

    y_labels = data[target_col].astype(str)
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_labels)

    X_clean = data.drop(columns=[target_col])

    scaler = None
    if scale and not X_clean.empty:
        scaler = StandardScaler()
        X_used = scaler.fit_transform(X_clean)
    else:
        X_used = X_clean.values

    return X_used, y_encoded, X_clean, scaler, label_encoder


def save_model_bundle(
    model,
    algo_name: str,
    data_source: str,
    feature_cols,
    target_col: str,
    scaler,
    horizon_label: str,
    label_encoder=None,
    time_series_mode: bool = False,
    n_lags: int | None = None,
    base_col: str | None = None,
    encoded_feature_names: list[str] | None = None,
    feature_dtypes: dict | None = None,
):
    """
    Speichert Modell + Metadaten als .pkl in MODEL_DIR.
    encoded_feature_names: Spaltennamen nach One-Hot-Encoding / Dummys etc.
    """
    ts_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_algo = algo_name.replace(" ", "")
    safe_target = target_col.replace(" ", "_").replace("/", "_")

    filename = f"{safe_algo}__{safe_target}__{ts_str}.pkl"
    filepath = os.path.join(MODEL_DIR, filename)

    bundle = {
        "model": model,
        "algo": algo_name,
        "data_source": data_source,
        "feature_cols": list(feature_cols),
        "target_col": target_col,
        "scaler": scaler,
        "horizon": horizon_label,
        "label_encoder": label_encoder,
        "time_series_mode": time_series_mode,
        "n_lags": n_lags,
        "lag_base_col": base_col,
        "encoded_feature_names": encoded_feature_names,
        "feature_dtypes": feature_dtypes,
        "saved_at": ts_str,
    }

    joblib.dump(bundle, filepath)
    return filepath


def build_X_for_prediction(
    df: pd.DataFrame,
    feature_cols,
    encoded_feature_names: list[str] | None = None,
    time_series_mode: bool = False,
    lag_base_col: str | None = None,
    n_lags: int | None = None,
    time_col: str | None = None,
):
    """
    Baut ein Feature-DataFrame X für Vorhersagen auf Basis des gespeicherten Bundles.
    - nutzt bei Zeitreihenmodus make_lag_features
    - rekonstruiert numerische / kategoriale Spalten
    - richtet sich nach encoded_feature_names (Spalten nach Training)
    """
    df_proc = df.copy()

    # Zeitreihen-Lags nachbauen
    if time_series_mode:
        if time_col is None or lag_base_col is None or n_lags is None:
            raise ValueError("Zeitreihenmodell benötigt Zeitspalte, Lag-Basis-Spalte und Anzahl der Lags.")
        df_proc, lag_cols = make_lag_features(df_proc, time_col, lag_base_col, n_lags)
        feature_cols = lag_cols

    missing = [c for c in feature_cols if c not in df_proc.columns]
    if missing:
        raise ValueError(f"Folgende Feature-Spalten fehlen in den Daten: {missing}")

    X_raw = df_proc[feature_cols].copy()

    numeric_feature_cols = []
    categorical_feature_cols = []

    for col in X_raw.columns:
        s = X_raw[col]
        if pd.api.types.is_numeric_dtype(s):
            numeric_feature_cols.append(col)
        else:
            converted = _try_parse_numeric_series(s)
            if converted is not None:
                X_raw[col] = converted
                numeric_feature_cols.append(col)
            else:
                categorical_feature_cols.append(col)

    X_num = X_raw[numeric_feature_cols] if numeric_feature_cols else pd.DataFrame(index=df_proc.index)
    X_cat = X_raw[categorical_feature_cols] if categorical_feature_cols else pd.DataFrame(index=df_proc.index)

    if not X_cat.empty:
        X_cat_dummies = pd.get_dummies(X_cat, drop_first=True)
    else:
        X_cat_dummies = X_cat

    X_full = pd.concat([X_num, X_cat_dummies], axis=1)

    # Spalten an encoded_feature_names aus dem Training ausrichten
    if encoded_feature_names is not None:
        for col in encoded_feature_names:
            if col not in X_full.columns:
                X_full[col] = 0.0
        X_full = X_full[encoded_feature_names]

    # NaNs entfernen
    X_full = X_full.dropna()
    df_proc = df_proc.loc[X_full.index]

    return X_full, df_proc


# --------------------------- UI ---------------------------

st.markdown(
    """
    <style>
    .big-title {
        font-size: 8.0rem;
        font-weight: 700;
    }
    .subtitle {
        font-size: 1rem;
        color: #888888;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 ML-Studio")
st.text("Baue schnell eigene Modelle auf Basis deiner Finanz- & User-Daten. Wähle Algorithmus, Datenquelle, Features & Target – das ML Studio übernimmt den Rest.")

st.divider()

# --------------------------- Sidebar ---------------------------

with st.sidebar:
    st.header("⚙️ Settings")

    algo = st.selectbox(
        "Algorithms",
        [
            "Linear Regression",
            "Decision Tree",
            "Random Forest",
            "Classification (Logistic Regression)",
            "Directional Classification (LogReg, Up/Down)",
        ]
    )

    data_source = st.selectbox(
        "Data source",
        [
            "No Table selected",
            "Entire Yahoo Finance Pricing Table",
            "Yahoo Finance Pricing Single Stock",
            "Alphavantage",
            "Alphavantage (Combined)",
            "User Tables",
        ]
    )

    symbol = None
    table_name = None

    if data_source == "Yahoo Finance Pricing Single Stock":
        symbol = st.text_input("Symbol (z.B. AAPL, MSFT)", value="AAPL")

    elif data_source == "No Table selected":
        st.info("Choose Table")

    elif data_source == "Alphavantage":
        table_name = st.selectbox(
            "Alphavantage-Tabelle",
            ALPHAVANTAGE_TABLES
        )

    elif data_source == "User Tables":
        user_tables = list_user_tables()
        if user_tables:
            table_name = st.selectbox("Choose User Table", user_tables)
        else:
            st.warning("No Table found in Database")
            table_name = None

    st.markdown("---")

    test_size = st.slider(
        "Test set size",
        min_value=0.1,
        max_value=0.5,
        value=0.2,
        step=0.05,
    )

    scale_features = st.checkbox(
        "Scale features (StandardScaler)",
        value=True,
        help="Recommended for linear and logistic Regression",
    )

    use_time_series = st.checkbox(
        "Time Series Mode (Lag-Features from target)",
        value=False,
        help="Automatically generates lag features of the target column (e.g., close_lag_1 … close_lag_n) and uses them as input for the model.",
    )

    if use_time_series:
        n_lags = st.slider(
            "Number of lags",
            min_value=1,
            max_value=30,
            value=5,
            help="How many past values of the target column should be used as features.",
        )
    else:
        n_lags = None

    st.markdown("---")
    train_button = st.button("🚀 Start training")


# --------------------------- Tabs ---------------------------

tab1, tab2 = st.tabs(["🔬 ML Studio", "📁 Saved Models"])

# --------------------------- TAB 1: Training ---------------------------

with tab1:
    # ---------------------- Daten laden & Spaltenwahl ----------------------
    with st.spinner("Loading..."):
        df = load_data_from_source(data_source, symbol=symbol, table_name=table_name)

    if df is None or df.empty:
        st.warning("No data found!")
    else:
        st.subheader("📊 Data Overview")

        # kleine Kennzahlen oben
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Rows", len(df))
        with c2:
            st.metric("Columns", df.shape[1])
        with c3:
            time_guess = detect_time_column(df.copy())
            st.metric("Time column detected", time_guess if time_guess else "None")

        if data_source == "Alphavantage":
            st.header(table_name)
        elif data_source == "User Tables":
            st.header(table_name)
        else:
            st.header(data_source)

        with st.expander("Show Dataframe", expanded=True):
            st.dataframe(df.head(50), width="stretch")

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        all_cols = df.columns.tolist()

        st.markdown("#### 🔧 Feature & target Selection")

        col1, col2 = st.columns([2, 1])

        with col1:
            feature_cols = st.multiselect(
                "Feature-Columns (X)",
                options=all_cols,
                default=[c for c in numeric_cols if c != "target"][:5],
            )

        with col2:
            target_col = st.selectbox(
                "Target-Spalte (y)",
                options=all_cols,
            )

        # ---------------- Zukunfts-Target Einstellungen ----------------

        st.markdown("#### ⏩ Forecasting Horizon (Future-Target)")

        auto_time_col = detect_time_column(df)

        if auto_time_col is None:
            st.warning("⚠️ No suitable time column detected. Future target shifting is disabled.")
            time_col = None
            horizon_label = "No Shift (current target)"
        else:
            time_col = st.selectbox(
                "Time-Column for future target",
                options=[auto_time_col] + [c for c in all_cols if c != auto_time_col],
                index=0,
                help="Automatically detected time column used to shift the target into the future.",
            )
            horizon_label = st.selectbox(
                "Vorhersagehorizont",
                [
                    "Kein Shift (aktuelles Target)",
                    "1 Tag",
                    "3 Wochen",
                    "3 Monate",
                    "1 Jahr",
                ],
                index=0,
            )

        # Hinweis bei möglichem Leakage (nur für Regression kritisch)
        if (algo not in ["Klassifikation (Logistische Regression)", "Richtungsklassifikation (LogReg, Up/Down)"]
                and target_col in feature_cols
                and horizon_label == "Kein Shift (aktuelles Target)"
                and not use_time_series):
            st.warning(
                "Hinweis: Die Target-Spalte ist auch als Feature ausgewählt **ohne** Zeithorizont-Shift. "
                "Das kann zu Data Leakage führen. Mit Zeit-Shift oder Zeitreihenmodus ist das normalerweise unkritisch."
            )

        # ---------------------- Training ----------------------

        if train_button:
            if not feature_cols and not use_time_series:
                st.error("Bitte wähle mindestens eine Feature-Spalte aus (oder aktiviere den Zeitreihenmodus).")
            elif not target_col:
                st.error("Bitte wähle eine Target-Spalte aus.")
            else:
                try:
                    df_for_model = df.copy()

                    # Mindestanzahl an Zeilen checken
                    if len(df_for_model) < MIN_ROWS_FOR_MODEL:
                        st.info(
                            f"Das geladene Dataset hat nur {len(df_for_model)} Zeilen. "
                            f"Für ein sinnvolles Modell werden mindestens {MIN_ROWS_FOR_MODEL} Zeilen benötigt. "
                            "Bitte wähle eine andere Datenquelle oder einen längeren Zeitraum."
                        )
                        st.stop()

                    # Zeilenlimit, damit RAM nicht explodiert
                    if len(df_for_model) > MAX_ROWS_FOR_MODEL:
                        st.warning(
                            f"Dataset hat {len(df_for_model)} Zeilen – es werden nur die ersten {MAX_ROWS_FOR_MODEL} "
                            f"Zeilen zum Training verwendet."
                        )
                        df_for_model = df_for_model.head(MAX_ROWS_FOR_MODEL)

                    with st.spinner("Training in Progress..."):
                        # 1) Zukunfts-Target erzeugen (falls gewünscht)
                        if horizon_label != "Kein Shift (aktuelles Target)":
                            if time_col is None:
                                st.error("Es wurde keine gültige Zeitspalte erkannt. Shift des Targets ist nicht möglich.")
                                st.stop()
                            df_for_model, effective_target_col = make_future_target(
                                df_for_model, time_col, target_col, horizon_label
                            )
                            st.info(
                                f"Zukunfts-Target erzeugt: '{effective_target_col}' basiert auf '{target_col}' "
                                f"mit Horizont '{horizon_label}'."
                            )
                        else:
                            effective_target_col = target_col

                        # 1a) Richtungsklassifikation: binary Target bauen (Up/Down)
                        is_directional_cls = (algo == "Richtungsklassifikation (LogReg, Up/Down)")
                        if is_directional_cls:
                            if effective_target_col == target_col:
                                st.error(
                                    "Richtungsklassifikation benötigt einen Vorhersagehorizont "
                                    "(z.B. 1 Tag, 3 Wochen, 3 Monate)."
                                )
                                st.stop()

                            current_vals = pd.to_numeric(df_for_model[target_col], errors="coerce")
                            future_vals = pd.to_numeric(df_for_model[effective_target_col], errors="coerce")
                            df_for_model["direction_up"] = (future_vals > current_vals).astype(int)
                            effective_target_col = "direction_up"

                            st.info(
                                "Richtungsklassifikation aktiv: "
                                "Target = 1, wenn Future-Preis > aktueller Preis, sonst 0."
                            )

                        # 2) Zeitreihenmodus: Lag-Features aus Target bauen
                        active_feature_cols = feature_cols.copy()

                        if use_time_series:
                            if time_col is None:
                                st.error("Zeitreihenmodus benötigt eine gültige Zeitspalte.")
                                st.stop()

                            df_for_model, lag_cols = make_lag_features(
                                df_for_model,
                                time_col=time_col,
                                base_col=target_col,
                                n_lags=n_lags,
                            )
                            active_feature_cols = lag_cols

                            st.info(
                                f"Zeitreihenmodus aktiv: Verwende die Lag-Features {lag_cols[:3]} ... "
                                f"(insgesamt {len(lag_cols)}) als Input."
                            )

                        # Klassifikation vs. Regression
                        is_classification = algo in [
                            "Klassifikation (Logistische Regression)",
                            "Richtungsklassifikation (LogReg, Up/Down)",
                        ]

                        # Preprocessing
                        if is_classification:
                            X_used, y, X_encoded, scaler, label_encoder = preprocess_features_target_classification(
                                df_for_model,
                                active_feature_cols,
                                effective_target_col,
                                scale=scale_features,
                            )
                        else:
                            X_used, y, X_encoded, scaler = preprocess_features_target_regression(
                                df_for_model,
                                active_feature_cols,
                                effective_target_col,
                                scale=scale_features,
                            )
                            label_encoder = None

                        encoded_feature_names = list(X_encoded.columns)

                        if X_used.shape[0] < 5:
                            st.warning(
                                f"Nur {X_used.shape[0]} Zeilen nach Preprocessing übrig – "
                                f"das ist sehr wenig zum Trainieren."
                            )

                        X_train, X_test, y_train, y_test = train_test_split(
                            X_used,
                            y,
                            test_size=test_size,
                            random_state=42,
                            shuffle=not use_time_series,
                        )

                        st.success(f"Trainingsdaten vorbereitet: X_train={X_train.shape}, X_test={X_test.shape}")

                        # ---------------------- Modelltraining ----------------------

                        if is_classification:
                            model = LogisticRegression(max_iter=1000)
                            model.fit(X_train, y_train)
                            y_pred = model.predict(X_test)

                            if is_directional_cls:
                                st.markdown("### 🎯 Ergebnisse – Richtungsklassifikation (Up/Down)")
                                algo_name_for_save = "Richtungsklassifikation (LogReg)"
                            else:
                                st.markdown("### 🎯 Ergebnisse – Klassifikation (Logistische Regression)")
                                algo_name_for_save = "Logistische Regression (Klassifikation)"

                            acc = accuracy_score(y_test, y_pred)
                            st.metric("Accuracy", f"{acc:.4f}")

                            fig, ax = plt.subplots()
                            ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax)
                            ax.set_title("Konfusionsmatrix")
                            st.pyplot(fig)

                        else:
                            if algo == "Lineare Regression":
                                model = LinearRegression()
                                algo_name_for_save = "Lineare Regression"
                            elif algo == "Decision Tree":
                                model = DecisionTreeRegressor(random_state=42)
                                algo_name_for_save = "Decision Tree (Regression)"
                            else:  # Random Forest
                                model = RandomForestRegressor(
                                    n_estimators=200,
                                    random_state=42,
                                )
                                algo_name_for_save = "Random Forest (Regression)"

                            model.fit(X_train, y_train)
                            y_pred = model.predict(X_test)

                            st.markdown(f"### 📈 Ergebnisse – {algo_name_for_save}")

                            mse = mean_squared_error(y_test, y_pred)
                            rmse = np.sqrt(mse)
                            r2 = r2_score(y_test, y_pred)

                            m1, m2, m3 = st.columns(3)
                            m1.metric("RMSE", f"{rmse:.4f}")
                            m2.metric("MSE", f"{mse:.4f}")
                            m3.metric("R²", f"{r2:.4f}")

                            st.line_chart(
                                pd.DataFrame({"y_true": y_test, "y_pred": y_pred}).reset_index(drop=True)
                            )

                        # ---------------------- Modell speichern ----------------------

                        feature_dtypes = (
                            df_for_model[active_feature_cols]
                            .dtypes.astype(str)
                            .to_dict()
                        )

                        save_path = save_model_bundle(
                            model=model,
                            algo_name=algo_name_for_save,
                            data_source=data_source,
                            feature_cols=active_feature_cols,
                            target_col=effective_target_col,
                            scaler=scaler,
                            horizon_label=horizon_label,
                            label_encoder=label_encoder,
                            time_series_mode=use_time_series,
                            n_lags=n_lags,
                            base_col=target_col if use_time_series else None,
                            encoded_feature_names=encoded_feature_names,
                            feature_dtypes=feature_dtypes,
                        )

                        st.success(f"Modell gespeichert unter: `{save_path}`")
                        st.caption("Du kannst diese .pkl-Datei in einem anderen Tab laden und für neue Vorhersagen nutzen.")

                except Exception as e:
                    st.error(f"Fehler beim Training oder bei der Auswertung: {e}")


# --------------------------- TAB 2: Gespeicherte Modelle ---------------------------

with tab2:
    st.subheader("📁 Gespeicherte Modelle")

    # Alle .pkl-Dateien im MODEL_DIR einsammeln
    try:
        model_files = sorted(
            [f for f in os.listdir(MODEL_DIR) if f.endswith(".pkl")]
        )
    except FileNotFoundError:
        st.info("Der Ordner für gespeicherte Modelle existiert noch nicht.")
        model_files = []

    if not model_files:
        st.info("Es wurden noch keine Modelle in `saved_models` gespeichert.")
    else:
        # Übersichtstabelle vorbereiten
        overview_rows = []
        for fname in model_files:
            path = os.path.join(MODEL_DIR, fname)
            try:
                bundle = joblib.load(path)
                overview_rows.append({
                    "Datei": fname,
                    "Algorithmus": bundle.get("algo", "-"),
                    "Datenquelle": bundle.get("data_source", "-"),
                    "Target": bundle.get("target_col", "-"),
                    "Horizont": bundle.get("horizon", "-"),
                    "Zeitreihenmodus": bundle.get("time_series_mode", False),
                    "Lags": bundle.get("n_lags", None),
                    "Lag-Basis": bundle.get("lag_base_col", None),
                    "Anzahl Features": len(bundle.get("feature_cols", []) or []),
                    "Gespeichert am": bundle.get("saved_at", "-"),
                })
            except Exception as e:
                overview_rows.append({
                    "Datei": fname,
                    "Algorithmus": f"⚠️ Fehler beim Laden: {e}",
                    "Datenquelle": "-",
                    "Target": "-",
                    "Horizont": "-",
                    "Zeitreihenmodus": "-",
                    "Lags": "-",
                    "Lag-Basis": "-",
                    "Anzahl Features": "-",
                    "Gespeichert am": "-",
                })

        st.markdown("### 🔎 Modell-Übersicht")
        overview_df = pd.DataFrame(overview_rows)
        st.dataframe(overview_df, width="stretch")

        # Detailansicht für ein ausgewähltes Modell
        st.markdown("### 🧬 Modellauswahl")

        selected_file = st.selectbox(
            "Modell auswählen",
            model_files,
            index=0,
        )

        if selected_file:
            path = os.path.join(MODEL_DIR, selected_file)

            try:
                bundle = joblib.load(path)
            except Exception as e:
                st.error(f"Modell-Bundle konnte nicht geladen werden: {e}")
            else:
                col_meta, col_dl = st.columns([3, 1])

                with col_meta:
                    st.markdown(f"#### Details zu `{selected_file}`")

                    st.write("**Algorithmus:**", bundle.get("algo", "-"))
                    st.write("**Datenquelle:**", bundle.get("data_source", "-"))
                    st.write("**Target-Spalte:**", bundle.get("target_col", "-"))
                    st.write("**Vorhersagehorizont:**", bundle.get("horizon", "-"))

                    st.write("**Zeitreihenmodus:**", "Ja" if bundle.get("time_series_mode") else "Nein")
                    if bundle.get("time_series_mode"):
                        st.write("• Lags:", bundle.get("n_lags"))
                        st.write("• Lag-Basis-Spalte:", bundle.get("lag_base_col"))

                    feature_cols_b = bundle.get("feature_cols", []) or []
                    feature_dtypes_b = bundle.get("feature_dtypes", {}) or {}

                    st.write(f"**Features (X) – {len(feature_cols_b)} Spalten:**")
                    if feature_cols_b:
                        lines = []
                        for col in feature_cols_b:
                            dtype = feature_dtypes_b.get(col, "?")
                            # "Länge": für Floats sagen wir explizit 3 Nachkommastellen
                            if isinstance(dtype, str) and ("float" in dtype or "double" in dtype):
                                lines.append(f"{col}  ({dtype}, 3 Nachkommastellen)")
                            else:
                                lines.append(f"{col}  ({dtype})")
                        st.code("\n".join(lines), language="text")
                    else:
                        st.write("_Keine Feature-Liste im Bundle gefunden._")

                    st.write("**Gespeichert am:**", bundle.get("saved_at", "-"))

                with col_dl:
                    st.markdown("#### Download")
                    try:
                        with open(path, "rb") as f:
                            st.download_button(
                                label="⬇️ Modell herunterladen",
                                data=f,
                                file_name=selected_file,
                                mime="application/octet-stream",
                            )
                    except Exception as e:
                        st.warning(f"Download nicht möglich: {e}")

                st.info(
                    "💡 Hinweis: Dieses Modell wurde mit genau den oben gelisteten Feature-Spalten trainiert. "
                    "Wenn du es später für Vorhersagen verwenden möchtest, musst du dieselben Feature-Spalten "
                    "in derselben Struktur wieder bereitstellen."
                )

                # --- Modell ausprobieren ---
                with st.expander("🧪 Modell mit aktuellen Daten ausprobieren", expanded=False):
                    st.write(
                        "Es werden die aktuell in der Sidebar gewählte Datenquelle, das Symbol bzw. die Tabelle verwendet. "
                        "Achte darauf, dass diese mit den Trainingsdaten kompatibel sind."
                    )

                    df_pred = load_data_from_source(data_source, symbol=symbol, table_name=table_name)

                    if df_pred is None or df_pred.empty:
                        st.info(
                            "Keine Daten aus der aktuell gewählten Datenquelle geladen. "
                            "Bitte wähle in der Sidebar eine passende Quelle aus."
                        )
                    else:
                        st.write(f"Aktuelle Daten: **{len(df_pred)} Zeilen**, **{df_pred.shape[1]} Spalten**.")

                        time_col_pred = None
                        if bundle.get("time_series_mode"):
                            auto_time_pred = detect_time_column(df_pred.copy())
                            if auto_time_pred is not None:
                                time_options = [auto_time_pred] + [c for c in df_pred.columns if c != auto_time_pred]
                                default_index = 0
                            else:
                                time_options = list(df_pred.columns)
                                default_index = 0

                            time_col_pred = st.selectbox(
                                "Zeitspalte für Vorhersage (für Lags)",
                                options=time_options,
                                index=default_index,
                            )

                        max_rows_pred = min(500, len(df_pred))
                        min_rows_pred = 1 if len(df_pred) < 10 else 10

                        n_rows_pred = st.slider(
                            "Wie viele der letzten Zeilen für Vorhersage verwenden?",
                            min_value=min_rows_pred,
                            max_value=max_rows_pred,
                            value=max_rows_pred,
                        )

                        if st.button("🔮 Vorhersage mit diesem Modell berechnen"):
                            try:
                                df_for_pred = df_pred.tail(n_rows_pred)

                                encoded_feature_names = bundle.get("encoded_feature_names")
                                X_full_pred, df_proc_pred = build_X_for_prediction(
                                    df_for_pred,
                                    feature_cols=bundle.get("feature_cols", []),
                                    encoded_feature_names=encoded_feature_names,
                                    time_series_mode=bundle.get("time_series_mode", False),
                                    lag_base_col=bundle.get("lag_base_col"),
                                    n_lags=bundle.get("n_lags"),
                                    time_col=time_col_pred,
                                )

                                scaler = bundle.get("scaler")
                                if scaler is not None:
                                    X_used_pred = scaler.transform(X_full_pred.values)
                                else:
                                    X_used_pred = X_full_pred.values

                                model = bundle["model"]
                                y_pred = model.predict(X_used_pred)

                                label_encoder = bundle.get("label_encoder")
                                if label_encoder is not None:
                                    y_pred_decoded = label_encoder.inverse_transform(y_pred)
                                else:
                                    y_pred_decoded = y_pred

                                # Output DataFrame
                                result_df = pd.DataFrame(index=df_proc_pred.index)
                                if bundle.get("time_series_mode") and time_col_pred is not None and time_col_pred in df_proc_pred.columns:
                                    result_df[time_col_pred] = df_proc_pred[time_col_pred]

                                result_df["prediction"] = y_pred_decoded

                                st.markdown("#### Vorhersagen (letzte Zeilen)")
                                st.dataframe(result_df.tail(50), width="stretch")

                            except Exception as e:
                                st.error(f"Vorhersage nicht möglich: {e}")