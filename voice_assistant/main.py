# main.py

from dotenv import load_dotenv

load_dotenv()

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

            # Detectar contexto para mejor reconocimiento
            context_hint = None
            pre_command = vr.listen_command()

            if not pre_command:
                vs.speak("No entendí, inténtalo de nuevo")
                continue

            # Si detectamos intención de email, usar modo especial
            if "correo" in pre_command.lower():
                context_hint = "email"
                comando = pre_command

                # Si el email parece mal reconocido, ofrecer deletreo
                if "correo a" in comando.lower():
                    email_part = comando.lower().split("correo a")[1].split("asunto")[0].strip()
                    if " " in email_part and "@" not in email_part:
                        vs.speak(
                            "Parece que no reconocí bien el email. ¿Quieres deletrearlo letra por letra? Di sí o no")
                        respuesta = vr.listen_command()
                        if respuesta and "sí" in respuesta.lower():
                            vs.speak("Deletrea el email completo")
                            email_deletreado = vr.listen_email_spelling()
                            if email_deletreado:
                                # Reemplazar la parte del email en el comando original
                                comando = comando.replace(email_part, email_deletreado)
                                vs.speak(f"Perfecto, enviaré correo a {email_deletreado}")
            else:
                comando = pre_command

            # NLP: elige acción + parámetros
            intent, params = nlu.parse(comando)
            action = registry.get_action(intent)

            if not action:
                vs.speak(f"No conozco la acción «{intent}»")
                continue

            # Para emails, confirmar antes de enviar
            if intent == "send_email":
                email_to = params.get("to", "")
                subject = params.get("subject", "Sin asunto")

                vs.speak(f"¿Confirmas enviar correo a {email_to} con asunto {subject}?")
                confirmacion = vr.listen_command()

                if not confirmacion or "sí" not in confirmacion.lower():
                    vs.speak("Correo cancelado")
                    continue

            vs.speak("Procesando tu solicitud")
            respuesta = action.execute(params)
            vs.speak(respuesta)


if __name__ == "__main__":
    main()