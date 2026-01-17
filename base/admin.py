from django.contrib import admin
from .models import Pokemon, Contacto, EjecucionRPA, Mensaje, Campana, Envio, Hito, Fase, Tarea
from .models import UploadedImage, Reunion


admin.site.register(Pokemon)
admin.site.register(UploadedImage)
admin.site.register(Contacto)
admin.site.register(Mensaje)
admin.site.register(EjecucionRPA)
admin.site.register(Campana)
admin.site.register(Envio)
admin.site.register(Hito)
admin.site.register(Fase)
admin.site.register(Tarea)
admin.site.register(Reunion)


# Register your models here.
