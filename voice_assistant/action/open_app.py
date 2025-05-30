# voice_assistant/action/open_app.py

import os
import platform
import subprocess
from .base_action import BaseAction

class OpenAppAction(BaseAction):
    def name(self) -> str:
        return "open_app"

    def execute(self, params: dict) -> str:
        app = params.get("app", "").lower()
        if not app:
            return "Debes indicar el nombre de la aplicación a abrir."

        cmd = app
        if not cmd:
            return f"No conozco cómo abrir «{app}». Verifica el nombre."

        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(cmd)
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", cmd])
            else:  # Linux
                subprocess.Popen([cmd])
            return f"Abrí {app}."
        except Exception as e:
            return f"Error al abrir {app}: {e}"
