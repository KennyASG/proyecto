# audio_io/synthesizer.py

import platform
import subprocess
import re

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
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            for v in self.engine.getProperty('voices'):
                if 'spanish' in v.name.lower():
                    self.engine.setProperty('voice', v.id)
                    break
        else:
            # macOS usará `say`
            pass

    def speak(self, text: str):
        if not text:
            return

        # Fragmenta por oraciones para evitar cortes
        parts = re.split(r'(?<=[\.\?\!])\s+', text)
        for sentence in parts:
            if not sentence.strip():
                continue
            print(f"[Synthesizer] Diciendo: {sentence}")
            if platform.system() == 'Darwin':
                subprocess.run(['say', sentence])
            elif HAS_PYTTX:
                self.engine.say(sentence)
                self.engine.runAndWait()
            else:
                print(sentence)
