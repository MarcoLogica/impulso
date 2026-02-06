from datetime import timedelta
from operator import truediv
from django.db import models
from django.contrib.auth.models import User
from django.db.models import BooleanField



class Pokemon(models.Model):
    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=200)
    descripcion =models.TextField(null=True,
                                blank=True)
    carta_valiosa = models.BooleanField(default=False)
    resistencia = models.CharField(max_length=200)
    impacto = models.CharField(max_length=200)
    numero_serie = models.CharField(max_length=200,
                                    null = True,
                                    blank = True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['fecha_creacion']



# sistema para gestión de inventario

from django.db import models

# Modelo para las Máquinas y Equipos
class MaquinaEquipo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)  # e.g., "grua horquilla", "apilador electrico"
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo para los Roles
class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo para las Personas
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Modelo para la Infraestructura (Ubicaciones)
class Ubicacion(models.Model):
    pasillo = models.CharField(max_length=50)
    columna = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)
    zona = models.CharField(max_length=100)  # e.g., "picking", "almacenaje"

    def __str__(self):
        return f"{self.pasillo}-{self.columna}-{self.nivel} ({self.zona})"

# Modelo para los Atributos a Revisar en los Inventarios
class AtributoRevisar(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo para los Tipos de Inventario
class TipoInventario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ejemplo_circunstancias = models.TextField()  # Para describir circunstancias en las que se usaría este tipo de inventario
    frecuencia = models.CharField(max_length=50)  # e.g., "diario", "mensual", "anual"
    objetivos = models.TextField()  # Objetivos como un campo de texto
    zonas_interes = models.ManyToManyField(Ubicacion)
    atributos_revisar = models.ManyToManyField(AtributoRevisar)

    def __str__(self):
        return self.nombre

# Modelo para los Recursos, relacionando con Máquinas, Personas e Infraestructura
# Modelo para los Recursos
class Recurso(models.Model):
    tipo = models.CharField(max_length=100)  # e.g., "Maquina", "Persona", "Ubicacion"
    nombre = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


# Modelo para la Planificación de Inventarios
# Eliminamos las referencias a Recurso en otros modelos donde corresponde
# Por ejemplo, en el modelo PlanInventario
class PlanInventario(models.Model):
    nombre = models.CharField(max_length=200)
    tipo_inventario = models.ForeignKey(TipoInventario, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='responsable')
    recursos = models.ManyToManyField(Recurso)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre


#/////////////////////////// APP FOTOS

from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

# ////////////////////////////////////////////////////////////////////////////////// RPA LOGICA ///////

from django.db import models



class Contacto(models.Model):
    nombre = models.CharField(max_length=255)
    linkedin_url = models.URLField(unique=True)
    mensaje_enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    industria = models.CharField(max_length=100, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    ETAPAS_VENTAS = [
        ('contacto', 'Contacto'),
        ('reunion', 'Reunión'),
        ('licitacion', 'Licitación'),
        ('cierre', 'Cierre'),
        ('postventa', 'PostVenta'),

    ]
    etapa_ventas = models.CharField(
        max_length=30,
        choices=ETAPAS_VENTAS,
        default='contacto'
    )


    def __str__(self):
        return self.nombre




class Mensaje(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class EjecucionRPA(models.Model):
        fecha_ejecucion = models.DateTimeField(auto_now_add=True)
        cantidad_objetivo = models.IntegerField()
        cantidad_enviados = models.IntegerField()
        cantidad_fallidos = models.IntegerField(default=0)
        estado = models.CharField(max_length=50)  # Ej: "completado", "error"

        def __str__(self):
            return f"Ejecutado el {self.fecha_ejecucion.strftime('%Y-%m-%d %H:%M:%S')}"


from django.db import models

class Campana(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    mensaje = models.TextField()
    industria = models.CharField(max_length=100, blank=True)
    cargo = models.CharField(max_length=100, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Envio(models.Model):
    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='envios')
    campana = models.ForeignKey('Campana', on_delete=models.CASCADE, related_name='envios')
    mensaje_enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    error_envio = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.contacto.nombre} en {self.campana.nombre}"


from django.db import models
from django.contrib.auth.models import User

class Iniciativa(models.Model):

    CATEGORIAS_MATERNAL = [
        ('hogar', 'Hogar y Logística'),
        ('crianza', 'Crianza y Desarrollo'),
        ('trabajo', 'Trabajo y Proyectos'),
        ('vinculos', 'Vínculos y Relaciones'),
        ('salud', 'Salud Mental y Emocional'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=120)
    objetivo = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    # ⭐ Nuevo campo
    categoria_maternal = models.CharField(
        max_length=20,
        choices=CATEGORIAS_MATERNAL,
        default='hogar'
    )

    def __str__(self):
        return self.nombre


class Fase(models.Model):
    iniciativa = models.ForeignKey(Iniciativa, related_name='fases', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    icono = models.CharField(max_length=5, default='📌')
    color_hex = models.CharField(max_length=7, default='#cccccc')  # formato tipo "#87CEFA"
    fecha_objetivo = models.DateField(blank=True, null=True)
    completado = models.BooleanField(default=False)
    reflexion = models.TextField(blank=True, null=True)
    publicado_en_feed = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.nombre} ({self.iniciativa.nombre})"

    from datetime import timedelta

    @property
    def fecha_objetivo_dinamica(self):
        tareas = self.tareas.all()
        fechas_finales = [t.fecha_inicio + timedelta(days=t.duracion_dias) for t in tareas]
        return max(fechas_finales) if fechas_finales else None



class Tarea(models.Model):
    fase = models.ForeignKey(Fase, related_name='tareas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    duracion_dias = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ], default='pendiente')
    notas = models.TextField(blank=True)
    fecha_completada = models.DateField(null=True, blank=True)  # 🟢 nuevo campo
    orden = models.PositiveIntegerField(default=0)
    delegado = models.ForeignKey(
            'RedApoyoUser',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name="tareas_delegadas"
        )

    def __str__(self):
        return self.nombre



from django.db import models

class Hito(models.Model):
    tarea = models.ForeignKey('Tarea', related_name='hitos', on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, help_text="Frase o nota significativa del hito")
    archivo = models.FileField(upload_to='hitos/', null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    series = models.PositiveIntegerField(null=True, blank=True, help_text="Número de series realizadas")
    repeticiones = models.PositiveIntegerField(null=True, blank=True, help_text="Número de repeticiones por serie")
    carga = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Carga utilizada (kg)")

    def __str__(self):
        return f"Hito de: {self.tarea.nombre}"



from django.db import models
from django.contrib.auth.models import User

class EventoAgenda(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('llamada', '📞 Llamada de reclutador'),
        ('entrevista_agendada', '🗓️ Entrevista agendada'),
        ('entrevista_realizada', '✅ Entrevista realizada'),
        ('oferta', '🎉 Oferta recibida'),
        ('avance', '👈Evento de avance'),
    ]




    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_evento = models.CharField(max_length=30, choices=TIPO_EVENTO_CHOICES)
    empresa = models.CharField(max_length=100)
    fecha_evento = models.DateField()
    comentario = models.TextField(blank=True)
    mostrar_en_feed = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_evento_display()} ({self.empresa})"


from django.db import models
from django.contrib.auth.models import User

class ProcesoSeleccion(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
    ]

    RESULTADOS = [
        ('positivo', 'Seleccionado'),
        ('negativo', 'No seleccionado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    resultado = models.CharField(max_length=30, choices=RESULTADOS, blank=True, null=True)
    comentario_final = models.TextField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.empresa} ({self.cargo})"


class HitoProceso(models.Model):
    TIPO_HITO = [
        ('contacto', 'Contacto inicial'),
        ('test_psico', 'Test psicológico'),
        ('entrevista_1', 'Entrevista 1'),
        ('entrevista_2', 'Entrevista 2'),
        ('entrevista_3', 'Entrevista 3'),
        ('fin_proceso', 'Fin del proceso'),
        ('resultado', 'Resultado / Feedback'),
    ]

    proceso = models.ForeignKey(ProcesoSeleccion, on_delete=models.CASCADE, related_name='hitos')
    tipo = models.CharField(max_length=20, choices=TIPO_HITO)
    fecha = models.DateField()
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha}"


class PublicacionFeed(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='feed_imagenes/', blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    # Reacciones emocionales
    me_gusta = models.ManyToManyField(User, related_name='reaccion_me_gusta', blank=True)
    animo = models.ManyToManyField(User, related_name='reaccion_animo', blank=True)
    fuerza = models.ManyToManyField(User, related_name='reaccion_fuerza', blank=True)
    tu_puedes = models.ManyToManyField(User, related_name='reaccion_tu_puedes', blank=True)
    felicidades = models.ManyToManyField(User, related_name='reaccion_felicidades', blank=True)

    def total_reacciones(self):
        return (
            self.me_gusta.count() +
            self.animo.count() +
            self.fuerza.count() +
            self.tu_puedes.count() +
            self.felicidades.count()
        )

    def __str__(self):
        return f"{self.usuario.username} publicó en el feed"


class ContactoLinkedIn(models.Model):
    nombre = models.CharField(max_length=200)
    perfil_linkedin = models.URLField()
    open_to_work = models.BooleanField(default=False)  # Detectado por visión RPA

    def __str__(self):
        return self.nombre

#////////////////////////////////////modelos CRM /////////////

from django.db import models

class Reunion(models.Model):
    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='reuniones')
    fecha = models.DateTimeField()
    modalidad = models.CharField(max_length=50)  # presencial, virtual, etc.
    responsable = models.CharField(max_length=100)
    resumen = models.TextField(blank=True)
    resultado = models.CharField(max_length=100, blank=True)  # ejemplo: respondió, sin interés, agendada

    def __str__(self):
        return f"Reunión con {self.contacto.nombre} el {self.fecha.strftime('%d-%m-%Y')}"

class Licitacion(models.Model):
    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='licitaciones')
    nombre_proyecto = models.CharField(max_length=255)
    fecha_envio_propuesta = models.DateTimeField()
    monto_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    documentos_adjuntos = models.TextField(blank=True)  # puede ser ruta o descripción
    estado = models.CharField(max_length=100)  # ejemplo: en evaluación, rechazado, preseleccionado

    def __str__(self):
        return f"Licitación: {self.nombre_proyecto} ({self.estado})"

class Cierre(models.Model):
    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='cierres')
    fecha_cierre = models.DateTimeField()
    tipo_cierre = models.CharField(max_length=50)  # exitoso, perdido, postergado
    monto_final = models.DecimalField(max_digits=12, decimal_places=2)
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Cierre {self.tipo_cierre} con {self.contacto.nombre}"

class PostVenta(models.Model):
    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='postventas')
    fecha_inicio = models.DateTimeField()
    tipo_servicio = models.CharField(max_length=100)  # soporte, capacitación, seguimiento
    nivel_satisfaccion = models.IntegerField(null=True, blank=True)  # escala 1–5
    comentarios_cliente = models.TextField(blank=True)
    acciones_realizadas = models.TextField(blank=True)

    def __str__(self):
        return f"PostVenta para {self.contacto.nombre} desde {self.fecha_inicio.strftime('%d-%m-%Y')}"

class Interaccion(models.Model):
    TIPO_INTERACCION = [
        ('mensaje', 'Mensaje'),
        ('respuesta', 'Respuesta'),
        ('reunion', 'Reunión'),
        ('llamada', 'Llamada'),
        ('seguimiento', 'Seguimiento'),
        ('otro', 'Otro'),
    ]

    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='interacciones')
    tipo = models.CharField(max_length=50, choices=TIPO_INTERACCION)
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} con {self.contacto.nombre}"

class HistorialEtapa(models.Model):
    contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE, related_name='historial_etapas')
    etapa_anterior = models.CharField(max_length=30, choices=Contacto.ETAPAS_VENTAS)
    etapa_nueva = models.CharField(max_length=30, choices=Contacto.ETAPAS_VENTAS)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.contacto.nombre}: {self.etapa_anterior} → {self.etapa_nueva}"


# RED DE APOYO - PERFILAMIENTO DE USUARIOS

class RedApoyoUser(models.Model):
    madre = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="red_apoyo"
    )
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    codigo_acceso = models.CharField(max_length=20, unique=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} (Apoyo de {self.madre.username})"
