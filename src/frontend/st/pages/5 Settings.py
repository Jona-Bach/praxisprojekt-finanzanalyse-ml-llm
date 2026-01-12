import streamlit as st
from pathlib import Path
import requests
import pandas as pd
from backend.database.db_functions import get_table_names, delete_table, add_system_config, get_config_dict, delete_system_config, update_system_config, add_list_system_config, get_list_system_config, append_to_list_system_config, remove_from_list_system_config
from backend.llm_functions import check_connection
from backend.data_model import TICKERS
from backend.scheduler import load_initial_data
from backend.database.users_database import list_user_tables
from backend.database.database_utils import delete_any_table
import os

#__________________________Header____________________________

st.set_page_config(page_title="Settings", page_icon="⚙️")
#____________________________________________________________

# Ordner der aktuellen Datei (z.B. app.py)
BASE_DIR = Path(__file__).resolve().parent.parent
st.session_state["BASE_DIR"] = BASE_DIR

MODEL_DIR_PKL = "saved_models"
os.makedirs(MODEL_DIR_PKL, exist_ok=True)

# Pfad zur PNG
img_path_fsbar = BASE_DIR / "assets" / "finsightbar.png"
img_path_fsold = BASE_DIR / "assets" / "logofinsightold.png"

toggle_cfg_check = get_config_dict("toggle_button")
if toggle_cfg_check is None:
    add_system_config("toggle_button", "test", False)
else:
    pass

#__________________________SIDEBAR___________________________
st.sidebar.subheader("Settings")
#st.sidebar.image(str(img_path_fsbar))
st.sidebar.divider()
#____________________________________________________________

st.header("Settings")
st.divider()


