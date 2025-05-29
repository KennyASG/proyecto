# main.py

from dotenv import load_dotenv
load_dotenv()  # carga HOTWORD, WEATHER_API_KEY, GENAI_API_KEY, GENAI_MODEL...

from voice_assistant.audio_io.recognizer import VoiceRecognizer
from voice_assistant.audio_io.synthesizer import VoiceSynthesizer
from voice_assistant.action.registry import ActionRegistry
from voice_assistant.intent.nlu import IntentParser

def main():
    # Inicializa componentes
    vr = VoiceRecognizer()
    vs = VoiceSynthesizer()
    registry = ActionRegistry()
    nlu = IntentParser(registry)

    vs.speak("Asistente iniciado y listo")

    while True:
        # Espera la hotword
        if vr.listen_for_hotword():
            vs.speak("Te escucho")
            comando = vr.listen_command()

            if not comando:
                vs.speak("No entendí, inténtalo de nuevo")
                continue

            # NLP: elige acción + parámetros
            intent, params = nlu.parse(comando)
            action = registry.get_action(intent)

            if not action:
                vs.speak(f"No conozco la acción «{intent}»")
                continue

            vs.speak("Procesando tu solicitud")
            respuesta = action.execute(params)
            vs.speak(respuesta)

if __name__ == "__main__":
    main()
