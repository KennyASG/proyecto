# audio_io/recognizer.py
import speech_recognition as sr
from ..config import HOTWORD, LISTEN_TIMEOUT, PHRASE_TIME_LIMIT

class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        # Ajuste inicial de ruido
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[Recognizer] Ajustado para ruido de ambiente")

    def listen_for_hotword(self) -> bool:
        """Escucha durante LISTEN_TIMEOUT y devuelve True si se detecta la hotword."""
        with self.microphone as source:
            print(f"[Recognizer] Escuchando hotword por {LISTEN_TIMEOUT}s...")
            try:
                audio = self.recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)
                text = self.recognizer.recognize_google(audio, language="es-ES").lower()
                print(f"[Recognizer] Interpretado: {text}")
                return HOTWORD in text
            except sr.WaitTimeoutError:
                return False
            except sr.UnknownValueError:
                return False
            except sr.RequestError as e:
                print(f"[Recognizer] Error de API: {e}")
                return False

    def listen_command(self) -> str:
        """Después de detectar hotword, captura un comando de voz y lo convierte a texto."""
        with self.microphone as source:
            print(f"[Recognizer] Dime tu comando...")
            audio = self.recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_TIME_LIMIT)
        try:
            command = self.recognizer.recognize_google(audio, language="es-ES")
            print(f"[Recognizer] Comando reconocido: {command}")
            return command
        except sr.UnknownValueError:
            print("[Recognizer] No entendí el comando")
            return ""
        except sr.RequestError as e:
            print(f"[Recognizer] Error de API: {e}")
            return ""
