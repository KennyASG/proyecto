# voice_assistant/action/send_whatsapp.py

import time
from pathlib import Path
from .base_action import BaseAction
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SendWhatsAppAction(BaseAction):
    def name(self) -> str:
        return "send_whatsapp"

    def execute(self, params: dict) -> str:
        to      = params.get("to", "").strip()
        message = params.get("message", "").strip()
        if not to or not message:
            return "Debes indicar el destinatario y el mensaje."

        # 1) Ruta del perfil dedicado dentro del proyecto
        project_root = Path(__file__).parent.parent
        profile_dir = project_root / "whatsapp_profile"
        profile_dir.mkdir(exist_ok=True)

        # 2) Configura Chrome para usar ese perfil
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={profile_dir}")
        # No especifique --profile-directory, así usará el único perfil creado allí

        # 3) Lanza Chrome (cierra todas las instancias de Chrome si están abiertas)
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        # 4) Navega a WhatsApp Web
        driver.get("https://web.whatsapp.com")

        try:
            # 5) Espera hasta que WhatsApp esté listo (título cambie)
            WebDriverWait(driver, 60).until(EC.title_contains("WhatsApp"))
            # A partir de aquí ya tienes sesión iniciada en este perfil

        


            # 6) Busca el chat
            search = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, 
                   '//div[@contenteditable="true" and @data-tab="3"]'))
            )
            search.click()
            search.clear()
            search.send_keys(to)
            time.sleep(2)
            search.send_keys(Keys.ENTER)

            # 7) Envía el mensaje
            msg_box = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, 
                   '//div[@contenteditable="true" and @data-tab="10"]'))
            )
            for line in message.split("\n"):
                msg_box.send_keys(line)
                msg_box.send_keys(Keys.SHIFT, Keys.ENTER)
            msg_box.send_keys(Keys.ENTER)

            time.sleep(1)
            driver.quit()
            return f"Mensaje enviado a {to}."
        except Exception as e:
            driver.quit()
            return f"Error enviando WhatsApp: {e}"