with st.expander("Global Settings"):
    st.header("Global Settings:")
    toggle_cfg = get_config_dict("toggle_button")

    local_ollama_choice_toggle = st.toggle(
        "Local Ollama",
        value=toggle_cfg["Tag"]
    )
    if local_ollama_choice_toggle:
        update_system_config(name="toggle_button",tag=True)
        custom_url = st.text_input("Local Ollama (standard: http://localhost:11434", value="http://localhost:11434")
        st.caption("")
        status, message = check_connection(custom_url) 
        if status == True:
            st.success(message)
            st.session_state["assistant_base_url"] = custom_url
        if status == False:
            st.error(message)
        if st.button("Set Local Ollama as standard!"):
            try:
                ollama_standard_cfg = get_config_dict("LocalOllamaURL")
                if ollama_standard_cfg is not None:
                    if ollama_standard_cfg["Tag"] == True and ollama_standard_cfg["Name"] == "LocalOllamaURL":
                        st.error("Local Ollama already set to standard!")
                else:
                    add_system_config(name="LocalOllamaURL", value= custom_url, tag=True)
                    st.success(f"Set {custom_url} as standard!")
            except Exception as e:
                st.error(e)
    else:
        st.write("Local Ollama not used!")
        update_system_config(name="toggle_button",tag=False)
    if st.button("Reset Ollama Config!"):
            try:
                delete_system_config("LocalOllamaURL")
                st.info("Standard Ollama Config was deleted!")
                ollama_config_dic = None
            except Exception as e:
                st.error(e)










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

        tables_system = st.session_state.tables
        users_tables = list(list_user_tables())
        tables = tables_system + users_tables

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
                    try:
                        msg = delete_any_table(table_name=table_name, system_db_path=database_path)
                        st.success(f"{table_name} deleted!")
                        st.session_state["_refresh"] = True
                    except Exception as e:
                        st.error(str(e))

            with col2:
                if st.button("Cancel"):
                    st.info("Cancelled")
                    st.rerun()

        if st.button("Clear Table"):
            confirm_delete(choice)

    st.divider()
    st.subheader("Initial Tickers loading:")
    with st.container():
        st.caption("""Here you can see the selected tickers that are loaded in your Databse in the beginning.
                    You can change these settings here to load other tickers.""")
        col1, col2 = st.columns([1,1]) 
        with col1:
            if st.button("Load initial Data"):
                with st.spinner("Loading Initial Ticker Data"):
                    load_initial_data()
            st.divider()
            st.write("Create new initial Tickers list")
            system_tickers = sorted(TICKERS)
            initial_ticker_list = st.multiselect(
            "Choose from known Ticker",
            options=system_tickers)
            custom_initial_ticker = st.text_input("Add custom ticker (comma separated):")
            custom_tickers = [t.strip().upper() for t in custom_initial_ticker.split(",") if t.strip()]
            #all_tickers = initial_ticker_list + custom_tickers
            all_selected_tickers = list(set(initial_ticker_list + custom_tickers))
            df_own_tickers = pd.DataFrame(all_selected_tickers, columns=["Selected Initial Tickers"])
            st.dataframe(df_own_tickers, hide_index=True)
            if st.button("Choose as New Initial Tickers:"):
                if not all_selected_tickers:
                    st.error("No tickers selected! Please choose at least one ticker.")
                else:
                    try:
                        delete_system_config("Custom_Initial_Tickers")
                    except:
                        pass
                    add_list_system_config(name="Custom_Initial_Tickers",values=all_selected_tickers, tag=True)
                    st.success("Initial tickers successfully saved!")
            if st.button("Add to Initial Tickers"):
                append_to_list_system_config("Custom_Initial_Tickers", items=all_selected_tickers)
                st.success("Initial tickers successfully added!")

            if st.button("Remove Selected Ticker from Initial Tickers"):
                try:
                    remove_from_list_system_config("Custom_Initial_Tickers", items=all_selected_tickers)
                    st.success("Removed Ticker from Custom Ticker List")
                except:
                    st.error("Could not remove Ticker")


            if st.button("Delete Custom Initial Tickers:"):
                try:
                    delete_system_config("Custom_Initial_Tickers")
                    st.success("Deleted Initial Ticker config")
                except:
                    st.error("No Custom Initial tickers added!")

            st.divider()


        with col2:
            with st.expander("Initial Tickers List:"):
                custom_tickers_cfg = get_list_system_config("Custom_Initial_Tickers")
                if custom_tickers_cfg is not None:
                    custom_tickers_cfg_df = pd.DataFrame(custom_tickers_cfg, columns=["Custom Tickers List"])
                    st.dataframe(custom_tickers_cfg_df, hide_index=True)
                else:
                    df_initial_tickers = pd.DataFrame(TICKERS, columns=["System Ticker List"])
                    st.dataframe(df_initial_tickers, hide_index=True)


    st.divider()
    st.subheader("Analysis Settings")
    with st.container():
        st.caption("""Select the earliest Date that the download will use for the new Ticker download!""")

        picked_date = st.date_input("Choose a date")
        date_str = picked_date.strftime("%Y-%m-%d")

        selected_date_cfg = get_config_dict("selected_date_for_ticker_download")
        st.write("Selected date:", date_str)

        if selected_date_cfg and "Value" in selected_date_cfg:
            current_stored_date = selected_date_cfg["Value"]
            st.write("Current date:", current_stored_date)
        else:
            st.write("Current date: 2020-01-01")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save new Date!"):
                st.warning("You have changed the Date which is used for new ticker Downloads")
                delete_system_config("selected_date_for_ticker_download")
                add_system_config("selected_date_for_ticker_download", value=date_str, tag=False)
                st.success(f"{picked_date} was successfully added as new Date")
        with col2:
            if st.button("Reset Date Config"):
                try:
                    delete_system_config("selected_date_for_ticker_download")
                except:
                    st.error(f"Couln't delete the config! {e} ")
                st.success("Date Config Reseted!")





