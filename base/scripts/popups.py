from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def cerrar_popups_visual(driver):
    try:
        # Buscar el texto específico del modal
        modal_texto = "¿Seguro que quieres eliminar este mensaje?"
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{modal_texto}')]"))
        )

        # Clic en botón "Descartar" si aparece
        boton_descartar = driver.find_element(By.XPATH, "//button[contains(., 'Descartar')]")
        boton_descartar.click()
        print("🧹 Popup detectado y cerrado.")
    except (NoSuchElementException, TimeoutException):
        print("✅ No hay popups activos, continuando...")