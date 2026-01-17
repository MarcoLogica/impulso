import os
import sys
import django
import cv2
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from base.models import ContactoLinkedIn

# 📦 Ajustar entorno Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # sube desde /scripts/ hacia /src/
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon.settings')  # ← asegúrate que tu proyecto se llama 'pokemon'
django.setup()

# 🚀 Configura Selenium en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1200,800")
driver = webdriver.Chrome(options=chrome_options)

# 🔍 Detectar franja “Open to Work”
def detectar_open_to_work(img_path):
    imagen = cv2.imread(img_path)
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Rango de color verde típico (ajustable si es necesario)
    verde_bajo = np.array([45, 100, 100])
    verde_alto = np.array([75, 255, 255])

    mascara = cv2.inRange(hsv, verde_bajo, verde_alto)
    porcentaje = (np.count_nonzero(mascara) / mascara.size) * 100

    return porcentaje > 1.0  # más del 1% verde: posible franja activa

# 🧠 Recorrer contactos sin marcar
contactos = ContactoLinkedIn.objects.filter(open_to_work=False)
total = contactos.count()
detectados = 0

for c in contactos:
    try:
        print(f"Analizando: {c.nombre}")
        driver.get(c.perfil_linkedin)
        time.sleep(5)  # esperar que cargue bien

        screenshot_path = f"temp/{c.nombre}_perfil.png"
        driver.save_screenshot(screenshot_path)

        if detectar_open_to_work(screenshot_path):
            c.open_to_work = True
            c.save()
            detectados += 1
            print(f"✅ {c.nombre} marcado como Open to Work")

        os.remove(screenshot_path)

    except Exception as e:
        print(f"❌ Error con {c.nombre}: {e}")

driver.quit()

# 📊 Resumen final
print(f"🎯 RPA completado: {detectados} marcados como Open to Work / {total} analizados")