with st.expander("Machine Learning Settings"):
    st.header("Machine Learning Settings:")

    try:
        model_files = sorted(
            [f for f in os.listdir(MODEL_DIR_PKL) if f.endswith(".pkl")]
        )
    except FileNotFoundError:
        model_files = []

    if not model_files:
        st.info("Es wurden noch keine Modelle in `saved_models` gespeichert.")
    else:
        st.write("Folgende Modelle sind aktuell gespeichert:")

        for fname in model_files:
            path = os.path.join(MODEL_DIR_PKL, fname)

            # Dateiinfos (optional)
            try:
                size_kb = os.path.getsize(path) / 1024
                mtime = os.path.getmtime(path)
                from datetime import datetime
                saved_at = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                size_kb = None
                saved_at = "-"

            col_name, col_meta, col_del = st.columns([4, 3, 1])

            with col_name:
                st.markdown(f"**{fname}**")

            with col_meta:
                meta_text = []
                if size_kb is not None:
                    meta_text.append(f"{size_kb:.1f} KB")
                if saved_at != "-":
                    meta_text.append(f"gespeichert am {saved_at}")
                if meta_text:
                    st.caption(" • ".join(meta_text))

            with col_del:
                if st.button("🗑️ Löschen", key=f"del_{fname}"):
                    try:
                        os.remove(path)
                        st.success(f"`{fname}` wurde gelöscht.")
                        # Seite neu laden, damit die Liste aktuell ist
                        st.rerun()
                    except Exception as e:
                        st.error(f"Konnte `{fname}` nicht löschen: {e}")
        
    st.divider()
    def render_ml_row_settings():
            st.subheader("Machine Learning – Zeilen-Limits")

            st.caption("Hier kannst du minimale und maximale Zeilenanzahl für das ML-Training definieren.")

            # Aktuell gespeicherte Werte laden (falls vorhanden)
            min_cfg = get_config_dict("ml_min_rows_for_model")
            max_cfg = get_config_dict("ml_max_rows_for_model")

            if min_cfg and "Value" in min_cfg:
                current_min = int(min_cfg["Value"])
            else:
                current_min = 50  # Default wie im Playground

            if max_cfg and "Value" in max_cfg:
                current_max = int(max_cfg["Value"])
            else:
                current_max = 20000  # Default wie im Playground

            st.write(f"Aktueller Minimalwert: **{current_min}** Zeilen")
            st.write(f"Aktueller Maximalwert: **{current_max}** Zeilen")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                min_rows_input = st.number_input(
                    "Neue minimale Zeilenanzahl für ML",
                    min_value=1,
                    max_value=1_000_000,
                    value=current_min,
                    step=10,
                    help="Unterhalb dieser Zeilenanzahl wird kein Modell trainiert."
                )

            with col2:
                max_rows_input = st.number_input(
                    "Neue maximale Trainingszeilen",
                    min_value=min_rows_input,
                    max_value=5_000_000,
                    value=current_max,
                    step=100,
                    help="Oberhalb dieser Zeilenanzahl werden die Daten gekappt."
                )

            st.markdown("---")
            c1, c2 = st.columns(2)

            with c1:
                if st.button("💾 ML-Zeilen-Limits speichern"):
                    # Alte Configs löschen (falls vorhanden)
                    delete_system_config("ml_min_rows_for_model")
                    delete_system_config("ml_max_rows_for_model")

                    # Neue Werte speichern
                    add_system_config("ml_min_rows_for_model", value=str(min_rows_input), tag=False)
                    add_system_config("ml_max_rows_for_model", value=str(max_rows_input), tag=False)

                    st.success(
                        f"Neue Limits gespeichert: min = {min_rows_input} Zeilen, "
                        f"max = {max_rows_input} Zeilen."
                    )

            with c2:
                if st.button("🔄 ML-Zeilen-Limits zurücksetzen"):
                    try:
                        delete_system_config("ml_min_rows_for_model")
                    except Exception as e:
                        st.warning(f"Konnte 'ml_min_rows_for_model' nicht löschen: {e}")

                    try:
                        delete_system_config("ml_max_rows_for_model")
                    except Exception as e:
                        st.warning(f"Konnte 'ml_max_rows_for_model' nicht löschen: {e}")

                    st.success("ML-Zeilen-Limits wurden auf Defaults zurückgesetzt (50 / 20000).")
    render_ml_row_settings()






with st.expander("Assistant Settings"):
    st.header("Assistant Settings:")

    # 1. Default nur EINMAL setzen
    ollama_config_dic = get_config_dict("LocalOllamaURL")
    if ollama_config_dic is not None and ollama_config_dic["Tag"] == True:
        st.session_state["assistant_base_url"] = ollama_config_dic["Value"]
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
    if ollama_config_dic is not None:
        if st.session_state["assistant_base_url"] == ollama_config_dic["Value"]:
            if st.button("Reset Local Ollama Config"):
                try:
                    delete_system_config("LocalOllamaURL")
                    st.info("Standard Ollama Config was deleted!")
                    ollama_config_dic = None
                except Exception as e:
                    st.error(e)

    elif toggle_cfg["Tag"] == True:
        st.warning("Local Ollama is activated!")

    else:
        
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
            "llama3.1:8b",
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
    suggested_models = {
        "phi3:mini" : 0,
        "llama3.1:8b" : 1,
        "llama3.2:3b":2,
        "mistral":3,
        "qwen2":4,
        "phi4":5,
        "codellama:7b" : 6,
    }

    saved_idx = get_config_dict("assistant_model_choice_index")
    if saved_idx is not None:
        idx = int(saved_idx["Value"])
    else:
        idx = 0

    # 3. Auswahl + Eingabe
    selected_model = st.selectbox(
        "Choose a model to manage:",
        options=suggested_models.keys(),
        #key="assistant_model_choice_selected",
        index=idx
    )

    custom_model = st.text_input("Or enter a custom model:", key="custom_model")

    if custom_model.strip():
        active_model = custom_model.strip()
    elif selected_model:
        active_model = selected_model
        delete_system_config("assistant_model_choice_index")
        index_new = str(suggested_models[selected_model])
        add_system_config(name="assistant_model_choice_index", value=index_new, tag=False)
    else:
        active_model = "phi3:mini"


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


