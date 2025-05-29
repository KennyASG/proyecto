
from .base_action import BaseAction
import requests
import os

class WeatherAction(BaseAction):
    def name(self) -> str:
        return "weather"

    def execute(self, params: dict) -> str:
        location = params.get("location", "Guatemala")
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return "No configuré la clave de OpenWeatherMap."

        url = "https://api.openweathermap.org/data/2.5/weather"
        resp = requests.get(url, params={
            "q": location,
            "appid": api_key,
            "units": "metric",
            "lang": "es"
        })

        # ── DEBUG ───────────────────────────────────────────────────
        
        # ───────────────────────────────────────────────────────────

        if resp.status_code != 200:
            return f"No pude obtener el clima para {location}."

        data = resp.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"En {location} hay {desc} y la temperatura es {temp} °C."
