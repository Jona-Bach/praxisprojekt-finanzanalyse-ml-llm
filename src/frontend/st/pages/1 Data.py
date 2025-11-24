import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
from datetime import datetime
from backend.data_model import TICKERS
from backend.scheduler import load_data, load_initial_data
from backend.database.db_functions import get_table, get_table_names, get_symbols_from_table, get_unique_table, get_yf_company_info
from backend.data_processing.alphavantage_processed import get_processed_table, process_alphavantage_raw_db, get_processed_entries_by_symbol
from backend.database.users_database import import_file_as_table, get_user_table, list_user_tables
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
if st.sidebar.button("Update Data"):
    with st.spinner("Updating data (this might take a while...)"):
        database_path = "data/alphavantage.db"
        av_raw_data_symbols = get_symbols_from_table(database_path=database_path, table_name="alphavantage_raw_kpi")
        av_pricing_symbols = get_symbols_from_table(database_path=database_path, table_name="alphavantage_daily_pricing")
        all_tickers_to_update = av_raw_data_symbols + av_pricing_symbols
        unique_list = sorted(list(set(all_tickers_to_update)))
        answer = load_data(unique_list)
        st.success(answer)
    updated_time = datetime.now().replace(microsecond=0)
    st.success(f"Updated Data at:{updated_time}!")

if st.sidebar.button("Update Processed Data"):
    process_alphavantage_raw_db()
    st.success("Updated Processed Data!")

t_choice = st.sidebar.multiselect(
    "Choose Ticker",
    options=sorted(TICKERS))

st.session_state["chosen_tickers"] = t_choice

if st.sidebar.button("Download Ticker Data"):
    with st.spinner("Downloading data (this might take a while...)"):
        answer = load_data(t_choice)
        st.success(answer)
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
    help="Name der Tabelle in deiner users_database",
)

# 3. Verhalten bei vorhandener Tabelle
if_exists_option = st.sidebar.selectbox(
    "If table exists",
    options=["fail", "replace", "append"],
    index=1,  # default: replace
    help=(
        "'fail' = Fehler, wenn Tabelle existiert\n"
        "'replace' = Tabelle löschen + neu anlegen\n"
        "'append' = Zeilen an bestehende Tabelle anhängen"
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

    st.header("Market Analysis")
    st.divider()

    with st.container():
        st.subheader("Ticker Analysis")
        ticker_to_analyze = st.selectbox(
            label="Choose Stock to Analyze",
            options=TICKERS
        )
        stock_info = get_yf_company_info(ticker_to_analyze)
        st.dataframe(stock_info)







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
