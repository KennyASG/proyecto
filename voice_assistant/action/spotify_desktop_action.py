# voice_assistant/action/spotify_desktop_action.py

import platform
import subprocess
import os
from .base_action import BaseAction
import time
import pygetwindow as gw


try:
    import keyboard
except ImportError:
    keyboard = None




try:
    import pygetwindow as gw
except ImportError:
    gw = None

def open_or_focus_spotify():
    system = platform.system()

    # 1) Si la ventana ya existe, tráela al frente
    if gw:
        
        #print("entra 1")
        wins = gw.getWindowsWithTitle("Spotify")
        if wins:
            #print("entra 2")
            win = wins[0]
            try:
                #print("entra 3")
               # print(f"[Netflix] SPOTIFY pantalla de perfiles: {win}")
                win.activate()
                time.sleep(0.5)
                return
            except Exception as e:
                return
                #print(f"Error al activar la ventana de Spotify: {e}")
                # Si falla, seguimos con el siguiente paso

    # 2) Si no hay ventana, abre la app nativa
    if system == "Windows":
       # print("entra 4")
        os.startfile("spotify.exe")
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", "Spotify"])
    else:
        subprocess.Popen(["spotify"])

    # 3) Espera a que arranque y enfócalo
    time.sleep(3)
    if gw:
        wins = gw.getWindowsWithTitle("Spotify")
        if wins:
            win = wins[0]
            win.activate()
            time.sleep(0.5)



class SpotifyDesktopAction(BaseAction):





    def name(self) -> str:
        return "spotify_desktop"

    def execute(self, params: dict) -> str:
        action = params.get("action", "").lower().strip()
        
        open_or_focus_spotify()

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
                "regresar": "previous track",
                "skip": "next track",
                "stop": "play/pause media"
            }
            if action in ("buscar", "search") :
                track = params.get("track", "").strip()
                time.sleep(7)
                # 1) Foco en el buscador: Ctrl+L
                keyboard.send("ctrl+l")
                time.sleep(2)
                # 2) Escribe el nombre de la canción
                keyboard.write(track)
                time.sleep(2)
                # 3) Enter para lanzar la búsqueda
                keyboard.send("enter")
                # 4) Espera a que cargue resultados
                time.sleep(4)
                # 5) Flecha abajo para seleccionar la primera canción
                keyboard.send("tab")
                time.sleep(2)
                # 6) Enter para reproducirla
                keyboard.send("enter")
                time.sleep(4)
                # 6) Enter para reproducirla
                keyboard.send("enter")
                time.sleep(1)
                return f"Buscando y reproduciendo «{track}» en Spotify Desktop."
            key = mapping.get(action)
            if key:
                if action == "anterior":
                    keyboard.send(key)
                    time.sleep(0.2)
                    keyboard.send(key)
                else:
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
                "regresar": 'tell application "Spotify" to previous track',
                "stop": 'tell application "Spotify" to pause'
            }
            cmd = script_map.get(action)
            if cmd:
                if action == "anterior":
                    subprocess.run(["osascript", "-e", cmd])
                    time.sleep(0.2)
                    subprocess.run(["osascript", "-e", cmd])
                else:
                    subprocess.run(["osascript", "-e", cmd])
                return f"Ejecutada acción «{action}» en Spotify Desktop."
        else:
            # Linux o demás
            return "Control de Spotify Desktop no soportado en este sistema."

        return f"No entendí la acción «{action}» para Spotify Desktop."
