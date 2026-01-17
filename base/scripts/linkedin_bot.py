from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from base.models import Contacto


# 📝 Función para buscar un contacto y enviar un mensaje


# 🔄 Función para procesar contactos SOLO cuando se llame desde el dashboard
from base.scripts.popups import cerrar_popups_visual  # 👈 importa tu función visual

def procesar_contactos(limite):
    # Configurar Chrome con User-Agent modificado para evitar bloqueos
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Inicializar el navegador
    driver = webdriver.Chrome(options=options)

    # Iniciar sesión en LinkedIn manualmente antes de ejecutar el RPA
    driver.get("https://www.linkedin.com")
    input("🔑 Inicia sesión en LinkedIn y luego presiona ENTER para continuar...")

    # Obtener contactos pendientes según el límite ingresado por el usuario
    contactos = Contacto.objects.filter(mensaje_enviado=False)[:limite]

    for contacto in contactos:
        cerrar_popups_visual()  # 🔹 justo antes de procesar el contacto

        buscar_contacto_y_enviar_mensaje(driver, contacto)

        cerrar_popups_visual()  # 🔹 después de enviar el mensaje

        # ✅ Pausa aleatoria entre contactos para evitar bloqueos
        pausa_aleatoria = random.uniform(3, 7)
        print(f"⏳ Esperando {pausa_aleatoria:.2f} segundos antes del siguiente contacto...")
        time.sleep(pausa_aleatoria)

    print(f"✅ Se enviaron {len(contactos)} mensajes.")

    # Cerrar el navegador al terminar
    driver.quit()



# Función para detectar y hacer clic en el botón por imagen
import cv2
import numpy as np
import pyautogui
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime


# Función para detectar y hacer clic en el botón por imagen
def buscar_y_hacer_click_en_boton(imagen_boton):
    # Obtener la ruta absoluta de la imagen
    ruta_imagen = os.path.abspath(imagen_boton)

    # Cargar la imagen desde la ruta absoluta
    template = cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED)

    if template is None:
        print(f"❌ No se encontró la imagen {ruta_imagen}. Verifica su ubicación.")
        return False

    # Capturar pantalla
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)

    # Convertir la captura de pantalla a escala de grises
    gray_screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Buscar coincidencias
    resultado = cv2.matchTemplate(gray_screenshot, gray_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

    # Si la coincidencia es suficientemente alta, hacer clic
    if max_val > 0.8:  # Ajusta el umbral según sea necesario
        x, y = max_loc
        pyautogui.moveTo(x + (template.shape[1] // 2), y + (template.shape[0] // 2), duration=1)
        pyautogui.click()
        print("✅ Botón encontrado y clickeado.")
        return True
    else:
        print("❌ No se encontró el botón en pantalla.")
        return False



# Función principal de LinkedIn

import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


import random
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def buscar_contacto_y_enviar_mensaje(driver, contacto, mensaje, campana):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import time, random
    from datetime import datetime
    import pyautogui
    from base.scripts.popups import cerrar_popups_visual
    from base.scripts.envio_log import registrar_envio  # ✅ registro personalizado

    try:
        nombre_completo = contacto.nombre.strip()
        primer_nombre = nombre_completo.split(" ")[0]
        mensaje_personalizado = mensaje.replace("{nombre}", primer_nombre)

        print(f"🔍 Buscando perfil de {nombre_completo} en LinkedIn...")

        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Buscar')]"))
        )
        search_box.send_keys(Keys.CONTROL, "a")
        search_box.send_keys(Keys.BACKSPACE)
        time.sleep(1)

        for letra in nombre_completo:
            search_box.send_keys(letra)
            time.sleep(random.uniform(0.1, 0.3))

        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        perfiles = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
        if not perfiles:
            # 🧠 Fallback: usar link directo si existe


            if contacto.linkedin_url:
                print(f"🔁 No se encontró perfil por búsqueda. Abriendo URL directa para {nombre_completo}...")
                driver.get(contacto.linkedin_url)
                time.sleep(5)
            else:
                print(f"❌ No se encontraron resultados ni URL para {nombre_completo}.")
                registrar_envio(contacto, campana, exito=False)
                return
        else:
            perfiles[0].click()
            time.sleep(5)
            print(f"✅ Perfil de {nombre_completo} abierto por búsqueda.")

        # 🕵️ Verifica si el perfil cargó correctamente (opcional)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile-top-card"))
            )
        except:
            print("⚠️ Perfil posiblemente no cargado del todo.")

        ActionChains(driver).move_by_offset(50, 50).click().perform()
        time.sleep(2)

        # 🔍 Intentar encontrar botón “Enviar mensaje”
        if not buscar_y_hacer_click_en_boton("boton_enviar.png"):
            try:
                boton_enviar = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Enviar mensaje')]"))
                )
                boton_enviar.click()
                print(f"✅ Botón detectado por XPath y clickeado.")
            except Exception:
                print(f"❌ No se pudo encontrar 'Enviar mensaje' para {nombre_completo}.")
                registrar_envio(contacto, campana, exito=False)
                return

        print(f"✅ Cuadro de mensaje abierto para {nombre_completo}.")

        mensaje_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Escribe un mensaje')]"))
        )

        mensaje_box.send_keys(mensaje_personalizado)
        time.sleep(3)

        if not buscar_y_hacer_click_en_boton("boton_enviar_chat.png"):
            print(f"❌ No se pudo hacer clic en el botón azul 'Enviar'.")
            registrar_envio(contacto, campana, exito=False)
            return

        print(f"✅ Mensaje enviado correctamente a {nombre_completo}.")

        cerrar_popups_visual(driver)
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        print(f"✅ Chat cerrado, listo para el siguiente contacto.")

        contacto.mensaje_enviado = True
        contacto.fecha_envio = datetime.now()
        contacto.save()

        registrar_envio(contacto, campana, exito=True)  # 📝 registro exitoso

    except Exception as e:
        print(f"❌ Error al procesar {nombre_completo}: {e}")
        registrar_envio(contacto, campana, exito=False)


def procesar_contactos_con_lista(contactos, mensaje, campana):
    from base.scripts.popups import cerrar_popups_visual
    from selenium import webdriver
    import random, time

    # ⚙️ Configuración estable del navegador Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36")
    options.add_argument('--disable-gpu')  # ✅ Evita errores gráficos
    options.add_argument('--no-sandbox')  # ✅ Estabilidad general
    options.add_argument('--disable-dev-shm-usage')  # ✅ Optimiza uso de memoria compartida
    # options.add_argument('--headless=new')  # ← si querés probar sin interfaz visible

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.linkedin.com")
    input("🔑 Inicia sesión en LinkedIn y presiona ENTER para continuar...")

    for idx, contacto in enumerate(contactos):
        cerrar_popups_visual(driver)
        buscar_contacto_y_enviar_mensaje(driver, contacto, mensaje, campana)
        cerrar_popups_visual(driver)
        time.sleep(random.uniform(3, 7))

        if idx > 0 and idx % 5 == 0:
            print("🧘 Pausa estratégica para refrescar navegador...")
            time.sleep(15)

    driver.quit()
    print(f"✅ Proceso completado: {len(contactos)} contactos procesados.")