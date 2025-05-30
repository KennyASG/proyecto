# voice_assistant/action/spotify_desktop_action.py

import platform
import subprocess
import os
from .base_action import BaseAction

try:
    import keyboard
except ImportError:
    keyboard = None

class SpotifyDesktopAction(BaseAction):
    def name(self) -> str:
        return "spotify_desktop"

    def execute(self, params: dict) -> str:
        action = params.get("action", "").lower().strip()
        print(f"[SpotifyDesktopAction] Acción recibida: {action}")

        system = platform.system()

        # 1) Si piden abrir la app
        if action in ("abrir", "open"):
            try:
                if system == "Windows":
                    os.startfile("spotify.exe")
                elif system == "Darwin":
                    subprocess.Popen(["open", "-a", "Spotify"])
                else:
                    subprocess.Popen(["spotify"])
                return "Abriendo Spotify Desktop..."
            except Exception as e:
                return f"Error abriendo Spotify: {e}"

        # 2) Para controlar reproducción necesitamos 'keyboard'
        if system == "Windows":
            if not keyboard:
                return "Instala la librería keyboard: pip install keyboard"
            mapping = {
                "play": "play/pause media",
                "reproducir": "play/pause media",
                "pause": "play/pause media",
                "pausa": "play/pause media",
                "next": "next track",
                "siguiente": "next track",
                "prev": "previous track",
                "anterior": "previous track",
                "skip": "next track",
                "stop": "play/pause media"
            }
            key = mapping.get(action)
            if key:
                keyboard.send(key)
                return f"Ejecutada acción «{action}» en Spotify Desktop."
        elif system == "Darwin":
            # AppleScript para macOS
            script_map = {
                "play": 'tell application "Spotify" to playpause',
                "reproducir": 'tell application "Spotify" to playpause',
                "pause": 'tell application "Spotify" to playpause',
                "pausa": 'tell application "Spotify" to playpause',
                "next": 'tell application "Spotify" to next track',
                "siguiente": 'tell application "Spotify" to next track',
                "prev": 'tell application "Spotify" to previous track',
                "anterior": 'tell application "Spotify" to previous track',
                "stop": 'tell application "Spotify" to pause'
            }
            cmd = script_map.get(action)
            if cmd:
                subprocess.run(["osascript", "-e", cmd])
                return f"Ejecutada acción «{action}» en Spotify Desktop."
        else:
            # Linux o demás
            return "Control de Spotify Desktop no soportado en este sistema."

        return f"No entendí la acción «{action}» para Spotify Desktop."
