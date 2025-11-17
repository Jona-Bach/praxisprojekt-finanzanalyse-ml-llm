import streamlit as st
from pathlib import Path
from backend.scheduler import load_data
from backend.database.db_functions import get_table, get_table_names
# Ordner der aktuellen Datei (z.B. app.py)
BASE_DIR = Path(__file__).resolve().parent

# Pfad zur PNG
img_path_fsbar = BASE_DIR.parent / "assets" / "finsightbar.png"
#__________________________Header____________________________

st.set_page_config(page_title="Data", page_icon="🔍")
#____________________________________________________________

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
        answer = load_data()
        st.success(answer)
#____________________________________________________________

st.header("Alphavantage RAW-Data Table")
df = get_table("alphavantage_raw_kpi")
st.dataframe(df, hide_index=True)

st.header("Alphavantage PRICING Table")
df = get_table("alphavantage_daily_pricing")
st.dataframe(df, hide_index= True)

if st.button("All Tables"):
    df = get_table_names("data/alphavantage.db")
    tables = get_table_names("data/alphavantage.db")  # returns list

    choice = st.radio("Tabellen:", tables)

    if choice:
        st.dataframe(get_table(choice))

if st.button("Delete Data"):
    st.warning("Are you sure you want to do this?")
    
    with st.expander("Confirm action"):
        if st.button("Yes, do it!"):
            st.success("Action executed!")
        if st.button("Cancel"):
            st.info("Canceled.")

