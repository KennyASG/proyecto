# voice_assistant/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# 1) Señala explícitamente el .env que está en la raíz del proyecto
#    (__file__ es voice_assistant/config.py → ../.env)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# 2) Variables de hotword y audio
HOTWORD = os.getenv("HOTWORD", "hola voiceai").lower()
LISTEN_TIMEOUT = float(os.getenv("LISTEN_TIMEOUT", 5))
PHRASE_TIME_LIMIT = float(os.getenv("PHRASE_TIME_LIMIT", 7))

# 3) Claves de servicios externos
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

GENAI_API_KEY  = os.getenv("GENAI_API_KEY")
GENAI_BASE_URL = os.getenv("GENAI_BASE_URL")
GENAI_MODEL    = os.getenv("GENAI_MODEL")

# 4) Credenciales SMTP para correo
SMTP_SERVER   = os.getenv("SMTP_SERVER")
SMTP_PORT     = int(os.getenv("SMTP_PORT", 587))
SMTP_USER     = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
