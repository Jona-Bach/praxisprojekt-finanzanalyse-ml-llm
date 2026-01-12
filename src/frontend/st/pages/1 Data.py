import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
from backend.data_model import TICKERS
from backend.scheduler import load_data, load_initial_data
from backend.database.db_functions import get_table, get_table_names, get_symbols_from_table, get_unique_table, get_yf_company_info, get_yf_price_history, get_yf_pricing_raw, get_config_dict
from backend.data_processing.alphavantage_processed import get_processed_table, process_alphavantage_raw_db, get_processed_entries_by_symbol, get_unique_symbols_from_table
from backend.database.users_database import import_file_as_table, get_user_table, list_user_tables
from backend.api_services.yf_connect import download_yf_company_info, download_yf_pricing_raw_newest, download_yf_pricing_raw_timeperiod
import openpyxl
# Ordner der aktuellen Datei (z.B. app.py)
BASE_DIR = Path(__file__).resolve().parent

# Pfad zur PNG
img_path_fsbar = BASE_DIR.parent / "assets" / "finsightbar.png"
#__________________________Header____________________________

st.set_page_config(page_title="Data", page_icon="🔍")
#__________________________Global Dekleration_____________________________

tab1, tab2 = st.tabs(["Analysis","Data Settings"])
database_path_yf = "data/yfinance.db"

selected_date_cfg = get_config_dict("selected_date_for_ticker_download")

if selected_date_cfg and "Value" in selected_date_cfg:
    timeperiod_for_download = selected_date_cfg["Value"]
else:
    timeperiod_for_download = "2020-01-01"

CARD_STYLE = """
<style>
.info-card {
    background-color: #1f2937;
    padding: 1rem 1.2rem;
    border-radius: 0.8rem;
    border: 1px solid #374151;
    margin-bottom: 1rem;
}
.info-title {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-bottom: 0.3rem;
}
.info-value {
    font-size: 1.0rem;
    font-weight: 600;
    color: #f9fafb;
    overflow-wrap: break-word;
}
</style>
"""
st.markdown(CARD_STYLE, unsafe_allow_html=True)


def info_card(title, value):
    value = value if value else "—"
    return f"""
    <div class="info-card">
        <div class="info-title">{title}</div>
        <div class="info-value">{value}</div>
    </div>
    """

def format_number(value):
    if value is None:
        return "—"

    # String → Float umwandeln
    if isinstance(value, str):
        value = value.replace(".", "").replace(",", "")
        try:
            value = float(value)
        except:
            return "—"

    abs_val = abs(value)

    # Billiarden (10^15)
    if abs_val >= 1_000_000_000_000_000:
        return f"{value / 1_000_000_000_000_000:.2f} Bil"

    # Billionen (10^12)
    elif abs_val >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f} Bio."

    # Milliarden (10^9)
    elif abs_val >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} Mrd."

    # Millionen (10^6)
    elif abs_val >= 1_000_000:
        return f"{value / 1_000_000:.2f} Mio."

    # Tausend
    elif abs_val >= 1_000:
        return f"{value / 1_000:.2f} Tsd."

    # Normale Zahl
    else:
        return f"{value:.2f}"

def format_number_en(value):
    """
    Format number using English short scale:
    - T (Trillion)
    - B (Billion)
    - M (Million)
    - K (Thousand)

    Always 2 decimals, automatically converts strings, adds $ sign.
    """
    if value is None:
        return "—"

    # Convert strings to float
    if isinstance(value, str):
        try:
            value = float(value.replace(",", "").replace(" ", ""))
        except:
            return "—"

    abs_val = abs(value)

    # Trillion (10^12)
    if abs_val >= 1_000_000_000_000:
        return f"$ {value / 1_000_000_000_000:.2f} Trillion"

    # Billion (10^9)
    elif abs_val >= 1_000_000_000:
        return f"$ {value / 1_000_000_000:.2f} Billion"

    # Million (10^6)
    elif abs_val >= 1_000_000:
        return f"$ {value / 1_000_000:.2f} Million"

    # Thousand (10^3)
    elif abs_val >= 1_000:
        return f"$ {value / 1_000:.2f} Thousand"

    # Normal number
    else:
        return f"$ {value:.2f}"

from datetime import datetime

