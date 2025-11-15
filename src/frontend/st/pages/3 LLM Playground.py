# file: src/backend/launch.py
import os
import time
import requests
import streamlit as st

#__________________________Header____________________________

st.set_page_config(page_title="LLM Playground", page_icon="🤖")
#____________________________________________________________

# -----------------------------
# Hilfsfunktionen
# -----------------------------
def base_url_from_choice(choice: str, custom: str | None = None) -> str:
    """
    Mappt die UI-Auswahl auf eine Base-URL.
    - 'Container'  -> http://ollama:11434  (dein Ollama-Service in docker-compose)
    - 'Host'       -> http://host.docker.internal:11434  (macOS/Windows; auf Linux nach extra_hosts)
    - 'Benutzerdefiniert' -> custom
    """
    if choice == "Container":
        return "http://ollama:11434"
    if choice == "Host":
        return "http://host.docker.internal:11434"
    if choice == "Benutzerdefiniert" and custom:
        return custom.strip().rstrip("/")
    # Fallback: ENV-Variable OLLAMA_HOST oder localhost
    return os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def check_connection(base_url: str, timeout: float = 3.0) -> tuple[bool, str]:
    """
    Prüft, ob Ollama am base_url erreichbar ist.
    Nutzt GET /api/version (schnell, ohne Model).
    """
    try:
        r = requests.get(f"{base_url}/api/version", timeout=timeout)
        if r.ok:
            return True, f"Verbunden mit Ollama @ {base_url} (Version: {r.json().get('version', 'unbekannt')})"
        return False, f"Keine OK-Antwort von {base_url} (Status {r.status_code})"
    except Exception as e:
        return False, f"Keine Verbindung zu {base_url}: {e}"


def ensure_model(base_url: str, model: str, timeout: float = 120.0) -> None:
    """
    Optionaler Komfort: sorgt dafür, dass ein Modell vorhanden ist.
    POST /api/pull mit stream=False wartet, bis der Pull abgeschlossen ist.
    Wir fangen Fehler nur ab und zeigen sie in der UI an.
    """
    try:
        resp = requests.post(
            f"{base_url}/api/pull",
            json={"name": model, "stream": False},
            timeout=timeout,
        )
        # Erfolgreich ist ok (201/200 je nach Version). Bei 400/404 kommt
        # u.U. eine Meldung "model already exists" o.ä. – ignorieren wir still.
    except Exception as e:
        st.info(f"Modell '{model}' konnte nicht automatisch geladen werden: {e}")


def generate_once(base_url: str, model: str, prompt: str, timeout: float = 120.0) -> str:
    """
    Einmalige Textgenerierung (keine Streaming-Antwort).
    """
    r = requests.post(
        f"{base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=timeout,
    )
    r.raise_for_status()
    data = r.json()
    return data.get("response", "")


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🤖 Ollama aus dem Container oder lokal auf dem Host nutzen")

st.caption("""
Wähle, ob das Dashboard den **Ollama-Container** (`http://ollama:11434`) oder dein
**lokales Ollama** auf dem **Host** (`http://host.docker.internal:11434`) verwenden soll.
Auf **Linux** bitte ggf. `extra_hosts` in docker-compose ergänzen (siehe Anleitung).
""")

# Auswahl des Backends
choice = st.radio(
    "Quelle wählen:",
    options=["Container", "Host", "Benutzerdefiniert"],
    index=0,
    horizontal=True,
)

custom_url = None
if choice == "Benutzerdefiniert":
    custom_url = st.text_input("Eigene Ollama-URL (z. B. http://192.168.1.10:11434):", value="http://localhost:11434")

base_url = base_url_from_choice(choice, custom_url)
st.write(f"Aktuelle Ziel-URL: `{base_url}`")

# Test-Button für Verbindung
if st.button("🔌 Verbindung testen"):
    ok, msg = check_connection(base_url)
    if ok:
        st.success(msg)
    else:
        st.error(msg)

# Prompt & Modell
st.divider()
model = st.text_input("Modellname:", value="phi3:mini")
prompt = st.text_area("Prompt:", value="Hello, how are you?")

col_a, col_b = st.columns(2)
with col_a:
    auto_pull = st.toggle("Modell automatisch laden, falls nötig", value=True, help="Versucht /api/pull, wenn das Modell fehlt.")
with col_b:
    timeout_s = st.number_input("Timeout (Sekunden)", min_value=5, max_value=600, value=120)

# Generieren
if st.button("🪄 Generieren"):
    # 1) Verbindung prüfen
    ok, msg = check_connection(base_url)
    if not ok:
        st.error(f"Kann nicht verbinden: {msg}")
    else:
        st.success(msg)
        # 2) Optional: Modell laden
        if auto_pull:
            with st.status(f"Lade/prüfe Modell '{model}'…", expanded=False) as status:
                ensure_model(base_url, model, timeout=timeout_s)
                status.update(label=f"Modell '{model}' bereit (oder bereits vorhanden).", state="complete", expanded=False)

        # 3) Generieren
        with st.status("Erzeuge Antwort…", expanded=False):
            try:
                t0 = time.time()
                text = generate_once(base_url, model, prompt, timeout=timeout_s)
                dt = time.time() - t0
                st.success(f"Antwort in {dt:.2f}s")
                st.code(text)
            except requests.HTTPError as http_err:
                # Häufiger Fall: Modell nicht vorhanden und auto_pull=False
                st.error(f"HTTP-Fehler: {http_err.response.status_code} – {http_err.response.text}")
            except Exception as e:
                st.error(f"Fehler bei der Generierung: {e}")