# voice_assistant/action/registry.py
import pkgutil
import importlib
from .base_action import BaseAction

class ActionRegistry:
    def __init__(self):
        self.actions = {}
        self._load_actions()

    def _load_actions(self):
        # Determina el nombre del paquete actual, p.ej. 'voice_assistant.action'
        package_name = __package__
        # Importa el paquete de acciones
        package = importlib.import_module(package_name)
        # Itera sobre los módulos del paquete
        for finder, module_name, ispkg in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package_name}.{module_name}")
            # Busca clases que hereden de BaseAction
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, BaseAction) and obj is not BaseAction:
                    instance = obj()
                    self.actions[instance.name()] = instance

    def get_action(self, name: str):
        """
        Devuelve la instancia de acción asociada al nombre dado.
        """
        return self.actions.get(name)

    def list_actions(self):
        """
        Retorna un listado con todos los nombres de acciones registradas.
        """
        return list(self.actions.keys())