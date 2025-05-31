# voice_assistant/action/shutdown_action.py

import sys
import os
from .base_action import BaseAction

class ShutdownAction(BaseAction):
    def name(self) -> str:
        return "shutdown"

    def execute(self, params: dict) -> str:
        """
        Esta acción no devuelve nada “útil” porque va a terminar el proceso.
        """
        # Si existiera algún recurso global que quieras cerrar (archivos, hilos, etc.),
        # hazlo antes de salir. Por ejemplo:
        # if existe_driver:
        #     driver.quit()
        #     driver = None

        # Notifica al usuario que el bot se va a cerrar
        respuesta = "Entendido. Me apago ahora mismo."
        # (Opcional) imprime/loggea la respuesta antes de morir:
        print(respuesta)

        # Cierra todo el proceso:
        os._exit(0)
        # Alternativa: sys.exit(0)
        # sys.exit(0)

        # (Nunca se llega a este return, porque os._exit() no regresa)
        return respuesta
