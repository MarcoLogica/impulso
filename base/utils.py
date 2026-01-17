from .models import Fase, Tarea
from datetime import date, timedelta

from .models import Fase, Tarea
from datetime import date, timedelta

def crear_plan_base_para_iniciativa(iniciativa):
    estructura = [
        ("Diagnostico y Proposito", "🧠", "#FFD700", [
            "Definir objetivo profesional",
            "Elegir industria y tipo de empresa",
            "Detectar habilidades clave"
        ]),
        ("Documentacion esencial", "📄", "#90EE90", [
            "Optimizar CV para ATS",
            "Actualizar perfil de LinkedIn",
            "Redactar pitch personal"
        ]),
        ("Posicionamiento digital", "🌐", "#87CEFA", [
            "Publicar contenido en LinkedIn",
            "Conectar con referentes del rubro",
            "Participar en debates del sector"
        ]),
        ("Aplicacion y contacto", "📬", "#FFA07A", [
            "Identificar 10 empresas objetivo",
            "Enviar 5 CVs personalizados",
            "Contactar reclutadores clave"
        ]),
        ("Feedback y reajuste", "🔁", "#D8BFD8", [
            "Registrar entrevistas y respuestas",
            "Pedir retroalimentacion",
            "Reajustar estrategia si es necesario"
        ])
    ]

    hoy = date.today()

    for index_fase, (nombre_fase, icono, color_hex, tareas) in enumerate(estructura, start=1):
        fase = Fase.objects.create(
            iniciativa=iniciativa,
            nombre=nombre_fase,
            orden=index_fase,
            icono=icono,
            color_hex=color_hex
        )
        for i, nombre_tarea in enumerate(tareas):
            Tarea.objects.create(
                fase=fase,
                nombre=nombre_tarea,
                fecha_inicio=hoy + timedelta(days=i + index_fase),
                duracion_dias=2
            )

from .models import Tarea

def calcular_avance_general(iniciativa):
    tareas = Tarea.objects.filter(fase__iniciativa=iniciativa)
    total = tareas.count()
    completadas = tareas.filter(estado='completada').count()
    return round((completadas / total) * 100) if total > 0 else 0

# utils.py

def generar_mensaje_motivacional(progreso):
    if progreso == 0:
        return "🚀 Es momento de iniciar. Cada tarea es un paso hacia tu meta."
    elif progreso < 40:
        return "💪 ¡Buen arranque! Tu constancia marcará la diferencia."
    elif progreso < 80:
        return "🔥 Vas por muy buen camino. No bajes el ritmo."
    elif progreso < 100:
        return "🏁 ¡Estás a punto de cerrar! Da ese último empuje."
    else:
        return "🎉 Plan completado con éxito. ¡Impecable gestión!"