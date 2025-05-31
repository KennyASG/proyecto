# voice_assistant/intent/nlu.py

import re


class IntentParser:
    def __init__(self, action_registry):
        self.registry = action_registry
        # Diccionario de contactos conocidos
        self.contacts = {
            "mayen": "mayenrosil@gmail.com",
            "kenny": "saenzk031@gmail.com",
            "fernando": "jofermelenbo@gmail.com",
            "erick" : ""
            # Agregar más contactos aquí
        }

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

        # 2. Regla mejorada para envío de correo
        # enviar correo a <email> asunto <asunto> cuerpo <cuerpo>
        if "enviar correo a" in text_lower:
            email = self._extract_email_from_text(text_lower)
            subject, body = self._extract_email_content(text_lower)
            return "send_email", {"to": email, "subject": subject, "body": body}

        # 3. Regla para WhatsApp
        if "enviar whatsapp a" in text_lower:
            parts = text_lower.replace("enviar whatsapp a ", "").split(" mensaje ")
            to = parts[0].strip()
            message = parts[1].strip() if len(parts) > 1 else ""
            return "send_whatsapp", {"to": to, "message": message}

        if text_lower.startswith("abrir "):
            app_name = text_lower.replace("abrir ", "").strip()
            return "open_app", {"app": app_name}

        # Regla para buscar archivos
        if "buscar archivo" in text_lower:
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

        # Regla para Netflix
        if "netflix" in text_lower or any(keyword in text_lower for keyword in
                                          ["buscar en netflix", "reproducir en netflix", "pausar netflix",
                                           "reanudar netflix"]):
            return self._parse_netflix_command(text_lower)

        # Fallback: chat con Gemini
        # Regla para Spotify
        # voice_assistant/intent/nlu.py  (inserta antes del fallback)

    # Regla para Spotify
           # voice_assistant/intent/nlu.py
        if text_lower.startswith(("spotify buscar", "spotify search")):
            parts = text_lower.split()
            # parts[2:] es el nombre
            track = " ".join(parts[2:]).strip()
            return "spotify_desktop", {"action": "buscar", "track": track}
    # Regla para Spotify
