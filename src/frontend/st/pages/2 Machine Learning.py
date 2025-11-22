import streamlit as st
from backend.data_processing.alphavantage_processed import process_alphavantage_raw_db

#__________________________Header____________________________

st.set_page_config(page_title="Machine Learning", page_icon="📈")
#____________________________________________________________

st.write("DEBUG use_local_ollama:", st.session_state.get("use_local_ollama_toggle", "nicht gesetzt"))

#st.write(st.session_state["local_ollama_toggle"])

if "assistant_base_url" in st.session_state:
    base_url = st.session_state["assistant_base_url"]
    st.write(base_url)

if "test" in st.session_state:
    base_url = st.session_state["test"]
    st.write(base_url)

if st.button("Press me"):
    process_alphavantage_raw_db()