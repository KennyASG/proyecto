# voice_assistant/action/send_email.py

import smtplib
from email.message import EmailMessage
import os
from .base_action import BaseAction
from voice_assistant.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

class SendEmailAction(BaseAction):
    def name(self) -> str:
        return "send_email"

    def execute(self, params: dict) -> str:
        to      = params.get("to")
        subject = params.get("subject", "")
        body    = params.get("body", "")

        # Validaciones básicas
        if not to:
            return "Debes indicar a quién enviar el correo."
        if not SMTP_SERVER or not SMTP_USER or not SMTP_PASSWORD:
            return "Faltan las credenciales SMTP en la configuración."

        # Construye el mensaje
        msg = EmailMessage()
        msg["From"]    = SMTP_USER
        msg["To"]      = to
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            # Conexión segura y envío
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            return f"Correo enviado correctamente a {to}."
        except Exception as e:
            return f"Error al enviar correo: {e}"
