# voice_assistant/action/youtube_action.py

import webbrowser
from pytube import Search
from .base_action import BaseAction

class YouTubeAction(BaseAction):
    def name(self) -> str:
        return "youtube"

    def execute(self, params: dict) -> str:
        """
        Params:
          - query: texto a buscar en YouTube
        """
        query = params.get("query", "").strip()
        if not query:
            return "Debes indicar qué video quieres buscar en YouTube."

        # Busca en YouTube y toma el primer resultado
        try:
            s = Search(query)
            s_results = s.results
        except Exception as e:
            return f"Error buscando en YouTube: {e}"

        if not s_results:
            return f"No encontré resultados para «{query}» en YouTube."

        first = s_results[0]
        url = first.watch_url
        title = first.title

        # Abre en el navegador por defecto
        webbrowser.open(url)
        return f"Abrí en YouTube: {title}"
