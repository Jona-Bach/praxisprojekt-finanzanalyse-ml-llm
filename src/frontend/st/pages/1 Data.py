import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
from datetime import datetime
from backend.data_model import TICKERS
from backend.scheduler import load_data, load_initial_data
from backend.database.db_functions import get_table, get_table_names, get_symbols_from_table, get_unique_table
from backend.data_processing.alphavantage_processed import get_processed_table
# Ordner der aktuellen Datei (z.B. app.py)
BASE_DIR = Path(__file__).resolve().parent

# Pfad zur PNG
img_path_fsbar = BASE_DIR.parent / "assets" / "finsightbar.png"
#__________________________Header____________________________

st.set_page_config(page_title="Data", page_icon="🔍")
#____________________________________________________________

tab1, tab2 = st.tabs(["Data Settings", "Analysis"])


#__________________________SIDEBAR___________________________
st.sidebar.subheader("Welcome to FinSight!")
st.sidebar.image(str(img_path_fsbar))
st.sidebar.divider()

if "load_data_time" in st.session_state:
    loaded_data_ts = st.session_state["load_data_time"]
else:
    st.session_state["load_data_time"] = "NOT NOW"
    loaded_data_ts = st.session_state["load_data_time"]

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


t_choice = st.sidebar.multiselect(
    "Choose Ticker",
    options=sorted(TICKERS))

st.session_state["chosen_tickers"] = t_choice

if st.sidebar.button("Download Ticker Data"):
    with st.spinner("Downloading data (this might take a while...)"):
        answer = load_data(t_choice)
        st.success(answer)
    st.success("Download Complete!")



#___________________________Data Tab_________________________________

with tab1:
    st.header("Alphavantage RAW-Data Table")
    df = get_table("alphavantage_raw_kpi")
    st.dataframe(df, hide_index=True)

    st.header("Alphavantage PRICING Table")
    df = get_table("alphavantage_daily_pricing")
    st.dataframe(df, hide_index= True)

    st.header("Alphavantage Processed Data Table")
    df = get_processed_table("alphavantage_processed_kpi")
    st.dataframe(df, hide_index=True)

    st.header("Alphavantage Processed PRICING Table")
    df = get_processed_table("alphavantage_pricing_processed")
    st.dataframe(df, hide_index= True)


with tab2:
    st.header("📊 Market Analysis")

    # ---------------------------
    # 1. Pricing-Daten laden
    # ---------------------------
    df_pricing = get_processed_table("alphavantage_pricing_processed")

    # Datentyp korrigieren
    df_pricing["date"] = pd.to_datetime(df_pricing["date"])
    df_pricing = df_pricing.sort_values(["symbol", "date"])

    symbols = sorted(df_pricing["symbol"].unique())

    st.subheader("Choose Symbol")
    chosen_symbol = st.selectbox("Select a ticker for analysis:", symbols)

    # ---------------------------
    # 2. Preis-Daten für Symbol
    # ---------------------------
    df_symbol = df_pricing[df_pricing["symbol"] == chosen_symbol]

    st.write(f"### Price Data for **{chosen_symbol}**")
    st.dataframe(df_symbol, hide_index=True)

    # ---------------------------
    # 3. Plotly Preis-Chart
    # ---------------------------
    import plotly.express as px

    fig_price = px.line(
        df_symbol,
        x="date",
        y="close",
        title=f"{chosen_symbol} – Close Price over Time",
        markers=True,
    )
    st.plotly_chart(fig_price, width="stretch")

    # Optional: Mehrere Datenlinien (Open/High/Low/Close)
    with st.expander("More Price Charts"):
        fig_multi = px.line(
            df_symbol,
            x="date",
            y=["open", "high", "low", "close"],
            title=f"{chosen_symbol} – OHLC Price Overview",
        )
        st.plotly_chart(fig_multi, width="stretch")

    st.divider()

    # ---------------------------
    # 4. Korrelationsanalyse
    # ---------------------------
    st.header("📈 Correlation Analysis")

    selected_corr_symbols = st.multiselect(
        "Choose symbols for correlation analysis",
        symbols,
        default=symbols[:5]  # erste 5 als Vorschlag
    )

    if len(selected_corr_symbols) >= 2:
        df_corr = df_pricing[df_pricing["symbol"].isin(selected_corr_symbols)]

        # Pivot: Zeilen = Date, Spalten = Symbol, Werte = Close
        df_pivot = df_corr.pivot(index="date", columns="symbol", values="close").dropna()

        # Daily returns
        df_returns = df_pivot.pct_change().dropna()

        corr_matrix = df_returns.corr()

        st.write("### Correlation Matrix (Daily Returns)")
        st.dataframe(corr_matrix, hide_index=True)

        # Plotly Heatmap
        import plotly.figure_factory as ff
        fig_corr = ff.create_annotated_heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.index.tolist(),
            colorscale="Blues",
            showscale=True,
        )
        st.plotly_chart(fig_corr, width="stretch")
    else:
        st.info("Please choose at least two symbols for correlation analysis.")