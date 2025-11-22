import time
from datetime import datetime
from src.backend.api_services.av_connect import fetch_alphavantage_raw, fetch_alphavantage_price_today
from src.backend.data_model import initial_tickers, TICKERS
from backend.database.db_functions import get_list_system_config
from backend.data_processing.alphavantage_processed import process_alphavantage_raw_db
import streamlit as st
now = datetime.now().replace(microsecond=0)


def load_data(data: list):
    st.session_state["load_data_time"] = now
    status_raw_data = st.empty()
    status_pricing_data = st.empty()
    today = datetime.today()
    print(f"Downloading data at: {today} ")
    #status_raw_data.write("Downloading...")

    for ticker in data:
        try:
            fetch_alphavantage_raw(ticker)
            status_raw_data.write(f"Fetched Raw Data for: {ticker}")
            fetch_alphavantage_price_today(ticker)
            status_pricing_data.write(f"Fetched Pricing Data for: {ticker}")
            print(f"{ticker} added to Database!")
            st.success(f"{ticker} was added successfully to the Database!")
        except Exception as e:
            st.error(f"Could not load data for {ticker}")

        time.sleep(30)
    
    return f"Updated data at: {today}"

def load_initial_data():
    st.session_state["load_data_time"] = now
    status_raw_data = st.empty()
    status_pricing_data = st.empty()
    today = datetime.today()
    print(f"Loading data at: {today} ")
    #status_raw_data.write("Loading...")

    new_custom_ticker = get_list_system_config("Custom_Initial_Tickers")
    if new_custom_ticker is not None:
        initial_tickers_list = new_custom_ticker
    else:
        initial_tickers_list = initial_tickers

    for ticker in initial_tickers_list:
        try:
            fetch_alphavantage_raw(ticker)
            status_raw_data.write(f"Fetched Raw Data for: {ticker}")
            fetch_alphavantage_price_today(ticker)
            status_pricing_data.write(f"Fetched Pricing Data for: {ticker}")
            print(f"{ticker} added to Database!")
            st.success(f"{ticker} was added successfully to the Database!")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(30)
    
    return f"Updated data at: {today}"