def format_date_string(date_str):
    # Versucht ISO-Format zuerst (z. B. "2025-01-21 13:44:22")
    try:
        dt = datetime.fromisoformat(date_str)
    except:
        # Fallback für andere typische Formate
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except:
                return date_str  # not parsable, return as-is

    return dt.strftime("%d %b %Y")  # z. B. "21 Jan 2025"
def parse_number(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()

    # "1.234,56" -> "1234.56"
    if "." in s and "," in s:
        s = s.replace(".", "").replace(",", ".")
    # "24,31" -> "24.31"
    elif "," in s:
        s = s.replace(",", ".")

    try:
        return float(s)
    except:
        return None


def format_ratio(value, decimals=2, suffix=""):
    v = parse_number(value)
    if v is None:
        return "—"
    return f"{v:.{decimals}f}{suffix}"


def format_percent(value, decimals=2, already_percent=False):
    v = parse_number(value)
    if v is None:
        return "—"
    if not already_percent:   # falls Rohwert 0.188 => 18.8%
        v *= 100
    return f"{v:.{decimals}f}%"
def format_pe(value, decimals=2):
    if value is None:
        return "—"

    # String sauber parsen (Deutsch/Englisch)
    if isinstance(value, str):
        s = value.strip()
        if "," in s and "." in s:          # z.B. "1.234,56"
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:                      # z.B. "24,31"
            s = s.replace(",", ".")         # -> "24.31"
        try:
            value = float(s)
        except:
            return "—"

    # Optional: negative PE ausblenden
    # if value <= 0:
    #     return "—"

    return f"{value:.{decimals}f}x"
symbols_yf_history = get_symbols_from_table(database_path=database_path_yf, table_name="yf_price_history")
symbols_yf_raw = get_symbols_from_table(database_path=database_path_yf, table_name="yf_pricing_raw")
symbols_yf_company_info = get_symbols_from_table(database_path=database_path_yf, table_name="yf_company_info")
symbols_av_processed = get_unique_symbols_from_table(table_name="alphavantage_processed_kpi")

combined_symbols = list(
set(symbols_yf_history + symbols_yf_company_info + symbols_av_processed + symbols_yf_raw)
)

combined_symbols = sorted(combined_symbols)

common_symbols = list(
    set(symbols_yf_history)
    & set(symbols_yf_company_info)
    & set(symbols_av_processed)
)

common_symbols = sorted(common_symbols)


#__________________________SIDEBAR___________________________
st.sidebar.subheader("Data")
#st.sidebar.image(str(img_path_fsbar))
st.sidebar.divider()

if "load_data_time" in st.session_state:
    loaded_data_ts = st.session_state["load_data_time"]
else:
    st.session_state["load_data_time"] = "NOT NOW"
    loaded_data_ts = st.session_state["load_data_time"]


st.sidebar.subheader("Options:")

st.sidebar.info(f"Last data update: {loaded_data_ts}")
if st.sidebar.button("Update All Data"):
    with st.spinner("Updating data (this might take a while...)"):
        # database_path = "data/alphavantage.db"
        # av_raw_data_symbols = get_symbols_from_table(database_path=database_path, table_name="alphavantage_raw_kpi")
        # av_pricing_symbols = get_symbols_from_table(database_path=database_path, table_name="alphavantage_daily_pricing")
        all_tickers_to_update = combined_symbols
        answer = load_data(all_tickers_to_update)
        download_yf_pricing_raw_newest(all_tickers_to_update)
        download_yf_company_info(all_tickers_to_update)
        st.success(answer)
    updated_time = datetime.now().replace(microsecond=0)
    st.success(f"Updated Data at:{updated_time}!")

if st.sidebar.button("Update Processed Data"):
    process_alphavantage_raw_db()
    st.success("Updated Processed Data!")

t_choice = st.sidebar.multiselect(
    "Choose Ticker",
    options=combined_symbols)

st.session_state["chosen_tickers"] = t_choice

if st.sidebar.button("Update Single Ticker Data"):
    with st.spinner("Adding data (this might take a while...)"):
        answer = load_data(t_choice)
        download_yf_pricing_raw_newest(t_choice)
        st.success(answer)
    st.success("Download Complete!")



t_choice_download = st.sidebar.text_input("Search Stock", placeholder="Type in Stock Symbol", 
                                          help="""Choose Ticker to download. 
                                          The Ticker Data will be downloaded for 5 Years max. 
                                          If you want to change this change it in the Settings""")

st.session_state["chosen_tickers_to_download"] = t_choice_download

if st.sidebar.button("Download Ticker Data"):
    with st.spinner("Downloading data (this might take a while...)"):
        try:
            t_choice_download_load = [t_choice_download]
            answer = load_data(t_choice_download_load)
            download_yf_company_info(t_choice_download_load)
            download_yf_pricing_raw_timeperiod(t_choice_download_load, startdate=timeperiod_for_download, enddate="2025-01-01")
            if t_choice_download and t_choice_download not in TICKERS:
                TICKERS.append(t_choice_download)
            st.success(answer)
        except Exception as e:
            st.error(f"Could not add Ticker: {e}")
    st.success("Download Complete!")



st.sidebar.divider()


st.sidebar.subheader("Create your own Database")

# 1. Datei-Upload
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"],
)

