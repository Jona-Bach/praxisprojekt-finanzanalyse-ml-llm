import time
from datetime import datetime
from src.backend.api_services.av_connect import fetch_alphavantage_raw, fetch_alphavantage_price_today
from src.backend.data_model import tickers
import streamlit as st
now = datetime.now().replace(microsecond=0)


def load_data():
    st.session_state["load_data_time"] = now
    status_raw_data = st.empty()
    status_pricing_data = st.empty()
    today = datetime.today()
    print(f"Loading data at: {today} ")
    status_raw_data.write("Loading...")

    for ticker in tickers:
        try:
            fetch_alphavantage_raw(ticker)
            status_raw_data.write(f"Fetched Raw Data for: {ticker}")
            fetch_alphavantage_price_today(ticker)
            status_pricing_data.write(f"Fetched Pricing Data for: {ticker}")
            print(f"{ticker} added to Database!")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)
    
    return f"Updated data at: {today}"