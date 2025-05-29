# action/base_action.py

from abc import ABC, abstractmethod

class BaseAction(ABC):
    @abstractmethod
    def name(self) -> str:
        """
        Nombre único de la acción.
        Ejemplo: 'weather', 'send_email', 'open_app', etc.
        """
        pass

    @abstractmethod
    def execute(self, params: dict) -> str:
        """
        Ejecuta la acción con los parámetros dados y devuelve
        la respuesta como texto.
        """
        pass
