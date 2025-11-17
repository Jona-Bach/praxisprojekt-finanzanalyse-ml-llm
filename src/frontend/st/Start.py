import streamlit as st
from pathlib import Path
import requests
import pandas as pd
from backend.database.db_functions import get_table_names, delete_table


# Ordner der aktuellen Datei (z.B. app.py)
BASE_DIR = Path(__file__).resolve().parent
st.session_state["BASE_DIR"] = BASE_DIR


# Pfad zur PNG
img_path_fsbar = BASE_DIR / "assets" / "finsightbar.png"
img_path_fsold = BASE_DIR / "assets" / "logofinsightold.png"






#__________________________Header____________________________

st.set_page_config(page_title="Start", page_icon="⚙️")
#____________________________________________________________

#__________________________SIDEBAR___________________________
st.sidebar.subheader("Welcome to FinSight!")
st.sidebar.image(str(img_path_fsbar))
st.sidebar.divider()
#____________________________________________________________


#__________________________PAGE______________________________
tab1, tab2, tab3 = st.tabs(["Welcome", "Setup", "Settings"])
st.title("")




#__________________________Welcome______________________________
with tab1:
    st.title("")
    st.image(str(img_path_fsold))
    st.title("")
    st.divider()


#__________________________Settings______________________________


with tab3:
    with st.expander("Data Settings"):
        st.header("Data Settings:")
        with st.expander("Clear Table"):
            database_path = "data/alphavantage.db"   # <--- anpassen falls nötig
            # Session-State für Reload
            if "reload_tables" not in st.session_state:
                st.session_state.reload_tables = True
            # Tabellen laden
            if st.session_state.reload_tables:
                df_tables = get_table_names(database_path)
                st.session_state.tables = df_tables["table_name"].tolist()
                st.session_state.reload_tables = False

            tables = st.session_state.tables

            # Kein Ergebnis?
            if len(tables) == 0:
                st.info("No table found")
                st.stop()

            # Tabelle auswählen
            choice = st.selectbox("Choose table to clear:", tables)

            @st.dialog("⚠️ Required!")
            def confirm_delete(table_name: str):
                st.error(f"Are you sure you want to clear **{table_name}**?")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Yes, clear", type="primary"):
                        msg = delete_table(database_path, table_name)
                        st.success(msg)
                        st.session_state["_refresh"] = True
                        st.rerun()

                with col2:
                    if st.button("Cancel"):
                        st.info("Cancelled")
                        st.rerun()

            if st.button("Clear Table"):
                confirm_delete(choice)

    with st.expander("Assistant Settings"):
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

        # 5. Modell auswählen

        #_____________________________________________________________________________

        def get_installed_models(base_url: str):
            try:
                res = requests.get(f"{base_url}/api/tags", timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    return [m["name"] for m in data.get("models", [])]
                return []
            except:
                return []


        # -------------------------
        # Helper: Modell-Pull
        # -------------------------
        def ensure_model(base_url: str, model: str, timeout: float = 120.0) -> bool:
            """Download (pull) an Ollama model, blocking until finished."""
            try:
                resp = requests.post(
                    f"{base_url}/api/pull",
                    json={"name": model, "stream": False},
                    timeout=timeout,
                )
                return resp.status_code in (200, 201)
            except Exception as e:
                st.error(f"Error pulling model '{model}': {e}")
                return False


        # -------------------------
        # UI
        # -------------------------

        BASE_URL = st.session_state.get("assistant_base_url", "http://host.docker.internal:11434")

        st.subheader("Assistant Model Management")
        st.caption("""
        You are able to change the Model which is used for the Assistant. Standard is phi3:mini.
        Larger models will have a much better outout but they will take longer to respond. You can
        see a list of potential models with their benefits in the Model list:
        """)

        with st.expander("Model list:"):
            df = pd.DataFrame({
            "Model": [
                "phi3:mini",
                "llama3",
                "llama3.2:3b",
                "mistral",
                "qwen2",
                "phi4",
                "codellama:7b",
            ],
            "Size (approx.)": [
                "3.8B parameters",
                "8B – 70B parameters",
                "3B parameters",
                "7B – 24B parameters",
                "up to 72B parameters",
                "3.8B parameters",
                "7B parameters",
            ],
            "Best for": [
                "Lightweight tasks, efficient local inference",
                "General-purpose LLM tasks, reasoning, chat",
                "Small, efficient model for low-resource environments",
                "Balanced performance, real-time agents, chat",
                "Large tasks, multilingual, coding, reasoning",
                "Efficient next-gen small LLM tasks",
                "Coding, software development, code generation",
            ]
            })

            st.dataframe(df, hide_index=True)

        # 1. Vorinstallierte Modelle holen
        installed_models = get_installed_models(BASE_URL)

        # 2. Vorschlagsmodelle (z. B. beliebte)
        suggested_models = [
            "phi3:mini",
            "llama3",
            "llama3.2:3b",
            "mistral",
            "qwen2",
            "phi4",
            "codellama:7b",
        ]

        # 3. Auswahl + Eingabe
        selected_model = st.selectbox(
            "Choose a model to manage:",
            options=suggested_models,
            key="model_choice",
        )

        custom_model = st.text_input("Or enter a custom model:", key="custom_model")

        # aktive Auswahl = custom first
        active_model = custom_model.strip() if custom_model.strip() else selected_model
        st.session_state["model"] = active_model

        st.write(f"Selected Model: **{active_model}**")

        # 4. Download-Button
        if st.button(f"⬇️ Download: {active_model}"):
            st.info(f"Downloading model '{active_model}', please wait...")
            ok = ensure_model(BASE_URL, active_model)
            if ok:
                st.success(f"Model '{active_model}' downloaded successfully!")
            else:
                st.error(f"Model '{active_model}' could not be downloaded.")


        # 5. Status anzeigen: installiert oder nicht
        installed_models = get_installed_models(BASE_URL)  # neu laden

        if active_model in installed_models:
            st.success(f"Model '{active_model}' is installed ✔")
        else:
            st.warning(f"Model '{active_model}' is NOT installed ❌")


