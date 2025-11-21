import os
import time
import requests
import streamlit as st


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
