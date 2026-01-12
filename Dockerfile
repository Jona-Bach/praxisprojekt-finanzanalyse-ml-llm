# Laufzeit-Image für deine App
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Dependencies separat für besseren Cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 2. Code kopieren
COPY . /app

# 3. Startbefehl (an deine Struktur angepasst)
#CMD ["python3", "src/backend/launch.py"]

#CMD ["streamlit", "run", "src/main/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
#docker build -t praxisprojekt:latest .
#docker build -t praxisprojekt:latest .