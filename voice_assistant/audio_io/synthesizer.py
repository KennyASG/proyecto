# audio_io/synthesizer.py
import platform
import subprocess

# Intentamos importar pyttsx3 para plataformas que lo soporten
try:
    import pyttsx3
    HAS_PYTTX = True
except ImportError:
    HAS_PYTTX = False

class VoiceSynthesizer:
    def __init__(self, rate: int = 150, volume: float = 1.0, lang: str = 'es'):
        self.rate = rate
        self.volume = volume
        self.lang = lang
        if platform.system() != 'Darwin' and HAS_PYTTX:
            # Configuración pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            # Seleccionar voz en español si existe
            for v in self.engine.getProperty('voices'):
                if 'spanish' in v.name.lower():
                    self.engine.setProperty('voice', v.id)
                    break
            print(f"[Synthesizer] pyttsx3 configurado: rate={rate}, volume={volume}")
        else:
            # En macOS usamos el comando 'say'
            print("[Synthesizer] Usando macOS 'say' para síntesis de voz")

    def speak(self, text: str):
        """Sintetiza el texto en voz."""
        if not text:
            return
        print(f"[Synthesizer] Diciendo: {text}")
        if platform.system() == 'Darwin':
            # Usar herramienta nativa 'say'
            subprocess.run(['say', text])
        elif HAS_PYTTX:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            # Fallback si no hay motor disponible
            print(f"[Synthesizer] No hay motor de síntesis disponible para: {text}")
