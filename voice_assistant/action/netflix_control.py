# voice_assistant/action/netflix_control.py

import time
from pathlib import Path
from .base_action import BaseAction
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class NetflixControlAction(BaseAction):
    def name(self) -> str:
        return "netflix_control"

    def execute(self, params: dict) -> str:
        action = params.get("action", "").strip().lower()
        query = params.get("query", "").strip()

        if not action:
            return "Debes especificar una acción: buscar, reproducir, pausar, reanudar, o cerrar."

        # 1) Ruta del perfil dedicado para Netflix
        project_root = Path(__file__).parent.parent
        profile_dir = project_root / "netflix_profile"
        profile_dir.mkdir(exist_ok=True)

        # 2) Configura Chrome
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={profile_dir}")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(options=chrome_options)

        # Ocultar que es un navegador automatizado
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.maximize_window()

        try:
            if action in ["buscar", "reproducir"]:
                return self._search_and_play(driver, query, action)
            elif action == "pausar":
                return self._pause_content(driver)
            elif action == "reanudar":
                return self._resume_content(driver)
            elif action == "cerrar":
                return self._close_netflix(driver)
            else:
                driver.quit()
                return f"Acción no reconocida: {action}"

        except Exception as e:
            driver.quit()
            return f"Error controlando Netflix: {e}"

    def _search_and_play(self, driver, query: str, action: str) -> str:
        """Busca contenido en Netflix y opcionalmente lo reproduce"""
        if not query:
            driver.quit()
            return "Debes especificar qué buscar en Netflix."

        # Navegar a Netflix
        driver.get("https://www.netflix.com/browse")

        try:
            # Esperar que cargue completamente la página
            print("[Netflix] Esperando que cargue Netflix...")
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(3)

            # Verificar si estamos en la pantalla de selección de perfiles
            if not self._handle_profile_selection(driver):
                driver.quit()
                return "No pude seleccionar un perfil automáticamente. Por favor selecciona uno manualmente e intenta de nuevo."

            print("[Netflix] Perfil seleccionado, continuando...")
            time.sleep(3)

            # Verificar que estemos en la página principal
            try:
                WebDriverWait(driver, 15).until(
                    lambda d: any([
                        len(d.find_elements(By.CSS_SELECTOR, ".lolomo")) > 0,
                        len(d.find_elements(By.CSS_SELECTOR, ".browse-container")) > 0,
                        len(d.find_elements(By.CSS_SELECTOR, "[data-uia='billboard']")) > 0
                    ])
                )
                print("[Netflix] Página principal cargada")
            except TimeoutException:
                print("[Netflix] Advertencia: La página principal tardó en cargar")

            # Ahora intentar búsqueda
            print("[Netflix] Intentando búsqueda...")

            # Intentar múltiples selectores para el icono de búsqueda
            search_selectors = [
                "button[data-uia='header-search-icon']",
                ".searchTab",
                "[aria-label='Buscar']",
                "a[href='/search']",
                ".search-box",
                ".icon-search"
            ]

            search_clicked = False
            for selector in search_selectors:
                try:
                    print(f"[Netflix] Intentando selector: {selector}")
                    search_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    search_element.click()
                    search_clicked = True
                    print("[Netflix] Icono de búsqueda encontrado y clickeado")
                    break
                except TimeoutException:
                    continue

            if not search_clicked:
                # Alternativa: usar atajo de teclado
                print("[Netflix] Intentando atajo de teclado...")
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
                # Presionar '/' para abrir búsqueda en Netflix
                driver.find_element(By.TAG_NAME, "body").send_keys("/")
                time.sleep(1)
                search_clicked = True

            if not search_clicked:
                print("[Netflix] DEBUG - No se pudo hacer clic en búsqueda, analizando página...")
                self._debug_page_elements(driver)
                driver.quit()
                return "No pude encontrar el botón de búsqueda en Netflix."

            # Buscar el campo de entrada de texto
            input_selectors = [
                "input[data-uia='search-box-input']",
                "input[placeholder*='search']",
                "input[placeholder*='buscar']",
                ".search-box input",
                "input[type='search']"
            ]

            search_input = None
            for selector in input_selectors:
                try:
                    print(f"[Netflix] Buscando input: {selector}")
                    search_input = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue

            if not search_input:
                # Si no encuentra el input, intentar con todos los inputs visibles
                inputs = driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    if inp.is_displayed():
                        search_input = inp
                        break

            if search_input:
                print(f"[Netflix] Campo de búsqueda encontrado, escribiendo: {query}")
                search_input.clear()
                search_input.send_keys(query)
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)
            else:
                driver.quit()
                return "No pude encontrar el campo de búsqueda en Netflix."

            if action == "reproducir":
                # Buscar resultados de búsqueda
                result_selectors = [
                    ".title-card",
                    ".slider-item",
                    ".boxart-container",
                    "[data-uia='title-card']",
                    ".titleCard"
                ]

                first_result = None
                for selector in result_selectors:
                    try:
                        print(f"[Netflix] Buscando resultados con: {selector}")
                        results = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                        )
                        if results:
                            first_result = results[0]
                            print(f"[Netflix] Encontrados {len(results)} resultados")
                            break
                    except TimeoutException:
                        continue

                if not first_result:
                    driver.quit()
                    return f"Encontré resultados para '{query}' pero no pude seleccionar ninguno."

                # Hacer clic en el primer resultado
                try:
                    driver.execute_script("arguments[0].click();", first_result)
                    print("[Netflix] Resultado seleccionado")
                    time.sleep(3)
                except Exception as e:
                    print(f"[Netflix] Error haciendo clic: {e}")

                # Buscar botón de reproducir en la página de detalles
                play_selectors = [
                    "button[data-uia='play-button']",
                    "button[aria-label*='Reproducir']",
                    "button[aria-label*='Play']",
                    ".playLink",
                    ".play-button",
                    "a[aria-label*='Reproducir']"
                ]

                for selector in play_selectors:
                    try:
                        print(f"[Netflix] Buscando botón play: {selector}")
                        play_button = WebDriverWait(driver, 8).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        play_button.click()
                        print("[Netflix] Botón de reproducir presionado")
                        time.sleep(3)
                        driver.quit()
                        return f"Reproduciendo: {query}"
                    except TimeoutException:
                        continue

                # Si no encuentra botón de play, intentar con enter o espacio
                try:
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
                    time.sleep(2)
                    driver.quit()
                    return f"Intentando reproducir: {query}"
                except:
                    pass

                driver.quit()
                return f"Encontré '{query}' pero no pude reproducirlo automáticamente. Se abrió la página de detalles."
            else:
                driver.quit()
                return f"Búsqueda completada para: {query}"

        except TimeoutException:
            driver.quit()
            return "No pude cargar Netflix o encontrar el contenido."

    def _pause_content(self, driver) -> str:
        """Pausa el contenido actual en Netflix"""
        # Buscar si hay una pestaña de Netflix abierta
        if not self._find_netflix_tab(driver):
            driver.quit()
            return "No hay contenido de Netflix reproduciéndose."

        try:
            # Hacer clic en el área del video para mostrar controles
            video_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            video_area.click()

            time.sleep(1)

            # Buscar botón de pausa
            pause_selectors = [
                "[data-uia='control-pause-button']",
                ".button-nfplayerPause",
                "[aria-label*='Pausar']"
            ]

            for selector in pause_selectors:
                try:
                    pause_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    pause_button.click()
                    driver.quit()
                    return "Contenido pausado."
                except TimeoutException:
                    continue

            # Alternativa: usar espacio para pausar
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
            driver.quit()
            return "Contenido pausado (usando espaciador)."

        except Exception:
            driver.quit()
            return "No pude pausar el contenido."

    def _resume_content(self, driver) -> str:
        """Reanuda el contenido pausado en Netflix"""
        if not self._find_netflix_tab(driver):
            driver.quit()
            return "No hay contenido de Netflix abierto."

        try:
            # Hacer clic en el área del video
            video_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            video_area.click()

            time.sleep(1)

            # Buscar botón de reproducir
            play_selectors = [
                "[data-uia='control-play-button']",
                ".button-nfplayerPlay",
                "[aria-label*='Reproducir']"
            ]

            for selector in play_selectors:
                try:
                    play_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    play_button.click()
                    driver.quit()
                    return "Contenido reanudado."
                except TimeoutException:
                    continue

            # Alternativa: usar espacio
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
            driver.quit()
            return "Contenido reanudado (usando espaciador)."

        except Exception:
            driver.quit()
            return "No pude reanudar el contenido."

    def _close_netflix(self, driver) -> str:
        """Cierra Netflix"""
        try:
            driver.quit()
            return "Netflix cerrado."
        except Exception:
            return "Error cerrando Netflix."

    def _find_netflix_tab(self, driver) -> bool:
        """Busca si hay una pestaña de Netflix abierta"""
        try:
            # Obtener todas las ventanas/pestañas
            windows = driver.window_handles
            for window in windows:
                driver.switch_to.window(window)
                if "netflix.com" in driver.current_url.lower():
                    return True

            # Si no hay pestaña abierta, ir a Netflix
            driver.get("https://www.netflix.com/browse")
            return True

        except Exception:
            return False

    def _handle_profile_selection(self, driver) -> bool:
        """Maneja la pantalla de selección de perfiles"""
        try:
            # Verificar si estamos en la pantalla de perfiles
            profile_indicators = [
                "¿Quién está viendo ahora?",
                "Who's watching?",
                ".profiles-gate-container",
                ".choose-profile",
                ".profile-gate"
            ]

            is_profile_screen = False
            for indicator in profile_indicators:
                try:
                    if indicator.startswith("."):
                        # Es un selector CSS
                        driver.find_element(By.CSS_SELECTOR, indicator)
                    else:
                        # Es texto
                        driver.find_element(By.XPATH, f"//*[contains(text(), '{indicator}')]")
                    is_profile_screen = True
                    print(f"[Netflix] Detectada pantalla de perfiles: {indicator}")
                    break
                except:
                    continue

            if not is_profile_screen:
                print("[Netflix] No hay pantalla de perfiles, continuando...")
                return True

            # Buscar perfiles disponibles
            profile_selectors = [
                ".profile-link",
                ".avatar",
                "[data-uia='profile-link']",
                ".profiles .profile",
                ".choose-profile .profile"
            ]

            selected_profile = False
            for selector in profile_selectors:
                try:
                    print(f"[Netflix] Buscando perfiles con: {selector}")
                    profiles = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )

                    if profiles:
                        # Seleccionar el primer perfil
                        print(f"[Netflix] Encontrados {len(profiles)} perfiles, seleccionando el primero")
                        first_profile = profiles[0]

                        # Intentar hacer clic
                        try:
                            first_profile.click()
                        except:
                            # Si no funciona el clic normal, usar JavaScript
                            driver.execute_script("arguments[0].click();", first_profile)

                        selected_profile = True
                        print("[Netflix] Perfil seleccionado exitosamente")

                        # Esperar a que cargue el perfil
                        time.sleep(5)
                        break

                except TimeoutException:
                    continue

            if not selected_profile:
                print("[Netflix] No se pudo seleccionar automáticamente un perfil")
                self._debug_page_elements(driver)
                return False

            return True

        except Exception as e:
            print(f"[Netflix] Error manejando selección de perfiles: {e}")
            return False

    def _debug_page_elements(self, driver):
        """Función de debugging para ver qué elementos están disponibles"""
        try:
            # Buscar todos los elementos clickeables
            clickable_elements = driver.find_elements(By.CSS_SELECTOR, "[role='button'], button, a, input")
            print(f"[Debug] Encontrados {len(clickable_elements)} elementos clickeables")

            for i, elem in enumerate(clickable_elements[:10]):  # Solo los primeros 10
                try:
                    text = elem.get_attribute("aria-label") or elem.text or elem.get_attribute(
                        "placeholder") or "Sin texto"
                    tag = elem.tag_name
                    print(f"[Debug] {i}: {tag} - {text[:50]}")
                except:
                    pass

        except Exception as e:
            print(f"[Debug] Error: {e}")