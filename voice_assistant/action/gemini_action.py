# voice_assistant/action/gemini_action.py

import os
import google.generativeai as genai
from .base_action import BaseAction

class GeminiAction(BaseAction):
    def __init__(self):
        # Configura tu API key de Google Generative AI desde .env
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Falta la variable GENAI_API_KEY en .env")
        genai.configure(api_key=api_key)

        # Selecciona el modelo (puedes parametrizar GENAI_MODEL en .env)
        model_name = os.getenv("GENAI_MODEL", "gemini-2.0-flash")
        self.model = genai.GenerativeModel(model_name)

    def name(self) -> str:
        return "gemini"

    def execute(self, params: dict) -> str:
        prompt = params.get("text", "").strip()
        if not prompt:
            return "No recibí ninguna pregunta para Gemini."

        try:
            # Genera la respuesta
            response = self.model.generate_content(prompt)
            # El texto de la respuesta está en response.text
            return response.text.strip()
        except Exception as e:
            return f"Error al llamar a Gemini: {e}"
