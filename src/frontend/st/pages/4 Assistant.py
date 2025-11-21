import streamlit as st
import requests
from pathlib import Path

if "BASE_DIR" in st.session_state:
    BASE_DIR = st.session_state["BASE_DIR"]
    img_path_fsbar = BASE_DIR / "assets" / "finsightbar.png"
    img_path_fsold = BASE_DIR / "assets" / "logofinsightold.png"
    assistant_info = BASE_DIR / "assets" / "assistantinfos.txt"
else:
    BASE_DIR = Path(__file__).resolve().parent
    img_path_fsbar = BASE_DIR / "assets_safety" / "finsightbar.png"
    img_path_fsold = BASE_DIR / "assets_safety" / "logofinsightold.png"

if "model" in st.session_state:
    model = st.session_state["model"]
else:
    model = "phi3:mini"


#__________________________Header____________________________

st.set_page_config(page_title="Digital Assistant", page_icon="💬")
#____________________________________________________________

#__________________________SIDEBAR___________________________
st.sidebar.subheader("Digital Assistant")
st.sidebar.image(str(img_path_fsbar))
st.sidebar.divider()
if st.sidebar.button("Chat zurücksetzen"):
    st.session_state.messages = []
#____________________________________________________________



# Chech Connection function__________________________________________
def check_connection(base_url: str, timeout: float = 3.0) -> tuple[bool, str]:
    """
    Checks if ollama is reachable
    Uses GET /api/version (easy, withoutj Model).
    """
    try:
        r = requests.get(f"{base_url}/api/version", timeout=timeout)
        if r.ok:
            return True, f"Connected with Ollama @ {base_url} (Version: {r.json().get('version', 'unbekannt')})"
        return False, f"No answer from {base_url} (Status {r.status_code})"
    except Exception as e:
        return False, f"No connection to {base_url}!"


#__________________________PAGE______________________________

st.title("🤖 Digital Assistant")
st.caption("""
This is your personal digital assistant. You can ask him questions regarding this application
if you need help. Please be aware that the answer might take a while and that you need to have a connection, to either the Ollama Container
or you own Ollama. You can see the status below:
""")

if "assistant_base_url" in st.session_state:
    base_url = st.session_state["assistant_base_url"]
else:
     base_url = "http://host.docker.internal:11434"
     # base_url = "http://localhost:11434" Vielleicht ändern wenn man Container nicht nutzt
ok, msg = check_connection(base_url)
if ok:
    st.success(msg)
else:
    st.error(msg)

st.caption("""
If you don't have a connection, you can go to the settings and change the connection to the Container Ollama version (standard: local Ollama is selected)
otherwise please reread the "Setup" Guide in the Start Menu! You can also change your Model in the settings. Larger models will give better output but will take longer to respond!
""")

st.write(f"Current model: {model}. (You can change this in the settings)")
st.divider()


# Chatbot_______________________________________________________
if "messages" not in st.session_state:
    st.session_state.messages = []
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def bot_answer(base_url: str, model: str, prompt: str, timeout: float = 120.0) -> str:
    with open(str(assistant_info)) as file:
        infos = file.read()

        new_prompt = f"""
        You are an assistant who answers strictly and only based on the INFORMATION below.

        INFORMATION:
        {infos}

        RULES:
        - Answer the question **only** using the INFORMATION above. 
        - Do NOT add any extra details, explanations, assumptions, or background stories.
        - Keep answers extremely short **max. 1–2 sentences**.
        - Do NOT invent facts. Do NOT speculate. Do NOT add context.
        - Keep the tone neutral and concise.

        QUESTION:
        {prompt}
        """
    try:
        r = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": new_prompt, "stream": False},
            timeout=timeout,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("response", "")
    except:
        return ("""This did not work. Please make sure you have a valid connection and the modell installed!
        Please read the Setup Guide if you unsure or check the settings""")

if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    antwort = bot_answer(base_url= base_url, model = model, prompt=prompt)

    st.session_state.messages.append({"role": "Assistant", "content": antwort})
    with st.chat_message("Assistant"):
        st.markdown(antwort)
#___________________________________________________________________________________


