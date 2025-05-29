# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Palabra clave para activar el asistente
HOTWORD = os.getenv("HOTWORD", "hola").lower()

# Configuración de micrófono
LISTEN_TIMEOUT = float(os.getenv("LISTEN_TIMEOUT", 5.0))
PHRASE_TIME_LIMIT = float(os.getenv("PHRASE_TIME_LIMIT", 7.0))
