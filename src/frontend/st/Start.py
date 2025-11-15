import streamlit as st

#__________________________Header____________________________

st.set_page_config(page_title="Welcome", page_icon="👋")
#____________________________________________________________

#__________________________SIDEBAR___________________________
st.sidebar.subheader("Welcome to FinSight!")
st.sidebar.image("./assets/finsightbar.png")
st.sidebar.divider()
#____________________________________________________________


#__________________________PAGE______________________________
tab1, tab2, tab3 = st.tabs(["Welcome", "Setup", "Settings"])
st.title("")




#__________________________Welcome______________________________
with tab1:
    st.image("./assets/logofinsightold.png")


#__________________________Settings______________________________

st.divider()
st.header("Assistant Settings:")

# 1. Default nur EINMAL setzen
if "assistant_base_url" not in st.session_state:
    st.session_state["assistant_base_url"] = "http://host.docker.internal:11434"

# 2. Mapping von Option → URL
options = ["Local Ollama", "Ollama Container"]
url_map = {
    "Local Ollama": "http://host.docker.internal:11434",
    "Ollama Container": "http://ollama:11434",
}

# 3. aktuelle Auswahl aus session_state ableiten
current_url = st.session_state["assistant_base_url"]
if current_url == url_map["Local Ollama"]:
    default_index = 0
else:
    default_index = 1

assistant_llm_choice = st.radio(   
    "Change Source:",
    options=options,
    key="assistant_llm_choice",
    index=default_index,        
    horizontal=True,
)

# 4. Auswahl ins session_state schreiben
st.session_state["assistant_base_url"] = url_map[assistant_llm_choice]

st.info(f"Current LLM Source: {st.session_state['assistant_base_url']}")
