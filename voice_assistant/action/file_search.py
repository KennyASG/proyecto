# voice_assistant/action/file_search.py

import os
from .base_action import BaseAction

class FileSearchAction(BaseAction):
    def name(self) -> str:
        return "file_search"

    def execute(self, params: dict) -> str:
        """
        Params:
          - name: parte del nombre de archivo a buscar
          - path: carpeta raíz opcional donde buscar (por defecto tu home)
        """
        name = params.get("name", "").lower().strip()
        root = params.get("path") or os.path.expanduser("~")
        if not name:
            return "Debes indicar el nombre (o parte) del archivo a buscar."

        matches = []
        for dirpath, dirnames, filenames in os.walk(root):
            for fn in filenames:
                if name in fn.lower():
                    matches.append(os.path.join(dirpath, fn))
                    if len(matches) >= 5:  # límite para no abrumar
                        break
            if len(matches) >= 5:
                break

        if not matches:
            return f"No encontré archivos que contengan «{name}» en {root}."
        # Formatea hasta 5 resultados
        respuesta = "Encontré:\n" + "\n".join(matches)
        return respuesta