# voice_assistant/intent/nlu.py

                # Spotify Desktop
        if text_lower.startswith("spotify "):
            # Ejemplos:
            #  spotify reproducir
            #  spotify play
            #  spotify pausa
            parts = text_lower.split()
            action = parts[1] if len(parts) > 1 else ""
            return "spotify_desktop", {"action": action}

     



        # 4. Fallback: chat con Gemini
        return "gemini", {"text": text}

    def _parse_netflix_command(self, text: str) -> tuple:
        """Parsea comandos específicos de Netflix"""

        # Patrones de comandos de Netflix
        if "buscar" in text and ("netflix" in text or "en netflix" in text):
            # "buscar stranger things en netflix"
            query = self._extract_netflix_query(text, "buscar")
            return "netflix_control", {"action": "buscar", "query": query}

        elif "reproducir" in text and ("netflix" in text or "en netflix" in text):
            # "reproducir la casa de papel en netflix"
            query = self._extract_netflix_query(text, "reproducir")
            return "netflix_control", {"action": "reproducir", "query": query}

        elif "pausar" in text and "netflix" in text:
            # "pausar netflix"
            return "netflix_control", {"action": "pausar", "query": ""}

        elif "reanudar" in text and "netflix" in text:
            # "reanudar netflix"
            return "netflix_control", {"action": "reanudar", "query": ""}

        elif "cerrar" in text and "netflix" in text:
            # "cerrar netflix"
            return "netflix_control", {"action": "cerrar", "query": ""}

        elif "abrir" in text and "netflix" in text:
            # "abrir netflix"
            return "netflix_control", {"action": "buscar", "query": ""}

        # Comando genérico de Netflix
        return "netflix_control", {"action": "buscar", "query": ""}

    def _extract_netflix_query(self, text: str, action: str) -> str:
        """Extrae la consulta de búsqueda para Netflix"""

        # Remover palabras clave para obtener la consulta
        text = text.replace(action, "").replace("netflix", "").replace("en netflix", "")

        # Limpiar palabras comunes
        stop_words = ["en", "la", "el", "de", "del", "que", "para", "por", "con"]
        words = text.split()
        query_words = [word for word in words if word not in stop_words and word.strip()]

        return " ".join(query_words).strip()

    def _parse_netflix_command(self, text: str) -> tuple:
        """Parsea comandos específicos de Netflix"""

        # Patrones de comandos de Netflix
        if "buscar" in text and ("netflix" in text or "en netflix" in text):
            # "buscar stranger things en netflix"
            query = self._extract_netflix_query(text, "buscar")
            return "netflix_control", {"action": "buscar", "query": query}

        elif "reproducir" in text and ("netflix" in text or "en netflix" in text):
            # "reproducir la casa de papel en netflix"
            query = self._extract_netflix_query(text, "reproducir")
            return "netflix_control", {"action": "reproducir", "query": query}

        elif "pausar" in text and "netflix" in text:
            # "pausar netflix"
            return "netflix_control", {"action": "pausar", "query": ""}

        elif "reanudar" in text and "netflix" in text:
            # "reanudar netflix"
            return "netflix_control", {"action": "reanudar", "query": ""}

        elif "cerrar" in text and "netflix" in text:
            # "cerrar netflix"
            return "netflix_control", {"action": "cerrar", "query": ""}

        elif "abrir" in text and "netflix" in text:
            # "abrir netflix"
            return "netflix_control", {"action": "buscar", "query": ""}

        # Comando genérico de Netflix
        return "netflix_control", {"action": "buscar", "query": ""}

    def _extract_netflix_query(self, text: str, action: str) -> str:
        """Extrae la consulta de búsqueda para Netflix"""

        # Remover palabras clave para obtener la consulta
        text = text.replace(action, "").replace("netflix", "").replace("en netflix", "")

        # Limpiar palabras comunes
        stop_words = ["en", "la", "el", "de", "del", "que", "para", "por", "con"]
        words = text.split()
        query_words = [word for word in words if word not in stop_words and word.strip()]

        return " ".join(query_words).strip()
        """Extrae y reconstruye el email del texto transcrito"""

        # Método 1: Buscar por contacto conocido
        for name, email in self.contacts.items():
            if name in text:
                print(f"[NLU] Contacto encontrado: {name} -> {email}")
                return email

        # Método 2: Intentar reconstruir el email
        email_pattern = self._reconstruct_email_from_speech(text)
        if email_pattern:
            return email_pattern

        # Método 3: Extraer después de "enviar correo a"
        parts = text.replace("enviar correo a ", "").split(" asunto ")
        potential_email = parts[0].strip()

        # Limpiar y reconstruir
        cleaned_email = self._clean_and_rebuild_email(potential_email)
        return cleaned_email

    def _reconstruct_email_from_speech(self, text: str) -> str:
        """Intenta reconstruir emails de texto hablado"""

        replacements = {
            " arroba ": "@",
            " @ ": "@",
            " at ": "@",
            " punto ": ".",
            " dot ": ".",
            " com": ".com",
            " gmail": "gmail",
            " hotmail": "hotmail",
            " yahoo": "yahoo",
            " outlook": "outlook"
        }

        result = text.lower()
        for pattern, replacement in replacements.items():
            result = result.replace(pattern, replacement)

        result = re.sub(r'\s*@\s*', '@', result)
        result = re.sub(r'\s*\.\s*', '.', result)

        email_match = re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', result)
        if email_match:
            return email_match.group()

        return None

    def _clean_and_rebuild_email(self, email_text: str) -> str:
        """Limpia y reconstruye un email mal transcrito"""

        email_text = re.sub(r'\s+', '', email_text.lower())

        corrections = {
            'gmail': '@gmail.com',
            'hotmail': '@hotmail.com',
            'yahoo': '@yahoo.com',
            'outlook': '@outlook.com'
        }

        for service, domain in corrections.items():
            if service in email_text and '@' not in email_text:
                username = email_text.replace(service, '')
                return f"{username}{domain}"

        if '@' in email_text and '.' in email_text:
            return email_text

        if '@' not in email_text:
            return f"{email_text}@gmail.com"

        return email_text

    def _extract_email_content(self, text: str):
        """Extrae asunto y cuerpo del comando de email"""
        subject, body = "", ""

        if " asunto " in text:
            parts = text.split(" asunto ")
            if len(parts) > 1:
                rest = parts[1]
                if " cuerpo " in rest:
                    subject_body = rest.split(" cuerpo ")
                    subject = subject_body[0].strip()
                    body = subject_body[1].strip() if len(subject_body) > 1 else ""
                else:
                    subject = rest.strip()

        return subject, body

    def _extract_email_from_text(self, text: str) -> str:Add commentMore actions
        """Extrae y reconstruye el email del texto transcrito"""

        # Método 1: Buscar por contacto conocido
        for name, email in self.contacts.items():
            if name in text:
                print(f"[NLU] Contacto encontrado: {name} -> {email}")
                return email

        # Método 2: Intentar reconstruir el email
        # Buscar patrones como "algo @ algo punto com"
        email_pattern = self._reconstruct_email_from_speech(text)
        if email_pattern:
            return email_pattern

        # Método 3: Extraer después de "enviar correo a"
        parts = text.replace("enviar correo a ", "").split(" asunto ")
        potential_email = parts[0].strip()

        # Limpiar y reconstruir
        cleaned_email = self._clean_and_rebuild_email(potential_email)
        return cleaned_email

    def _reconstruct_email_from_speech(self, text: str) -> str:
        """Intenta reconstruir emails de texto hablado"""

        # Patrones comunes de speech-to-text para emails
        replacements = {
            " arroba ": "@",
            " @ ": "@",
            " at ": "@",
            " punto ": ".",
            " dot ": ".",
            " com": ".com",
            " gmail": "gmail",
            " hotmail": "hotmail",
            " yahoo": "yahoo",
            " outlook": "outlook"
        }

        result = text.lower()
        for pattern, replacement in replacements.items():
            result = result.replace(pattern, replacement)

        # Remover espacios alrededor de @ y puntos
        result = re.sub(r'\s*@\s*', '@', result)
        result = re.sub(r'\s*\.\s*', '.', result)

        # Buscar patrón de email válido
        email_match = re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', result)
        if email_match:
            return email_match.group()

        return None

    def _clean_and_rebuild_email(self, email_text: str) -> str:
        """Limpia y reconstruye un email mal transcrito"""

        # Remover espacios extra
        email_text = re.sub(r'\s+', '', email_text.lower())

        # Patrones comunes de corrección
        corrections = {
            'gmail': '@gmail.com',
            'hotmail': '@hotmail.com',
            'yahoo': '@yahoo.com',
            'outlook': '@outlook.com'
        }

        # Si no tiene @ pero tiene un servicio conocido
        for service, domain in corrections.items():
            if service in email_text and '@' not in email_text:
                username = email_text.replace(service, '')
                return f"{username}{domain}"

        # Si ya parece un email, devolverlo
        if '@' in email_text and '.' in email_text:
            return email_text

        # Fallback: asumir gmail si no se especifica
        if '@' not in email_text:
            return f"{email_text}@gmail.com"

        return email_text

    def _extract_email_content(self, text: str):
        """Extrae asunto y cuerpo del comando de email"""
        subject, body = "", ""

        if " asunto " in text:
            parts = text.split(" asunto ")
            if len(parts) > 1:
                rest = parts[1]
                if " cuerpo " in rest:
                    subject_body = rest.split(" cuerpo ")
                    subject = subject_body[0].strip()
                    body = subject_body[1].strip() if len(subject_body) > 1 else ""
                else:
                    subject = rest.strip()

        return subject, body