# main.py
from audio_io.recognizer import VoiceRecognizer
from audio_io.synthesizer import VoiceSynthesizer

def main():
    vr = VoiceRecognizer()
    vs = VoiceSynthesizer()

    vs.speak("Asistente iniciado y listo")

    while True:
        if vr.listen_for_hotword():
            vs.speak("Te escucho")
            comando = vr.listen_command()
            if comando:
                # Por ahora, solo repetimos lo que dijo
                vs.speak(f"Dijiste: {comando}")
            else:
                vs.speak("No entendí nada, inténtalo de nuevo")

if __name__ == "__main__":
    main()
