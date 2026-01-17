import pandas as pd
from base.models import Contacto


def importar_contactos(archivo_excel):
    try:
        df = pd.read_excel(archivo_excel)
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return {"error": f"No se pudo abrir el archivo: {e}"}

    for index, row in df.iterrows():
        if "nombre" not in row or "linkedin_url" not in row:
            print(f"⚠️ Fila inválida en índice {index}: {row}")
            continue  # Saltar filas con datos incorrectos

        contacto, creado = Contacto.objects.get_or_create(
            nombre=row["nombre"],
            linkedin_url=row["linkedin_url"],
            defaults={"mensaje_enviado": False}
        )

        if creado:
            print(f"✅ Contacto agregado: {contacto.nombre}")
        else:
            print(f"⚠️ Contacto ya existe en la base de datos: {contacto.nombre}")

    return {"mensaje": "✅ Importación completada."}