# init_spotify_profile.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time

# 1) Crea la carpeta de perfil si no existe
project_root = Path(__file__).parent
profile_dir = project_root / "spotify_profile"
profile_dir.mkdir(exist_ok=True)

# 2) Configura Chrome para usar ese perfil
options = Options()
options.add_argument(f"--user-data-dir={profile_dir}")

# 3) Abre Spotify Web y espera a que inicies sesión manualmente
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://open.spotify.com")

print("\n→ Se abrió Spotify Web en una ventana de Chrome.")
print("→ Inicia sesión manualmente (o escanea QR) y luego cierra la ventana para continuar.")
# Espera hasta que cierres la ventana
while True:
    try:
        # Si intenta acceder a driver.title falla, asumimos que cerraste
        _ = driver.title
        time.sleep(1)
    except:
        break

print("Perfil de Spotify Web inicializado y guardado en:", profile_dir)
