from base.models import Envio
from datetime import datetime

def registrar_envio(contacto, campana, exito=True):
    Envio.objects.create(
        contacto=contacto,
        campana=campana,
        mensaje_enviado=exito,
        fecha_envio=datetime.now() if exito else None,
        error_envio=not exito
    )