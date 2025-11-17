import streamlit as st
from pathlib import Path
from backend.scheduler import load_data
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
#____________________________________________________________

if st.button("Load Data"):
    with st.spinner("Updating data (this might take a while...)"):
        answer = load_data()
    st.success(answer)