# 2. Tabellenname
default_table_name = ""
if uploaded_file is not None:
    # Vorschlag: Dateiname ohne Endung
    default_table_name = uploaded_file.name.rsplit(".", 1)[0]

table_name = st.sidebar.text_input(
    "Table name in database",
    value=default_table_name,
    help="Name of your table in Database",
)

# 3. Verhalten bei vorhandener Tabelle
if_exists_option = st.sidebar.selectbox(
    "If table exists",
    options=["fail", "replace", "append"],
    index=1,  # default: replace
    help=(
        "'fail' = Fail, if Table exists\n"
        "'replace' = Delete Table + create new\n"
        "'append' = Append Rows to Table"
    ),
)

# 4. Import-Button
if st.sidebar.button("Import file into database"):
    if uploaded_file is None:
        st.sidebar.error("Please upload a file first.")
    elif not table_name:
        st.sidebar.error("Please enter a table name.")
    else:
        try:
            df_preview = import_file_as_table(
                file_obj=uploaded_file,
                filename=uploaded_file.name,
                table_name=table_name,
                if_exists=if_exists_option,
            )
            st.success(f"✅ Table '{table_name}' successfully saved in users_database.")
            st.write("### Preview of imported data")
            st.dataframe(df_preview.head(), hide_index=True)
        except Exception as e:
            st.error(f"❌ Error while importing: {e}")













#___________________________Data Tab_________________________________


