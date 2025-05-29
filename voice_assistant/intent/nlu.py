# voice_assistant/intent/nlu.py

class IntentParser:
    def __init__(self, action_registry):
        self.registry = action_registry

    def parse(self, text: str):
        text_lower = text.lower()

        # Clima
        if "clima" in text_lower:
            parts = text_lower.split()
            if "en" in parts:
                idx = parts.index("en")
                location = parts[idx + 1]
            else:
                location = "Guatemala"
            return "weather", {"location": location.capitalize()}

        # Envío de correo
        if "enviar correo a" in text_lower:
            # Ejemplo de frase:
            # "enviar correo a juan@example.com asunto prueba cuerpo este es el mensaje"
            parts = text_lower.replace("enviar correo a ", "").split(" asunto ")
            to = parts[0].strip()
            subject, body = "", ""
            if len(parts) > 1:
                rest = parts[1].split(" cuerpo ")
                subject = rest[0].strip()
                if len(rest) > 1:
                    body = rest[1].strip()
            return "send_email", {
                "to": to,
                "subject": subject,
                "body": body
            }

        # Fallback: chat con Gemini
        return "gemini", {"text": text}
