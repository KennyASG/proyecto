# voice_assistant/action/gemini_action.py

from .base_action import BaseAction
import google.generativeai as genai
from voice_assistant.config import GENAI_API_KEY, GENAI_MODEL

class GeminiAction(BaseAction):
    def __init__(self):
        if not GENAI_API_KEY:
            raise RuntimeError("Falta GENAI_API_KEY en .env")
        genai.configure(api_key=GENAI_API_KEY)
        self.model = genai.GenerativeModel(GENAI_MODEL)

    def name(self) -> str:
        return "gemini"

    def execute(self, params: dict) -> str:
        prompt = params.get("text", "").strip()
        if not prompt:
            return "No recibí ninguna pregunta para Gemini."
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error al llamar a Gemini: {e}"