with tab1:

    st.header("Single Stock Analysis")

    with st.container():
        #st.subheader("Basic Analysis")
        ticker_to_analyze = st.selectbox(
            label="Choose Stock to Analyze",
            options=combined_symbols
        )
        try:
            stock_info = get_yf_company_info(ticker_to_analyze) # STOCK INFOOOO
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(info_card("Symbol", stock_info["symbol"].iloc[0]), unsafe_allow_html=True)
            with col2:
                st.markdown(info_card("Short Name", stock_info["shortName"].iloc[0]), unsafe_allow_html=True)
            with col3:
                st.markdown(info_card("Country", stock_info["country"].iloc[0]), unsafe_allow_html=True)
            
            col4, col5, col6 = st.columns(3)
            with col4:
                st.markdown(info_card("Sector", stock_info["sector"].iloc[0]), unsafe_allow_html=True)
            with col5:
                st.markdown(info_card("Industry", stock_info["industry"].iloc[0]), unsafe_allow_html=True)
            with col6:
                st.markdown(info_card("Website", stock_info["website"].iloc[0]), unsafe_allow_html=True)

            st.markdown(info_card("Business Summary", stock_info["longBusinessSummary"].iloc[0]), unsafe_allow_html=True)
            st.divider()

            col7, col8, col9 = st.columns(3)
        except Exception as e:
            st.warning("Missing Data! Try loading Initial data from Settings!")
        try:
            # Versuche vorhandene Daten zu lesen
            up_to_date_av_entries = get_processed_entries_by_symbol(
                "alphavantage_processed_kpi", ticker_to_analyze
            )

            # Falls leer → Daten müssen nachgeladen werden
            if up_to_date_av_entries is None or len(up_to_date_av_entries) == 0:
                raise ValueError("No Data found!")

        except Exception:
            # Daten laden
            with st.spinner("Loading current data.."):
                load_data([ticker_to_analyze])

                # Erneut abrufen
                up_to_date_av_entries = get_processed_entries_by_symbol(
                    "alphavantage_processed_kpi", ticker_to_analyze
                )
        try:
            data_updated_time = up_to_date_av_entries.sort_values("timestamp", ascending=False)["timestamp"].iloc[0]

            market_cap_str = up_to_date_av_entries.sort_values("timestamp", ascending=False)["market_capitalization"].iloc[0]
            market_cap = format_number(market_cap_str)
            pre_ratio_str = up_to_date_av_entries.sort_values("timestamp", ascending=False)["pe_ratio"].iloc[0]
            pe_ratio = format_ratio(pre_ratio_str, 2, "x")
            price_to_book_ratio_str = up_to_date_av_entries.sort_values("timestamp", ascending=False)["price_to_book_ratio"].iloc[0]
            ptbr = format_ratio(price_to_book_ratio_str, 2)
            
            col7.metric("Market Capitalization", market_cap)
            col8.metric("PE-Ratio", pe_ratio)
            col9.metric("Price/Book", price_to_book_ratio_str)

            col10, col11, col12 = st.columns(3)

            roe_str = up_to_date_av_entries.sort_values("timestamp", ascending=False)["return_on_equity_ttm"].iloc[0]
            roe = format_percent(roe_str, 2, already_percent=False)
            profit_margin_str = up_to_date_av_entries.sort_values("timestamp", ascending=False)["profit_margin_raw"].iloc[0]
            profit_margin = format_percent(profit_margin_str, 2, already_percent=False)
            beta = up_to_date_av_entries.sort_values("timestamp", ascending=False)["beta_raw"].iloc[0]
            beta = format_ratio(beta, 2)

                
            col10.metric("ROE", roe)
            col11.metric("Profit-Margin", f"{profit_margin}")
            col12.metric("Beta", beta)

            st.write("")
            st.caption(f"Last Updated: {format_date_string(data_updated_time)}")
            st.divider()
        except Exception as e:
            st.warning("Missing Data")

        def plot_price_history(ticker: str):
            # Pricing-Daten laden
            pricing_ticker_data = get_yf_price_history(ticker)

            if pricing_ticker_data.empty:
                pricing_ticker_data = get_yf_pricing_raw(ticker)

            if pricing_ticker_data.empty:
                st.warning(f"No pricing data for {ticker} found.")
                return

            # ---------------------------
            # Auswahl der Metrik (Y-Achse)
            # ---------------------------
            y_option = st.selectbox(
                "Choose Metric",
                ["close", "open", "high", "low", "volume"],
                index=0
            )

            # ---------------------------
            # User kann "ältestes" Startdatum festlegen
            # ---------------------------
            min_date = pricing_ticker_data["date"].min()
            max_date = pricing_ticker_data["date"].max()

            start_date = st.date_input(
                "Starting Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )

            # Daten entsprechend filtern
            filtered_df = pricing_ticker_data[
                pricing_ticker_data["date"] >= start_date
            ]

            # ---------------------------
            # Plot erstellen
            # ---------------------------
            fig = px.line(
                filtered_df,
                x="date",
                y=y_option,
                title=f"{ticker} — {y_option} over time",
            )

            # Weiße Linie
            #fig.update_traces(line=dict(color="white"))

            # Layout
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title=y_option.capitalize(),
                template="plotly_dark",
                height=450,
            )

            # RangeSlider unter dem Chart
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeslider=dict(
                    bgcolor="rgba(255,255,255,0.05)"
                ),
            )

            st.plotly_chart(fig, width="stretch")
        plot_price_history(ticker_to_analyze)

    st.divider()
    st.header("Compared Stock Analysis")
    with st.container():
        tickers_to_compare = st.multiselect(
            label="Choose Stocks to Compare",
            options=TICKERS
        )

        def plot_compare_stocks(tickers: list):
            if not tickers:
                st.info("Please select at least one stock.")
                return

            # --- Daten aller Ticker für globales Mindestdatum laden ---
            all_data = {}
            for stock in tickers:
                df = get_yf_pricing_raw(stock)
                if df.empty:
                    st.warning(f"No data for {stock}")
                    continue
                all_data[stock] = df

            if not all_data:
                st.warning("No data found for selected tickers.")
                return

            # Globales minimalstes Datum aller geladenen Ticker
            global_min_date = min(df["date"].min() for df in all_data.values())
            global_max_date = max(df["date"].max() for df in all_data.values())

            # --- Start Date Auswahl ---
            start_date = st.date_input(
                "Start Date",
                value=global_min_date,
                min_value=global_min_date,
                max_value=global_max_date
            )

            # --- Plot erstellen ---
            fig = go.Figure()

            for stock, df in all_data.items():

                # Startdatum anwenden
                df_filtered = df[df["date"] >= start_date]

                fig.add_trace(
                    go.Scatter(
                        x=df_filtered["date"],
                        y=df_filtered["close"],
                        mode="lines",
                        name=stock
                    )
                )

            fig.update_layout(
                title="Stock Comparison (Close Prices)",
                xaxis_title="Date",
                yaxis_title="Close Price",
                template="plotly_dark",
                height=500
            )

            # Plotly-Rangeslider
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeslider=dict(bgcolor="rgba(255,255,255,0.05)")
            )

            st.plotly_chart(fig, width="stretch")
        plot_compare_stocks(tickers_to_compare)


        def compare_stock_metrics(tickers):
            if not tickers:
                st.info("Please select at least one stock.")
                return

            # Eine Column pro Ticker
            cols = st.columns(len(tickers))

            for idx, stock in enumerate(tickers):
                df = get_processed_entries_by_symbol("alphavantage_processed_kpi", stock)

                if df.empty:
                    cols[idx].warning(f"No KPI data for {stock}")
                    continue

                # Neuester Eintrag
                latest = df.sort_values("timestamp", ascending=False).iloc[0]

                # Extract + Format
                market_cap = format_number(latest["market_capitalization"])
                pe_ratio   = format_number(latest["pe_ratio"])
                ptbr       = format_number(latest["price_to_book_ratio"])

                with cols[idx]:
                    st.subheader(stock)

                    st.metric("Market Cap", market_cap)
                    st.metric("PE Ratio", pe_ratio)
                    st.metric("Price/Book", ptbr)
        compare_stock_metrics(tickers_to_compare)
        st.divider()







