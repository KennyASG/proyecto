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

    def listen_command(self, context_hint: str = None) -> str:
        """Después de detectar hotword, captura un comando de voz y lo convierte a texto."""
        with self.microphone as source:
            print(f"[Recognizer] Dime tu comando...")
            # Aumentar timeout para comandos largos como emails
            timeout = LISTEN_TIMEOUT + 5 if context_hint == "email" else LISTEN_TIMEOUT
            phrase_limit = PHRASE_TIME_LIMIT + 3 if context_hint == "email" else PHRASE_TIME_LIMIT

            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

        try:
            # Intentar con diferentes configuraciones para mejor precisión
            command = self._recognize_with_fallback(audio)
            print(f"[Recognizer] Comando reconocido: {command}")
            return command
        except sr.UnknownValueError:
            print("[Recognizer] No entendí el comando")
            return ""
        except sr.RequestError as e:
            print(f"[Recognizer] Error de API: {e}")
            return ""

    def _recognize_with_fallback(self, audio) -> str:
        """Intenta reconocer con diferentes configuraciones"""

        # Primer intento: configuración estándar
        try:
            return self.recognizer.recognize_google(audio, language="es-ES")
        except:
            pass

        # Segundo intento: con hints para emails
        try:
            return self.recognizer.recognize_google(
                audio,
                language="es-ES",
                show_all=False
            )
        except:
            pass

        # Tercer intento: en inglés para emails
        try:
            result_en = self.recognizer.recognize_google(audio, language="en-US")
            # Si parece contener un email, usar el resultado en inglés
            if "@" in result_en or "gmail" in result_en.lower() or "hotmail" in result_en.lower():
                return result_en
        except:
            pass

        # Si todo falla, levantar excepción
        raise sr.UnknownValueError()

    def listen_email_spelling(self) -> str:
        """Modo especial para deletrear emails letra por letra"""
        with self.microphone as source:
            print("[Recognizer] Deletrea el email letra por letra...")
            audio = self.recognizer.listen(source, timeout=30, phrase_time_limit=20)

        try:
            spelled_text = self.recognizer.recognize_google(audio, language="es-ES")
            print(f"[Recognizer] Deletreado: {spelled_text}")
            return self._convert_spelled_to_email(spelled_text)
        except:
            return ""

    def _convert_spelled_to_email(self, spelled_text: str) -> str:
        """Convierte texto deletreado a email"""
        # Mapeo de letras habladas a caracteres
        letter_map = {
            'a': 'a', 'be': 'b', 'ce': 'c', 'de': 'd', 'e': 'e',
            'efe': 'f', 'ge': 'g', 'ache': 'h', 'i': 'i', 'jota': 'j',
            'ka': 'k', 'ele': 'l', 'eme': 'm', 'ene': 'n', 'eñe': 'ñ',
            'o': 'o', 'pe': 'p', 'cu': 'q', 'erre': 'r', 'ese': 's',
            'te': 't', 'u': 'u', 've': 'v', 'doble ve': 'w', 'equis': 'x',
            'ye': 'y', 'zeta': 'z', 'arroba': '@', 'punto': '.'
        }

        words = spelled_text.lower().split()
        result = ""

        for word in words:
            if word in letter_map:
                result += letter_map[word]
            elif word.isdigit():
                result += word
            else:
                result += word

        return result