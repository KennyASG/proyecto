# voice_assistant/action/spotify_action.py

from pathlib import Path
from .base_action import BaseAction
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class SpotifyAction(BaseAction):
    def __init__(self):
        project_root = Path(__file__).parent.parent
        profile_dir = project_root / "spotify_profile"
        if not profile_dir.exists():
            raise RuntimeError("Ejecuta antes init_spotify_profile.py para iniciar sesión en Spotify Web")
        options = Options()
        options.add_argument(f"--user-data-dir={profile_dir}")
        self.chrome_options = options

    def name(self) -> str:
        return "spotify"

    def execute(self, params: dict) -> str:
        action = params.get("action", "").lower()
        track  = params.get("track", "").strip()

        driver = webdriver.Chrome(options=self.chrome_options)
        driver.maximize_window()
        driver.get("https://open.spotify.com")
        time.sleep(5)  # deja que cargue tu sesión

        try:
            # ... (lógica de búsqueda/reproducción igual que antes) ...
            # Por ejemplo, para “play track”:
            if action in ("play", "reproducir") and track:
                # tu código de búsqueda y click de botón Play aquí...
                pass

            # Para “pause”
            if action in ("pause", "pausar"):
                btn = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Pause']")
                if btn:
                    btn[0].click()
                    driver.quit()
                    return "Pausado en Spotify Web."

            # y así con next, prev...

            driver.quit()
            return "Acción Spotify ejecutada."
        except Exception as e:
            driver.quit()
            return f"Error en SpotifyAction: {e}"