with tab2:
    st.title("Database Viewer")

    st.markdown("Explore all Alphavantage tables as well as your own uploaded datasets.")

    # ---------------------------------------------------------------
    # SECTION 1: Alphavantage RAW data
    # ---------------------------------------------------------------
    st.subheader("Alphavantage Raw KPI Data")
    try:
        df_raw_kpi = get_table("alphavantage_raw_kpi")
        st.dataframe(df_raw_kpi, hide_index=True, width="stretch")
    except Exception as e:
        st.error(f"Could not load raw KPI data: {e}")

    st.subheader("Alphavantage Raw Pricing Data")
    try:
        df_raw_pricing = get_table("alphavantage_daily_pricing")
        st.dataframe(df_raw_pricing, hide_index=True, width="stretch")
    except Exception as e:
        st.error(f"Could not load raw pricing data: {e}")

    st.divider()

    # ---------------------------------------------------------------
    # SECTION 2: Alphavantage Processed data
    # ---------------------------------------------------------------
    st.subheader("Processed KPI Data")
    try:
        df_processed_kpi = get_processed_table("alphavantage_processed_kpi")
        st.dataframe(df_processed_kpi, hide_index=True, width="stretch")
    except Exception as e:
        st.error(f"Could not load processed KPI data: {e}")

    st.subheader("Processed Pricing Data")
    try:
        df_processed_pricing = get_processed_table("alphavantage_pricing_processed")
        st.dataframe(df_processed_pricing, hide_index=True, width="stretch")
    except Exception as e:
        st.error(f"Could not load processed pricing data: {e}")

    st.divider()

    # ---------------------------------------------------------------
    # SECTION 3: User-created database tables
    # ---------------------------------------------------------------
    st.subheader("User-created Database Tables")
    st.markdown("These tables come from your uploaded CSV or Excel files.")

    try:
        user_tables = list_user_tables()
    except Exception as e:
        user_tables = []
        st.error(f"Could not list user tables: {e}")

    if not user_tables:
        st.info("No user tables found yet. Upload a CSV or Excel file to create one.")

    # Table selection
    chosen_table = st.selectbox("Select a table to view:", user_tables)

    if chosen_table:
        try:
            df_user_table = get_user_table(chosen_table)
            st.write(f"### Table: `{chosen_table}` — {len(df_user_table)} rows")
            st.dataframe(df_user_table, hide_index=True, width = "stretch")
        except Exception as e:
            st.error(f"Error loading table '{chosen_table}': {e}")
