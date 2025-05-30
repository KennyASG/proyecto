# voice_assistant/intent/nlu.py

class IntentParser:
    def __init__(self, action_registry):
        self.registry = action_registry

    def parse(self, text: str):
        text_lower = text.lower()

        # 1. Regla para clima
        if "clima" in text_lower:
            parts = text_lower.split()
            if "en" in parts:
                idx = parts.index("en")
                location = parts[idx + 1]
            else:
                location = "Guatemala"
            return "weather", {"location": location.capitalize()}

        # 2. Regla para envío de correo
        if "enviar correo a" in text_lower:
            # "enviar correo a <to> asunto <subject> cuerpo <body>"
            parts = text_lower.replace("enviar correo a ", "").split(" asunto ")
            to = parts[0].strip()
            subject, body = "", ""
            if len(parts) > 1:
                rest = parts[1].split(" cuerpo ")
                subject = rest[0].strip()
                if len(rest) > 1:
                    body = rest[1].strip()
            return "send_email", {"to": to, "subject": subject, "body": body}

        # 3. Regla para WhatsApp
        if "enviar whatsapp a" in text_lower:
            # "enviar whatsapp a <to> mensaje <message>"
            parts = text_lower.replace("enviar whatsapp a ", "").split(" mensaje ")
            to = parts[0].strip()
            message = parts[1].strip() if len(parts) > 1 else ""
            return "send_whatsapp", {"to": to, "message": message}

        if text_lower.startswith("abrir "):
            # "abrir vscode", "abrir chrome", etc.
            app_name = text_lower.replace("abrir ", "").strip()
            return "open_app", {"app": app_name}


        # Regla para buscar archivos
        if "buscar archivo" in text_lower:
            # "buscar archivo presupuesto en Documentos"
            parts = text_lower.replace("buscar archivo ", "").split(" en ")
            name = parts[0].strip()
            path = parts[1].strip() if len(parts) > 1 else None
            return "file_search", {"name": name, "path": path}
            
        # Regla para YouTube
        if text_lower.startswith(("buscar video", "reproducir video", "youtube")):
            # e.g. "buscar video gatos divertidos"
            #      "reproducir video música jazz"
            #      "youtube tutorial python"
            # quitamos la palabra clave y usamos el resto como query
            for prefix in ("buscar video", "reproducir video", "youtube"):
                if text_lower.startswith(prefix):
                    query = text_lower[len(prefix):].strip()
                    break
            return "youtube", {"query": query}

        # 4. Fallback: chat con Gemini
        return "gemini", {"text": text}
