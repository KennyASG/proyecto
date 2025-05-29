# intent/nlu.py

class IntentParser:
    def __init__(self, action_registry):
        """
        Recibe la instancia de ActionRegistry para luego resolver acciones.
        """
        self.registry = action_registry

    def parse(self, text: str):
        """
        Analiza el texto y devuelve una tupla (action_name, params_dict).
        """
        text_lower = text.lower()

        # 1. Regla simple para clima
        if "clima" in text_lower:
            parts = text_lower.split()
            if "en" in parts:
                idx = parts.index("en")
                # tomo la palabra siguiente como ubicación
                location = parts[idx + 1]
            else:
                location = "Guatemala"
            return "weather", {"location": location.capitalize()}

        # 2. Aquí puedes añadir más reglas basadas en palabras clave...
        #    por ejemplo:
        #    if "correo" in text_lower: return "send_email", {...}

        # 3. Fallback: todo lo demás va a ChatGPT
        return "chat", {"text": text}
