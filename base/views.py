from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django import forms
from .form import MaquinaEquipoForm, RolForm, PersonaForm, UbicacionForm, AtributoRevisarForm, TipoInventarioForm, RecursoForm, PlanInventarioForm
from django.utils.translation.template import context_re
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required



from base.models import Pokemon, MaquinaEquipo, Rol, Persona, Ubicacion, PlanInventario, AtributoRevisar, TipoInventario, Recurso



class ListaPokemon(ListView):
    model = Pokemon
    context_object_name = 'pokemon'

#crear clientes

class CrearPokemon(CreateView):
    model= Pokemon
    fields = '__all__'
    success_url = reverse_lazy('pokemon')

class DetallePokemon(DetailView):
    model = Pokemon
    context_object_name = 'detpokemon'

# ///////////////////////////


from django.shortcuts import render, redirect
from .models import (
    MaquinaEquipo, Rol, Persona, Ubicacion,
    AtributoRevisar, TipoInventario, Recurso,
    PlanInventario
)


def manage_maquinas(request):
    if request.method == "POST":
        form = MaquinaEquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_maquinas')
    else:
        form = MaquinaEquipoForm()
    maquinas = MaquinaEquipo.objects.all()
    return render(request, 'base/manage_maquinas.html', {'form': form, 'maquinas': maquinas})

def manage_roles(request):
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_roles')
    else:
        form = RolForm()
    roles = Rol.objects.all()
    return render(request, 'base/manage_roles.html', {'form': form, 'roles': roles})

def manage_personas(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_personas')
    else:
        form = PersonaForm()
    personas = Persona.objects.all()
    return render(request, 'base/manage_personas.html', {'form': form, 'personas': personas})

def manage_ubicaciones(request):
    if request.method == "POST":
        form = UbicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_ubicaciones')
    else:
        form = UbicacionForm()
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'base/manage_ubicaciones.html', {'form': form, 'ubicaciones': ubicaciones})

def manage_atributos(request):
    if request.method == "POST":
        form = AtributoRevisarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_atributos')
    else:
        form = AtributoRevisarForm()
    atributos = AtributoRevisar.objects.all()
    return render(request, 'base/manage_atributos.html', {'form': form, 'atributos': atributos})

def manage_tipos_inventario(request):
    if request.method == "POST":
        form = TipoInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_tipos_inventario')
    else:
        form = TipoInventarioForm()
    tipos_inventario = TipoInventario.objects.all()
    return render(request, 'base/manage_tipos_inventario.html', {'form': form, 'tipos_inventario': tipos_inventario})



def recurso_list(request):
    recursos = Recurso.objects.all()
    return render(request, 'base/recurso_list.html', {'recursos': recursos})


def recurso_create(request):
    if request.method == "POST":
        form = RecursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recurso_list')
    else:
        form = RecursoForm()
    return render(request, 'base/recurso_form.html', {'form': form})

def recurso_update(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    if request.method == "POST":
        form = RecursoForm(request.POST, instance=recurso)
        if form.is_valid():
            form.save()
            return redirect('recurso_list')
    else:
        form = RecursoForm(instance=recurso)
    return render(request, 'base/recurso_form.html', {'form': form})

def recurso_delete(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    if request.method == "POST":
        recurso.delete()
        return redirect('recurso_list')
    return render(request, 'base/recurso_confirm_delete.html', {'recurso': recurso})

def manage_planes_inventario(request):
    if request.method == "POST":
        form = PlanInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_planes_inventario')
    else:
        form = PlanInventarioForm()
    planes_inventario = PlanInventario.objects.all()
    return render(request, 'base/manage_planes_inventario.html', {'form': form, 'planes_inventario': planes_inventario})



#///// sitio gestion de imagenes ///////////

from django.shortcuts import render
from .models import UploadedImage

def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        UploadedImage.objects.create(image=image)
    return render(request, "base/upload_image.html")

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden


@csrf_exempt  # Exime la protección CSRF para pruebas, no se recomienda en producción
def administrador(request):
    if request.method == "POST":
        image = request.FILES.get("image")  # Verifica si el archivo fue enviado
        if image:
            image_path = f"media/{image.name}"
            with open(image_path, "wb") as f:
                for chunk in image.chunks():
                    f.write(chunk)
            return render(request, "base/administrador.html", {"image_url": f"/{image_path}"})
        return JsonResponse({"error": "No se envió ninguna imagen."}, status=400)
    return JsonResponse({"error": "Método no permitido."}, status=405)


#///////////////////////////////////////////////////////////////// RPA ///////////////

from django.shortcuts import render
from django.http import JsonResponse
from base.models import Contacto, EjecucionRPA
# from base.scripts.linkedin_bot import procesar_contactos
import datetime

# 🖥️ Vista del Dashboard
def dashboard(request):
    ejecuciones = EjecucionRPA.objects.order_by("-fecha_ejecucion")[:5]  # Últimas 5 ejecuciones
    contactos_pendientes = Contacto.objects.filter(mensaje_enviado=False).count()  # Contactos sin procesar
    return render(request, "base/dashboard.html", {
        "ejecuciones": ejecuciones,
        "contactos_pendientes": contactos_pendientes
    })

# 🚀 Función para ejecutar el RPA
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Solo para pruebas
def ejecutar_rpa(request):
    if request.method == "POST":
        try:
            limite = int(request.POST.get("limite", 10))  # ✅ Obtener el límite de contactos
            procesar_contactos(limite)  # ✅ Ejecutar el RPA con el límite indicado
            return JsonResponse({"mensaje": f"✅ RPA ejecutado con límite de {limite} contactos."})
        except Exception as e:
            return JsonResponse({"error": f"❌ Error al ejecutar el RPA: {str(e)}"}, status=500)

    return JsonResponse({"error": "❌ Método no permitido"}, status=405)  # ✅ Código 405 para error de método



from django.shortcuts import render
from django.http import JsonResponse
from base.scripts.importar_contactos import importar_contactos
import os


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from base.models import Contacto

import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.models import Contacto

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from base.models import Contacto
from django.db import IntegrityError
import pandas as pd

@csrf_exempt
def cargar_excel(request):
    if request.method == "POST" and request.FILES.get("archivo"):
        archivo = request.FILES["archivo"]

        try:
            df = pd.read_excel(archivo)
            df.columns = df.columns.str.strip().str.lower()  # Normalizamos nombres de columna
        except Exception as e:
            return JsonResponse({"error": f"❌ Error al procesar el archivo: {str(e)}"}, status=400)

        columnas_requeridas = {"nombre", "linkedin_url"}
        if not columnas_requeridas.issubset(set(df.columns)):
            return JsonResponse({
                "error": "❌ El archivo debe tener columnas: 'nombre' y 'linkedin_url'."
            }, status=400)

        nuevos_contactos = 0
        duplicados = 0

        for _, fila in df.iterrows():
            nombre = fila["nombre"].strip()
            linkedin_url = fila["linkedin_url"].strip()
            industria = fila.get("industria", None)
            cargo = fila.get("cargo", None)

            try:
                Contacto.objects.create(
                    nombre=nombre,
                    linkedin_url=linkedin_url,
                    industria=industria.strip() if isinstance(industria, str) else None,
                    cargo=cargo.strip() if isinstance(cargo, str) else None,
                )
                nuevos_contactos += 1
            except IntegrityError:
                duplicados += 1
                continue

        return JsonResponse({
            "mensaje": f"✅ {nuevos_contactos} contactos importados exitosamente.",
            "omitidos": f"⚠️ {duplicados} duplicados fueron omitidos."
        })

    return JsonResponse({"error": "❌ No se recibió un archivo válido."}, status=400)

# //////////////////////////////////////panel de control /////////////

from django.db.models.functions import TruncDate
from django.db.models import Count, Q

def metricas_grafico_1(request):
    resultados = (
        Contacto.objects
        .annotate(fecha=TruncDate("fecha_envio"))
        .values("fecha")
        .annotate(total=Count("id"))
        .order_by("fecha")
    )
    return JsonResponse({"labels": [r["fecha"].strftime("%Y-%m-%d") for r in resultados],
                         "data": [r["total"] for r in resultados]})

def metricas_grafico_2(request):
    resultados = (
        Contacto.objects
        .filter(mensaje_enviado=True)
        .annotate(fecha=TruncDate("fecha_envio"))
        .values("fecha")
        .annotate(total=Count("id"))
        .order_by("fecha")
    )
    return JsonResponse({"labels": [r["fecha"].strftime("%Y-%m-%d") for r in resultados],
                         "data": [r["total"] for r in resultados]})

def resumen_base_vs_fallidos(request):
    total = Contacto.objects.count()
    enviados = Contacto.objects.filter(mensaje_enviado=True).count()
    fallidos = total - enviados

    return JsonResponse({
        "labels": ["Contactos totales", "Enviados con éxito", "Fallidos"],
        "data": [total, enviados, fallidos]
    })

from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from base.models import Contacto

def metricas_total_dia(request):
    resultados = (
        Contacto.objects
        .exclude(fecha_envio__isnull=True)
        .annotate(fecha=TruncDate("fecha_envio"))
        .values("fecha")
        .annotate(total=Count("id"))
        .order_by("fecha")
    )

    return JsonResponse({
        "labels": [r["fecha"].strftime("%Y-%m-%d") for r in resultados],
        "data": [r["total"] for r in resultados]
    })

from django.http import JsonResponse
from base.models import Contacto

def resumen_contactos(request):
    procesados = Contacto.objects.filter(mensaje_enviado=True).count()
    pendientes = Contacto.objects.filter(mensaje_enviado=False).count()

    return JsonResponse({
        "labels": ["Procesados", "Pendientes"],
        "data": [procesados, pendientes]
    })

from django.shortcuts import render
from .models import Contacto

def vista_contactos(request):
    contactos = Contacto.objects.all()

    # 🔍 Filtro por etapa
    etapa = request.GET.get('etapa')
    if etapa:
        contactos = contactos.filter(etapa_ventas=etapa)

    # 🔎 Filtro por nombre
    nombre = request.GET.get('nombre')
    if nombre:
        contactos = contactos.filter(nombre__icontains=nombre)

    total = contactos.count()
    enviados = contactos.filter(mensaje_enviado=True).count()

    return render(request, 'base/contactos.html', {
        'contactos': contactos,
        'total': total,
        'enviados': enviados,
        'etapa_seleccionada': etapa,
        'nombre_buscado': nombre
    })

from django.shortcuts import redirect
from .models import Contacto

def eliminar_multiples(request):
    if request.method == 'POST':
        ids = request.POST.getlist('seleccionados')
        if ids:
            Contacto.objects.filter(id__in=ids).delete()
    return redirect('vista_contactos')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Contacto

def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)

    if request.method == 'POST':
        contacto.nombre = request.POST.get('nombre', contacto.nombre)
        contacto.email = request.POST.get('email', contacto.email)
        contacto.save()
        return redirect('vista_contactos')

    return render(request, 'base/editar_contacto.html', {'contacto': contacto})

from django.shortcuts import get_object_or_404, redirect
from .models import Contacto

def eliminar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    contacto.delete()
    return redirect('vista_contactos')


from django.shortcuts import render, redirect
from .models import Campana

def vista_campanas(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        mensaje = request.POST.get("mensaje")
        industria = request.POST.get("industria", "")
        cargo = request.POST.get("cargo", "")

        if nombre and mensaje:
            Campana.objects.create(
                nombre=nombre,
                mensaje=mensaje,
                industria=industria,
                cargo=cargo
            )
            return redirect("vista_campanas")

    campanas = Campana.objects.all().order_by("-fecha_creacion")
    return render(request, "base/campanas.html", {"campanas": campanas})

from django.shortcuts import render, redirect
from base.models import Campana, Contacto

from django.shortcuts import render
from base.models import Campana, Contacto

def ejecutar_campana(request):
    mensaje = None
    coincidencias = None
    contactos = []
    mensaje_confirmacion = ""

    if request.method == "POST":
        accion = request.POST.get("accion")
        campana_id = request.POST.get("campana_id")
        limite = int(request.POST.get("limite", 10))

        campana = Campana.objects.get(id=campana_id)

        contactos_filtrados = Contacto.objects.filter(
            mensaje_enviado=False,
            industria__icontains=campana.industria,
            cargo__icontains=campana.cargo
        )[:limite]

        if accion == "preview":
            print("🔍 Se presionó 'Ver coincidencias'")
            mensaje = campana.mensaje
            contactos = contactos_filtrados
            coincidencias = Contacto.objects.filter(
                mensaje_enviado=False,
                industria__icontains=campana.industria,
                cargo__icontains=campana.cargo
            ).count()

        elif accion == "ejecutar":
            print("🎯 Entrando en la ejecución del RPA desde la vista")
            print(f"🧩 Campaña: {campana.nombre} — Contactos: {len(contactos_filtrados)}")
            procesar_contactos_con_lista(contactos_filtrados, campana.mensaje, campana)
            mensaje_confirmacion = "✅ El RPA fue ejecutado correctamente con esta campaña."

    campanas = Campana.objects.all().order_by("-fecha_creacion")

    return render(request, "base/ejecutar_campana.html", {
        "campanas": campanas,
        "contactos": contactos,
        "mensaje": mensaje,
        "coincidencias": coincidencias,
        "mensaje_confirmacion": mensaje_confirmacion
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def editar_campana(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)

    if request.method == "POST":
        campana.nombre = request.POST.get("nombre")
        campana.industria = request.POST.get("industria")
        campana.cargo = request.POST.get("cargo")
        campana.mensaje = request.POST.get("mensaje")
        campana.save()
        messages.success(request, "✅ Campaña actualizada con éxito.")
        return redirect("vista_campanas")  # reemplaza con el nombre real de la vista

    return render(request, "base/editar_campana.html", {"campana": campana})


def eliminar_campana(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)
    campana.delete()
    messages.success(request, "🗑️ Campaña eliminada.")
    return redirect("vista_campanas")  # reemplaza con el nombre real de tu vista de campañas


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contacto

def corregir_mojibake(texto):
    if isinstance(texto, str):
        try:
            return texto.encode('latin1').decode('utf-8')
        except UnicodeError:
            return texto
    return texto

@csrf_exempt
def corregir_nombres_en_modelo(request):
    contactos_corregidos = 0

    for contacto in Contacto.objects.all():
        nombre_original = contacto.nombre
        nombre_corregido = corregir_mojibake(nombre_original)

        if nombre_original != nombre_corregido:
            contacto.nombre = nombre_corregido
            contacto.save(update_fields=['nombre'])
            contactos_corregidos += 1

    return JsonResponse({
        'status': 'ok',
        'mensaje': f'Se corrigieron {contactos_corregidos} nombres en la base de datos.'
    })

from django.shortcuts import render, get_object_or_404
from .models import Campana

def ver_metricas(request, campaña_id):
    campaña = get_object_or_404(Campana, id=campaña_id)
    contactos = campaña.contactos.all()

    total = contactos.count()
    enviados = contactos.filter(mensaje_enviado=True).count()
    fallidos = contactos.filter(error_envio=True).count() if hasattr(contactos.first(), 'error_envio') else 0
    progreso = round((enviados / total) * 100, 1) if total else 0

    context = {
        "campaña": campaña,
        "total": total,
        "enviados": enviados,
        "fallidos": fallidos,
        "progreso": progreso,
    }

    return render(request, "base/campañas/metricas.html", context)

# ////////////////// IMPULSO

from django.shortcuts import render, redirect, get_object_or_404
from .models import Iniciativa, Fase, Tarea
from .forms import IniciativaForm

def lista_iniciativas(request):
    iniciativas = Iniciativa.objects.filter(usuario=request.user)
    return render(request, 'base/lista_iniciativas.html', {'iniciativas': iniciativas})

from django.shortcuts import render, redirect
from .forms import IniciativaForm
from .utils import crear_plan_base_para_iniciativa  # ✅ Importar script de generación
from .models import Iniciativa

def crear_iniciativa(request):
    if request.method == 'POST':
        formulario = IniciativaForm(request.POST)
        if formulario.is_valid():
            iniciativa = formulario.save(commit=False)
            iniciativa.usuario = request.user
            iniciativa.save()
            crear_plan_base_para_iniciativa(iniciativa)  # ✅ Generación automática del plan
            return redirect('detalle_iniciativa', iniciativa_id=iniciativa.id)
    else:
        formulario = IniciativaForm()
    return render(request, 'base/crear_iniciativa.html', {'formulario': formulario})

def detalle_iniciativa(request, iniciativa_id):
    iniciativa = get_object_or_404(Iniciativa, id=iniciativa_id, usuario=request.user)
    return render(request, 'base/detalle_iniciativa.html', {'iniciativa': iniciativa})


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import date, timedelta
from .models import Iniciativa, Tarea, Fase
from .utils import calcular_avance_general
from .utils import generar_mensaje_motivacional

from datetime import timedelta
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db.models import Prefetch
from .models import Iniciativa, Fase, Tarea
from .utils import calcular_avance_general, generar_mensaje_motivacional  # si usas funciones externas
def vista_plan(request, iniciativa_id):
    hoy = timezone.now().date()
    iniciativa = get_object_or_404(Iniciativa, id=iniciativa_id, usuario=request.user)

    # 🔧 Ordenar tareas por 'orden' dentro de cada fase
    tareas_ordenadas = Tarea.objects.order_by('orden')
    fases = iniciativa.fases.prefetch_related(
        Prefetch('tareas', queryset=tareas_ordenadas)
    ).order_by('orden')

    tareas = Tarea.objects.filter(fase__iniciativa=iniciativa)

    # 🔥 AGREGADO: marcar tareas retrasadas dinámicamente
    from datetime import timedelta
    for fase in fases:
        for tarea in fase.tareas.all():
            if tarea.fecha_inicio:
                fecha_objetivo = tarea.fecha_inicio + timedelta(days=tarea.duracion_dias)
                tarea.retrasada = (
                    tarea.estado != 'completada' and fecha_objetivo < hoy
                )
            else:
                tarea.retrasada = False

    # KPIs principales
    total_tareas = tareas.count()
    tareas_completadas = tareas.filter(estado='completada').count()
    tareas_pendientes = tareas.exclude(estado='completada').count()

    # 🔥 KPI retrasadas basado en la misma lógica
    tareas_retrasadas = sum(
        1 for t in tareas
        if t.estado != 'completada'
        and t.fecha_inicio
        and (t.fecha_inicio + timedelta(days=t.duracion_dias)) < hoy
    )

    total_fases = fases.count()

    # Fecha fin estimada
    fechas_estimadas = [
        t.fecha_inicio + timedelta(days=t.duracion_dias)
        for t in tareas if t.fecha_inicio
    ]
    fecha_fin_estimada = max(fechas_estimadas) if fechas_estimadas else None
    dias_restantes = (fecha_fin_estimada - hoy).days if fecha_fin_estimada else None

    # Última tarea completada
    ultima_tarea_completada = tareas.filter(
        estado='completada',
        fecha_completada__isnull=False
    ).order_by('-fecha_completada').first()

    # Avance semanal
    hace_una_semana = hoy - timedelta(days=7)
    avance_semanal = tareas.filter(
        estado='completada',
        fecha_completada__gte=hace_una_semana
    ).count()

    # Fase más activa
    fase_mas_activa = None
    max_completadas = 0
    for fase in fases:
        completadas = fase.tareas.filter(estado='completada').count()
        if completadas > max_completadas:
            max_completadas = completadas
            fase_mas_activa = fase

    # Próxima tarea
    proxima_tarea = tareas.exclude(estado='completada').filter(
        fecha_inicio__gte=hoy
    ).order_by('fecha_inicio').first()

    # Progreso general
    progreso_total = calcular_avance_general(iniciativa)

    # Mensaje motivacional dinámico
    mensaje = generar_mensaje_motivacional(progreso_total)

    return render(request, 'base/vista_plan.html', {
        'iniciativa': iniciativa,
        'fases': fases,
        'progreso_total': progreso_total,
        'total_tareas': total_tareas,
        'tareas_completadas': tareas_completadas,
        'tareas_pendientes': tareas_pendientes,
        'tareas_retrasadas': tareas_retrasadas,
        'total_fases': total_fases,
        'fecha_fin_estimada': fecha_fin_estimada,
        'dias_restantes': dias_restantes,
        'ultima_tarea_completada': ultima_tarea_completada,
        'avance_semanal': avance_semanal,
        'fase_mas_activa': fase_mas_activa,
        'proxima_tarea': proxima_tarea,
        'mensaje_motivacional': mensaje
    })

from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from .models import Tarea


@require_POST
def actualizar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, fase__iniciativa__usuario=request.user)
    if tarea.estado != 'completada':
        tarea.estado = 'completada'
        tarea.fecha_completada = date.today()  # 🟢 registramos cuándo
        tarea.save()
    return redirect('vista_plan', iniciativa_id=tarea.fase.iniciativa.id)

from .models import Fase
from .utils import calcular_avance_general

def vista_fase_detalle(request, fase_id):
    fase = get_object_or_404(Fase, id=fase_id, iniciativa__usuario=request.user)
    tareas = fase.tareas.all().order_by('fecha_inicio')
    progreso_total = calcular_avance_general(fase.iniciativa)
    fases_siblings = fase.iniciativa.fases.order_by('orden')

    return render(request, 'base/fase_detalle.html', {
        'fase': fase,
        'tareas': tareas,
        'progreso_total': progreso_total,
        'fases': fases_siblings
    })

from django.shortcuts import render
from datetime import date, timedelta
from .models import Iniciativa

def gantt_general(request):
    iniciativas = Iniciativa.objects.filter(usuario=request.user).prefetch_related('fases__tareas').order_by('-id')
    datos_gantt = []
    px_por_dia = 20

    fechas_inicio = []
    fechas_fin = []

    for ini in iniciativas:
        for fase in ini.fases.all():
            tareas = fase.tareas.order_by('fecha_inicio')
            if tareas.exists():
                inicio = tareas.first().fecha_inicio
                fin = max([t.fecha_inicio + timedelta(days=t.duracion_dias) for t in tareas])
                fechas_inicio.append(inicio)
                fechas_fin.append(fin)

    fecha_inicio_base = min(fechas_inicio) if fechas_inicio else date.today()
    fecha_max = max(fechas_fin) if fechas_fin else fecha_inicio_base + timedelta(days=30)

    rango_dias = (fecha_max - fecha_inicio_base).days + 1
    fechas_gantt = [fecha_inicio_base + timedelta(days=i) for i in range(rango_dias)]

    # ✅ Línea roja: desplazamiento exacto desde el primer día del Gantt
    hoy = date.today()
    dias_desde_inicio = (hoy - fecha_inicio_base).days
    hoy_offset_px = dias_desde_inicio * px_por_dia if dias_desde_inicio >= 0 else None

    for ini in iniciativas:
        for fase in ini.fases.all():
            tareas = fase.tareas.order_by('fecha_inicio')
            if tareas.exists():
                inicio = tareas.first().fecha_inicio
                fin = max([t.fecha_inicio + timedelta(days=t.duracion_dias) for t in tareas])
                offset_dias = (inicio - fecha_inicio_base).days
                duracion_dias = max((fin - inicio).days, 1)
                datos_gantt.append({
                    'label': fase.nombre,
                    'nombre_iniciativa': ini.nombre,
                    'color': fase.color_hex,
                    'offset_px': offset_dias * px_por_dia,
                    'ancho_px': duracion_dias * px_por_dia,
                    'iniciativa_id': ini.id
                })

    return render(request, 'base/gantt_general.html', {
        'datos_gantt': datos_gantt,
        'fecha_inicio': fecha_inicio_base,
        'fechas_gantt': fechas_gantt,
        'px_por_dia': px_por_dia,
        'hoy_offset_px': hoy_offset_px
    })


def editar_iniciativa(request, pk):
    iniciativa = get_object_or_404(Iniciativa, id=pk, usuario=request.user)
    if request.method == 'POST':
        form = IniciativaForm(request.POST, instance=iniciativa)
        if form.is_valid():
            form.save()
            return redirect('vista_plan', iniciativa_id=iniciativa.id)
    else:
        form = IniciativaForm(instance=iniciativa)
    return render(request, 'base/editar_iniciativa.html', {'form': form, 'iniciativa': iniciativa})

def eliminar_iniciativa(request, pk):
    iniciativa = get_object_or_404(Iniciativa, id=pk, usuario=request.user)
    if request.method == 'POST':
        iniciativa.delete()
        return redirect('lista_iniciativas')  # o 'gantt_general' si prefieres
    return render(request, 'base/eliminar_confirmacion.html', {'iniciativa': iniciativa})

from django.shortcuts import render, get_object_or_404, redirect
from .forms import TareaForm
from .models import Tarea

def editar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, id=pk, fase__iniciativa__usuario=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('vista_plan', iniciativa_id=tarea.fase.iniciativa.id)
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'base/editar_tarea.html', {'form': form, 'tarea': tarea})

from .forms import IniciativaForm
from .models import Iniciativa

def crear_iniciativa_personalizada(request):
    form = IniciativaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        iniciativa = form.save(commit=False)
        iniciativa.usuario = request.user
        iniciativa.save()
        return redirect('vista_plan', iniciativa_id=iniciativa.id)
    return render(request, 'base/crear_iniciativa_personalizada.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import FaseForm
from .models import Iniciativa

def crear_fase(request, iniciativa_id):
    iniciativa = get_object_or_404(Iniciativa, id=iniciativa_id, usuario=request.user)
    form = FaseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        fase = form.save(commit=False)
        fase.iniciativa = iniciativa
        fase.save()
        return redirect('vista_plan', iniciativa_id=iniciativa.id)
    return render(request, 'base/crear_fase.html', {
        'form': form,
        'iniciativa': iniciativa
    })
from .forms import TareaForm

def crear_tarea_suelta(request, iniciativa_id):
    iniciativa = get_object_or_404(Iniciativa, id=iniciativa_id, usuario=request.user)
    form = TareaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tarea = form.save(commit=False)
        tarea.iniciativa = iniciativa
        tarea.fase = None  # Tarea suelta, sin fase
        tarea.save()
        return redirect('vista_plan', iniciativa_id=iniciativa.id)
    return render(request, 'base/crear_tarea_suelta.html', {
        'form': form,
        'iniciativa': iniciativa
    })

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Max
from .models import Fase, Tarea
from .forms import TareaForm

def crear_tarea_en_fase(request, fase_id):
    fase = get_object_or_404(Fase, id=fase_id, iniciativa__usuario=request.user)
    form = TareaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        tarea = form.save(commit=False)
        tarea.fase = fase

        # 🧠 Asignar orden automáticamente al final
        ultimo_orden = Tarea.objects.filter(fase=fase).aggregate(Max('orden'))['orden__max'] or 0
        tarea.orden = ultimo_orden + 1

        tarea.save()
        messages.success(request, "Tarea creada exitosamente.")
        return redirect('vista_plan', iniciativa_id=fase.iniciativa.id)

    return render(request, 'base/crear_tarea_en_fase.html', {
        'form': form,
        'fase': fase
    })

from .models import Fase
from .forms import FaseForm
from django.shortcuts import get_object_or_404, redirect, render

def editar_fase(request, fase_id):
    fase = get_object_or_404(Fase, id=fase_id, iniciativa__usuario=request.user)
    form = FaseForm(request.POST or None, instance=fase)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('vista_plan', iniciativa_id=fase.iniciativa.id)

    return render(request, 'base/editar_fase.html', {
        'form': form,
        'fase': fase,
        'iniciativa': fase.iniciativa
    })

# Hitos

from django.shortcuts import redirect, get_object_or_404, render
from .models import Tarea
from .forms import HitoForm

def marcar_tarea_completada(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, fase__iniciativa__usuario=request.user)

    if request.method == 'POST':
        form = HitoForm(request.POST, request.FILES)
        if form.is_valid():
            hito = form.save(commit=False)
            hito.tarea = tarea
            hito.save()
            tarea.estado = 'completada'
            tarea.fecha_completada = timezone.now().date()
            tarea.save()
            return redirect('vista_plan', iniciativa_id=tarea.fase.iniciativa.id)
    else:
        form = HitoForm()

    return render(request, 'base/registrar_hito.html', {
        'tarea': tarea,
        'form': form
    })


# agenda

from django.shortcuts import render, redirect
from .models import EventoAgenda
from .forms import EventoAgendaForm
from django.contrib.auth.decorators import login_required

@login_required
def registrar_evento(request):
    if request.method == 'POST':
        form = EventoAgendaForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            return redirect('mi_agenda')
    else:
        form = EventoAgendaForm()
    return render(request, 'base/registrar_evento.html', {'form': form})

@login_required
def mi_agenda(request):
    eventos = EventoAgenda.objects.filter(usuario=request.user).order_by('-fecha_evento')
    return render(request, 'base/mi_agenda.html', {'eventos': eventos})


from django.utils.timezone import now

def feed_comunitario(request):
    eventos = EventoAgenda.objects.filter(mostrar_en_feed=True).order_by('-creado')[:30]

    hoy = now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())

    eventos_semana = EventoAgenda.objects.filter(
        mostrar_en_feed=True,
        fecha_evento__gte=inicio_semana
    )

    resumen = {
        'llamados': eventos_semana.filter(tipo_evento='llamada').count(),
        'entrevistas_agendadas': eventos_semana.filter(tipo_evento='entrevista_agendada').count(),
        'entrevistas_realizadas': eventos_semana.filter(tipo_evento='entrevista_realizada').count(),
        'ofertas': eventos_semana.filter(tipo_evento='oferta').count(),
    }

    total = {
        'llamados': EventoAgenda.objects.filter(mostrar_en_feed=True, tipo_evento='llamada').count(),
        'entrevistas_agendadas': EventoAgenda.objects.filter(mostrar_en_feed=True, tipo_evento='entrevista_agendada').count(),
        'entrevistas_realizadas': EventoAgenda.objects.filter(mostrar_en_feed=True, tipo_evento='entrevista_realizada').count(),
        'ofertas': EventoAgenda.objects.filter(mostrar_en_feed=True, tipo_evento='oferta').count(),
    }

    return render(request, 'base/feed_comunitario.html', {
        'eventos': eventos,
        'resumen': resumen,
        'total': total
    })

from django.shortcuts import render, redirect
from .forms import ProcesoSeleccionForm

def crear_proceso(request):
    if request.method == 'POST':
        form = ProcesoSeleccionForm(request.POST)
        if form.is_valid():
            proceso = form.save(commit=False)
            proceso.usuario = request.user
            proceso.save()
            return redirect('ver_proceso', proceso.id)
    else:
        form = ProcesoSeleccionForm()
    return render(request, 'base/crear_proceso.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import ProcesoSeleccion
from .forms import HitoProcesoForm

def ver_proceso(request, proceso_id):
    proceso = get_object_or_404(ProcesoSeleccion, id=proceso_id, usuario=request.user)
    return render(request, 'base/ver_proceso.html', {'proceso': proceso})

from django.shortcuts import render
from .models import ProcesoSeleccion

from django.db.models import Case, When, Value, IntegerField
from base.models import ProcesoSeleccion

def lista_procesos(request):
    procesos = ProcesoSeleccion.objects.filter(usuario=request.user).annotate(
        prioridad=Case(
            When(estado='activo', then=Value(1)),
            When(estado='finalizado', then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
    ).order_by('prioridad', 'fecha_ingreso')

    return render(request, 'base/lista_procesos.html', {'procesos': procesos})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ProcesoSeleccion
from .forms import HitoProcesoForm

def agregar_hito(request, proceso_id):
    proceso = get_object_or_404(ProcesoSeleccion, id=proceso_id, usuario=request.user)

    if request.method == 'POST':
        form = HitoProcesoForm(request.POST)
        if form.is_valid():
            hito = form.save(commit=False)
            hito.proceso = proceso
            hito.save()
            return redirect('ver_proceso', proceso_id=proceso.id)
    else:
        form = HitoProcesoForm()

    return render(request, 'base/agregar_hito.html', {
        'form': form,
        'proceso': proceso
    })

from .forms import ProcesoSeleccionForm

def editar_proceso(request, proceso_id):
    proceso = get_object_or_404(ProcesoSeleccion, id=proceso_id, usuario=request.user)

    if request.method == 'POST':
        form = ProcesoSeleccionForm(request.POST, instance=proceso)
        if form.is_valid():
            form.save()
            return redirect('ver_proceso', proceso_id=proceso.id)
    else:
        form = ProcesoSeleccionForm(instance=proceso)

    return render(request, 'base/editar_proceso.html', {'form': form, 'proceso': proceso})

from .forms import HitoProcesoForm
from .models import HitoProceso

def editar_hito(request, hito_id):
    hito = get_object_or_404(HitoProceso, id=hito_id, proceso__usuario=request.user)

    if request.method == 'POST':
        form = HitoProcesoForm(request.POST, instance=hito)
        if form.is_valid():
            form.save()
            return redirect('ver_proceso', proceso_id=hito.proceso.id)
    else:
        form = HitoProcesoForm(instance=hito)

    return render(request, 'base/editar_hito.html', {'form': form, 'hito': hito})

from .forms import CierreProcesoForm

def cerrar_proceso(request, proceso_id):
    proceso = get_object_or_404(ProcesoSeleccion, id=proceso_id, usuario=request.user)

    if request.method == 'POST':
        form = CierreProcesoForm(request.POST, instance=proceso)
        if form.is_valid():
            proceso = form.save(commit=False)
            proceso.estado = 'finalizado'
            proceso.save()
            return redirect('ver_proceso', proceso.id)
    else:
        form = CierreProcesoForm(instance=proceso)

    return render(request, 'base/cerrar_proceso.html', {'form': form, 'proceso': proceso})

from django.shortcuts import redirect

def eliminar_proceso(request, proceso_id):
    proceso = get_object_or_404(ProcesoSeleccion, id=proceso_id, usuario=request.user)

    if request.method == 'POST':
        proceso.delete()
        return redirect('lista_procesos')

    return render(request, 'base/eliminar_proceso.html', {'proceso': proceso})

#clasificador depurador excelbase contactos linkedin

import pandas as pd
import unicodedata
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ClasificadorForm
import io

def limpiar_texto(texto, reemplazos):
    texto = ''.join(reemplazos.get(c, c) for c in str(texto))
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.lower()

def clasificar_general(fila, columnas, grupo_palabras):
    texto = ' '.join(str(fila.get(col, '')).lower() for col in columnas if col)
    for etiqueta, palabras in grupo_palabras.items():
        if any(p.strip() in texto for p in palabras if p.strip()):
            return etiqueta
    return "No clasificado"

def clasificar_responsabilidad(fila, columnas, niveles):
    texto = ' '.join(str(fila.get(col, '')).lower() for col in columnas if col)
    for nivel, palabras in niveles.items():
        if any(p.strip() in texto for p in palabras if p.strip()):
            return nivel
    return "No clasificado"

def clasificador_view(request):
    if request.method == 'POST':
        form = ClasificadorForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['archivo_excel'])
            df.columns = df.columns.str.strip().str.lower()
            columnas = [col.strip().lower() for col in form.cleaned_data['columnas_analizar'].split(',')]

            reemplazos = {'@': 'a', '#': 'n', '$': 's'}
            for col in df.columns:
                df[col] = df[col].astype(str).apply(lambda x: limpiar_texto(x, reemplazos))

            categorias = {
                "Logística": [form.cleaned_data['logistica1'], form.cleaned_data['logistica2'], form.cleaned_data['logistica3']],
                "Recursos Humanos": [form.cleaned_data['rrhh1'], form.cleaned_data['rrhh2'], form.cleaned_data['rrhh3']],
                "Ventas": [form.cleaned_data['ventas1'], form.cleaned_data['ventas2'], form.cleaned_data['ventas3'], form.cleaned_data['ventas4']],
                "Informática y Tecnología": [form.cleaned_data['tecnologia1'], form.cleaned_data['tecnologia2'], form.cleaned_data['tecnologia3']],
                "Administración y Finanzas": [form.cleaned_data['administracion1'], form.cleaned_data['administracion2'], form.cleaned_data['administracion3']],
                "Abastecimiento y Compras": [form.cleaned_data['compras1'], form.cleaned_data['compras2'], form.cleaned_data['compras3']],
                "Alta Dirección": [form.cleaned_data['direccion1'], form.cleaned_data['direccion2'], form.cleaned_data['direccion3']]
            }

            niveles = {
                "Director": [form.cleaned_data['director1'], form.cleaned_data['director2'], form.cleaned_data['director3']],
                "Gerente": [form.cleaned_data['gerente1'], form.cleaned_data['gerente2'], form.cleaned_data['gerente3']],
                "Jefe": [form.cleaned_data['jefe1'], form.cleaned_data['jefe2'], form.cleaned_data['jefe3']],
                "Supervisor": [form.cleaned_data['supervisor1'], form.cleaned_data['supervisor2'], form.cleaned_data['supervisor3']],
                "Junior": [form.cleaned_data['junior1'], form.cleaned_data['junior2'], form.cleaned_data['junior3']]
            }

            df["Clasificación"] = df.apply(lambda fila: clasificar_general(fila, columnas, categorias), axis=1)
            df["Responsabilidad"] = df.apply(lambda fila: clasificar_responsabilidad(fila, columnas, niveles), axis=1)

            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            response = HttpResponse(
                output.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=clasificado.xlsx'
            return response
    else:
        form = ClasificadorForm()

    return render(request, 'base/formulario.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Campana, Envio
from django.db.models import Count, Q
from django.utils.timezone import now

def panel_campana(request, campana_id):
    campana = get_object_or_404(Campana, id=campana_id)

    envios = campana.envios.all()
    total_envios = envios.count()
    enviados_ok = envios.filter(mensaje_enviado=True).count()
    errores = envios.filter(error_envio=True).count()
    contactos_unicos = envios.values('contacto').distinct().count()

    fecha_primera = envios.filter(fecha_envio__isnull=False).order_by('fecha_envio').first()
    fecha_primera_envio = fecha_primera.fecha_envio if fecha_primera else None

    porcentaje_exito = (enviados_ok * 100 / total_envios) if total_envios > 0 else 0

    context = {
        'campana': campana,
        'total_envios': total_envios,
        'enviados_ok': enviados_ok,
        'errores': errores,
        'porcentaje_exito': round(porcentaje_exito, 1),
        'contactos_unicos': contactos_unicos,
        'fecha_primera_envio': fecha_primera_envio,
    }

    return render(request, 'base/panel_campana.html', context)


from django.shortcuts import render, redirect
from .forms import PublicacionFeedForm
from .models import PublicacionFeed
from django.contrib.auth.decorators import login_required

@login_required
def publicar_en_feed(request):
    if request.method == 'POST':
        form = PublicacionFeedForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.save()
            return redirect('feed_comunitario')
    else:
        form = PublicacionFeedForm()
    return render(request, 'base/publicar.html', {'form': form})


@login_required
def dar_reaccion(request, publicacion_id, tipo):
    publicacion = PublicacionFeed.objects.get(id=publicacion_id)
    reaccion_map = {
        'me_gusta': publicacion.me_gusta,
        'animo': publicacion.animo,
        'fuerza': publicacion.fuerza,
        'tu_puedes': publicacion.tu_puedes,
        'felicidades': publicacion.felicidades,
    }
    if tipo in reaccion_map:
        reaccion = reaccion_map[tipo]
        if request.user in reaccion.all():
            reaccion.remove(request.user)
        else:
            reaccion.add(request.user)
    return redirect('feed_comunitario')


from .models import PublicacionFeed
from base.models import EventoAgenda  # ajusta si lo tienes en otro lugar


@login_required
def feed_comunitario(request):
    publicaciones = PublicacionFeed.objects.order_by('-creado_en')[:30]
    eventos = EventoAgenda.objects.order_by('-fecha_evento')[:30]
    resumen = {}  # opcional: reemplaza con lógica real
    total = {}

    return render(request, 'base/feed_comunitario.html', {
        'publicaciones': publicaciones,
        'eventos': eventos,
        'resumen': resumen,
        'total': total,
    })

from .forms import RegistroUsuarioForm  # nuevo import

def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('feed_comunitario')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('feed_comunitario')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'base/registro.html', {'form': form})


from django.utils import timezone
from datetime import timedelta
from .models import Fase
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.utils import timezone
from datetime import timedelta

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def panel_metas_usuario(request):
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)

    fases_con_meta = []

    for fase in Fase.objects.filter(iniciativa__usuario=request.user):
        fecha_obj = fase.fecha_objetivo or fase.fecha_objetivo_dinamica
        if fecha_obj and inicio_semana <= fecha_obj <= fin_semana:
            fases_con_meta.append(fase)

    iniciativas_data = []

    # 🔥 Agrupamos por iniciativa
    for iniciativa in set(f.iniciativa for f in fases_con_meta):

        fases_lista = []

        for fase in [f for f in fases_con_meta if f.iniciativa == iniciativa]:

            # 🔥 TAREAS ACTIVAS ESTA SEMANA
            tareas_semana = fase.tareas.filter(
                fecha_inicio__gte=inicio_semana,
                fecha_inicio__lte=fin_semana
            ).order_by("fecha_inicio")

            # 🔥 Convertimos la fase en diccionario
            fases_lista.append({
                "id": fase.id,
                "nombre": fase.nombre,
                "completado": fase.completado,
                "reflexion": fase.reflexion,
                "tareas": tareas_semana,   # ← AHORA SÍ FUNCIONA
            })

        total = len(fases_lista)
        completadas = sum(1 for f in fases_lista if f["completado"])
        porcentaje = int((completadas / total) * 100) if total > 0 else 0

        iniciativas_data.append({
            "iniciativa": iniciativa,
            "fases": fases_lista,
            "total": total,
            "completadas": completadas,
            "porcentaje": porcentaje
        })

    return render(request, 'base/panel_metas.html', {
        'iniciativas_data': iniciativas_data,
        'inicio': inicio_semana,
        'fin': fin_semana
    })


from django.shortcuts import get_object_or_404, redirect


@login_required
def completar_fase(request, fase_id):
    fase = get_object_or_404(Fase, id=fase_id, iniciativa__usuario=request.user)

    if request.method == 'POST':
        fase.completado = True
        fase.reflexion = request.POST.get("reflexion", "")
        publicar = request.POST.get("publicar_en_feed") == "on"

        if publicar and not fase.publicado_en_feed:
            PublicacionFeed.objects.create(
                usuario=request.user,
                contenido=f"✅ He completado la fase “{fase.nombre}” de la iniciativa “{fase.iniciativa.nombre}”. ¡Sigo avanzando!",
            )
            fase.publicado_en_feed = True

        fase.save()
    return redirect('panel_metas_usuario')


from django.http import JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from datetime import timedelta

@login_required
def tareas_json(request):
    tareas = Tarea.objects.filter(fase__iniciativa__usuario=request.user)
    data = []

    colores_por_estado = {
        'pendiente': '#f39c12',     # naranja
        'en_progreso': '#3498db',   # azul
        'completada': '#2ecc71'     # verde
    }

    for tarea in tareas:
        fecha_final = tarea.fecha_inicio + timedelta(days=tarea.duracion_dias)

        color = colores_por_estado.get(tarea.estado, '#95a5a6')  # gris por defecto

        data.append({
            'title': tarea.nombre,
            'start': tarea.fecha_inicio.isoformat(),
            'end': fecha_final.isoformat(),
            'url': reverse('editar_tarea', args=[tarea.id]),  # 📝 enlace al editor
            'backgroundColor': color,
            'extendedProps': {
                'iniciativa': tarea.fase.iniciativa.nombre,
                'estado': tarea.estado
            }
        })

    return JsonResponse(data, safe=False)

# RPA para detectar "Open To Work"

import openpyxl
from django.shortcuts import render
from django.contrib import messages
from base.models import ContactoLinkedIn

def panel_open_to_work(request):
    if request.method == "POST":
        accion = request.POST.get("accion")

        # 📥 Importar Excel
        if accion == "importar" and request.FILES.get("archivo_excel"):
            archivo = request.FILES["archivo_excel"]
            try:
                wb = openpyxl.load_workbook(archivo)
                hoja = wb.active
                contador = 0
                for fila in hoja.iter_rows(min_row=2, values_only=True):
                    nombre, perfil = fila[:2]
                    if nombre and perfil:
                        ContactoLinkedIn.objects.create(
                            nombre=nombre,
                            perfil_linkedin=perfil,
                            open_to_work=False
                        )
                        contador += 1
                messages.success(request, f"✅ {contador} contactos importados correctamente.")
            except Exception as e:
                messages.error(request, f"❌ Error al importar: {e}")

        # 🧠 Activar RPA internamente
        elif accion == "ejecutar_rpa":
            try:
                from .views import detectar_open_to_work_desde_django
                detectados, total = detectar_open_to_work_desde_django()
                messages.success(request, f"🎯 RPA ejecutado: {detectados} de {total} contactos detectados como 'Open to Work'.")
            except Exception as e:
                messages.error(request, f"❌ Error al ejecutar RPA: {e}")

    contactos = ContactoLinkedIn.objects.all()
    return render(request, 'base/panel_open_to_work.html', {'contactos': contactos})

import cv2
import numpy as np
import time
import os
import dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from base.models import ContactoLinkedIn

def detectar_open_to_work_desde_django():
    # 🔐 Carga credenciales si fueran necesarias después
    dotenv.load_dotenv()

    # 📁 Asegura carpeta de capturas
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # 🧠 Abre navegador visible y realiza login manual
    print("🔓 Abriendo navegador para login manual...")
    login_options = Options()
    login_options.add_argument("--window-size=1200,800")
    driver_visible = webdriver.Chrome(options=login_options)
    driver_visible.get("https://www.linkedin.com/login")
    input("🖐️ Inicia sesión en LinkedIn manualmente y presiona Enter aquí cuando termines...")

    # 🔄 Guardar cookies luego del login
    cookies = driver_visible.get_cookies()
    driver_visible.quit()
    print("✅ Login manual completado. Continuando en modo oculto...")

    # 🕶️ Abre navegador oculto y reutiliza cookies
    headless_options = Options()
    headless_options.add_argument("--headless=new")
    headless_options.add_argument("--window-size=1200,800")
    headless_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36")
    driver = webdriver.Chrome(options=headless_options)

    driver.get("https://www.linkedin.com")  # Prepara contexto para agregar cookies
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(2)
    driver.get("https://www.linkedin.com/feed")
    time.sleep(3)

    if "feed" not in driver.current_url:
        print("❌ No se restauró la sesión correctamente.")
        driver.quit()
        return 0, 0

    print("🧠 Sesión restaurada. Iniciando escaneo visual...")

    # 🎯 Función de análisis visual
    def detectar(img_path):
        imagen = cv2.imread(img_path)
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        verde_bajo = np.array([45, 100, 100])
        verde_alto = np.array([75, 255, 255])
        mascara = cv2.inRange(hsv, verde_bajo, verde_alto)
        porcentaje = (np.count_nonzero(mascara) / mascara.size) * 100
        return porcentaje > 1.0

    contactos = ContactoLinkedIn.objects.filter(open_to_work=False)
    detectados = 0

    for c in contactos:
        try:
            print(f"🔍 Analizando: {c.nombre}")
            driver.get(c.perfil_linkedin)
            time.sleep(5)

            screenshot_path = f"temp/{c.nombre}_perfil.png"
            driver.save_screenshot(screenshot_path)

            if detectar(screenshot_path):
                c.open_to_work = True
                c.save()
                detectados += 1
                print(f"✅ {c.nombre} marcado como Open to Work")
            else:
                print(f"🔘 {c.nombre} sin franja detectada")

        except Exception as e:
            print(f"❌ Error con {c.nombre}: {e}")

    driver.quit()
    print(f"🎯 Finalizado: {detectados} marcados / {contactos.count()} analizados")
    print("📸 Capturas guardadas en carpeta temp/")
    return detectados, contactos.count()

from django.shortcuts import get_object_or_404, redirect
from .models import Tarea

def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    fase_id = tarea.fase.id
    iniciativa_id = tarea.fase.iniciativa.id
    tarea.delete()
    return redirect('vista_plan', iniciativa_id=iniciativa_id)


from .models import Fase

def eliminar_fase(request, fase_id):
    fase = get_object_or_404(Fase, id=fase_id)
    iniciativa_id = fase.iniciativa.id
    fase.delete()  # Si tus relaciones están en cascada, las tareas se eliminan automáticamente
    return redirect('vista_plan', iniciativa_id=iniciativa_id)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Fase, Tarea
from django.db.models import F

def replicar_fase(request, fase_id):
    fase_original = get_object_or_404(Fase, id=fase_id)
    iniciativa = fase_original.iniciativa

    # Calcular nuevo orden (después del original)
    nuevo_orden = fase_original.orden + 1

    # Ajustar orden de fases posteriores
    Fase.objects.filter(iniciativa=iniciativa, orden__gt=fase_original.orden).update(orden=F('orden') + 1)

    # Crear nueva fase con datos replicados
    fase_copia = Fase.objects.create(
        iniciativa=iniciativa,
        nombre=f"{fase_original.nombre} (copia)",
        orden=nuevo_orden,
        icono=fase_original.icono,
        color_hex=fase_original.color_hex,
        fecha_objetivo=fase_original.fecha_objetivo,
        reflexion=fase_original.reflexion,
        publicado_en_feed=False,  # No replicar como publicado
        completado=False  # Siempre inicia como incompleta
    )

    # Replicar tareas asociadas
    for tarea in fase_original.tareas.all():
        Tarea.objects.create(
            fase=fase_copia,
            nombre=tarea.nombre,
            fecha_inicio=timezone.now().date(),  # Ajustar a hoy
            duracion_dias=tarea.duracion_dias,
            estado='pendiente',
            notas=tarea.notas
        )

    messages.success(request, f"Fase '{fase_original.nombre}' replicada exitosamente.")
    return redirect('vista_plan', iniciativa.id)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Tarea

@csrf_exempt
def reordenar_tareas(request, fase_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        orden = data.get('orden', [])
        for i, tarea_id in enumerate(orden):
            Tarea.objects.filter(id=tarea_id, fase_id=fase_id).update(orden=i)
        return JsonResponse({'status': 'ok'})


#/////////////////////// RPA //////////////////

from django.utils import timezone
from .models import Contacto

def completar_industria_y_cargo():
    contactos_actualizados = []

    contactos = Contacto.objects.all()
    for contacto in contactos:
        actualizado = False

        if not contacto.industria:
            contacto.industria = "Logística"
            actualizado = True

        if not contacto.cargo:
            contacto.cargo = "Gerente general"
            actualizado = True

        if actualizado:
            contacto.save()
            contactos_actualizados.append(contacto)

    print(f"✅ Se actualizaron {len(contactos_actualizados)} contactos.")
    return contactos_actualizados

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def ejecutar_completado(request):
    if request.method == "POST":
        completar_industria_y_cargo()  # ← llamada directa, sin importar
        return HttpResponse("Contactos actualizados")
    return HttpResponse("Método no permitido", status=405)


from django.shortcuts import get_object_or_404, redirect

@csrf_exempt
def registrar_respuesta(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)
    contacto.etapa_ventas = 'respondido'
    contacto.save()
    return redirect('base/vista_contactos')  # o donde estés mostrando la tabla

def actualizar_estatus(request, id):
    print("Vista ejecutada")  # ← Esto debe aparecer en consola

    contacto = get_object_or_404(Contacto, id=id)

    if request.method == 'POST':
        nueva_etapa = request.POST.get('etapa_ventas')
        print("Valor recibido:", nueva_etapa)

        if nueva_etapa in dict(Contacto.ETAPAS_VENTAS):
            contacto.etapa_ventas = nueva_etapa
            contacto.save()
            print("✅ Estatus actualizado a:", nueva_etapa)

    return redirect('base/vista_contactos')  # ← Ajusta según el nombre de tu vista principal


from django.shortcuts import render
from .models import Contacto, Reunion, Licitacion, Cierre, PostVenta

def flujo_ventas(request):
    context = {
        'contactos': Contacto.objects.all(),
        'reuniones': Reunion.objects.select_related('contacto'),
        'licitaciones': Licitacion.objects.select_related('contacto'),
        'cierres': Cierre.objects.select_related('contacto'),
        'postventas': PostVenta.objects.select_related('contacto'),
    }
    return render(request, 'base/flujoventa.html', context)


@require_POST
@csrf_exempt  # Solo si no usas {{ csrf_token }}
def actualizar_etapa(request, contacto_id, etapa):
    contacto = get_object_or_404(Contacto, id=contacto_id)

    etapas_validas = dict(Contacto.ETAPAS_VENTAS).keys()
    if etapa not in etapas_validas:
        return JsonResponse({'error': 'Etapa no válida'}, status=400)

    contacto.etapa_ventas = etapa
    contacto.save()

    return JsonResponse({'status': 'ok'})


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
import json

from .models import Contacto, Reunion

@require_POST
@csrf_exempt
def crear_reunion(request):
    print("✅ Solicitud POST recibida")

    try:
        # Cargar datos del cuerpo de la solicitud
        data = json.loads(request.body)
        print("📦 Datos recibidos:", data)

        # Validar existencia del contacto
        contacto = get_object_or_404(Contacto, id=data['contacto_id'])
        print("👤 Contacto encontrado:", contacto)

        # Procesar fecha
        fecha_raw = datetime.fromisoformat(data['fecha'].replace("Z", "+00:00"))  # Asegura compatibilidad con formato ISO
        tz_chile = pytz.timezone('America/Santiago')

        if fecha_raw.tzinfo is None:
            fecha_final = make_aware(fecha_raw, timezone=tz_chile)
        else:
            fecha_final = fecha_raw.astimezone(tz_chile)

        print("🕒 Fecha ajustada a hora Chile:", fecha_final)

        # Crear objeto Reunion
        reunion = Reunion.objects.create(
            contacto=contacto,
            fecha=fecha_final,
            modalidad=data['modalidad'],
            resultado=data['resultado']
        )
        print("✅ Reunión creada con ID:", reunion.id)

        return JsonResponse({'status': 'ok', 'reunion_id': reunion.id})

    except Exception as e:
        print("❌ Error al crear reunión:", e)
        return JsonResponse({'error': str(e)}, status=500)



from django.utils.timezone import localtime, is_aware, make_aware
import pytz

def contactos_con_reuniones(request):
    reuniones = Reunion.objects.select_related('contacto').all()
    datos = []

    for r in reuniones:
        fecha = r.fecha

        # Asegurar que la fecha sea aware
        if not is_aware(fecha):
            fecha = make_aware(fecha)

        # Convertir a hora local de Chile
        fecha_local = localtime(fecha).astimezone(pytz.timezone('America/Santiago'))

        datos.append({
            'id': r.contacto.id,
            'nombre': r.contacto.nombre,
            'fecha': fecha_local.strftime('%d/%m/%Y %H:%M'),
            'modalidad': r.modalidad,
            'resultado': r.resultado
        })

    return JsonResponse({'contactos': datos})


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Reunion

@csrf_exempt  # Solo si no estás usando CSRF token en el frontend
@require_POST
def eliminar_reunion(request):
    try:
        reunion_id = int(request.POST.get('id'))
        reunion = Reunion.objects.get(id=reunion_id)
        reunion.delete()  # 🔥 Aquí se elimina el registro en el modelo Reunión
        return JsonResponse({'status': 'ok', 'mensaje': 'Reunión eliminada correctamente'})
    except Reunion.DoesNotExist:
        return JsonResponse({'status': 'error', 'mensaje': 'Reunión no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)


from django.shortcuts import render
from .models import Tarea, Hito, Iniciativa
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Tarea, Hito, Iniciativa
from django.contrib.auth.decorators import login_required

@login_required
def panel_avance(request):
    usuario = request.user

    tareas_completadas = Tarea.objects.filter(estado='completada', fase__iniciativa__usuario=usuario).count()
    hitos_recientes = Hito.objects.filter(tarea__fase__iniciativa__usuario=usuario).order_by('-creado_en')[:5]
    iniciativas = Iniciativa.objects.filter(usuario=usuario)

    # 🔢 Calcular avance y color por iniciativa
    for iniciativa in iniciativas:
        fases = iniciativa.fases.all()
        tareas_total = sum(fase.tareas.count() for fase in fases)
        tareas_completadas = sum(fase.tareas.filter(estado='completada').count() for fase in fases)

        avance = round((tareas_completadas / tareas_total) * 100, 1) if tareas_total > 0 else 0
        iniciativa.avance = avance

        if avance < 30:
            iniciativa.color_barra = "bg-danger"
        elif avance < 70:
            iniciativa.color_barra = "bg-warning"
        else:
            iniciativa.color_barra = "bg-success"

    # 💪 Músculos únicos
    musculos_unicos = set()
    for hito in hitos_recientes:
        if hasattr(hito, 'musculo') and hito.musculo:
            musculos_unicos.add(hito.musculo)

    # 📊 Tareas por día
    dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    tareas_por_dia = [Tarea.objects.filter(
        estado='completada',
        fase__iniciativa__usuario=usuario,
        fecha_completada__week_day=i+2
    ).count() for i in range(7)]

    context = {
        'tareas_completadas': tareas_completadas,
        'hitos_recientes': hitos_recientes,
        'iniciativas': iniciativas,
        'musculos_unicos': list(musculos_unicos),
        'dias_semana': dias_semana,
        'tareas_por_dia': tareas_por_dia,
        'feed': [],
    }

    return render(request, 'base/panel_avance.html', context)


@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(PublicacionFeed, pk=pk)

    if publicacion.usuario != request.user:
        return HttpResponseForbidden("No puedes editar esta publicación.")

    if request.method == "POST":
        publicacion.contenido = request.POST.get("contenido")
        publicacion.save()
        return redirect('feed_comunitario')

    return render(request, "editar_publicacion.html", {"publicacion": publicacion})

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(PublicacionFeed, pk=pk)

    if publicacion.usuario != request.user:
        return HttpResponseForbidden("No puedes eliminar esta publicación.")

    publicacion.delete()
    return redirect('feed_comunitario')


from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from .models import Iniciativa


def mapa_maternal(request):
    hoy = timezone.now().date()

    # Estructura base del mapa
    categorias = {
        'hogar': {
            'nombre': 'Hogar y Logística',
            'icono': '🏡',
            'color': '#85c1e9',
            'iniciativas': [],
            'tareas_totales': 0,
            'tareas_completadas': 0,
            'tareas_retrasadas': 0,
        },
        'crianza': {
            'nombre': 'Crianza y Desarrollo',
            'icono': '👶',
            'color': '#f5b7b1',
            'iniciativas': [],
            'tareas_totales': 0,
            'tareas_completadas': 0,
            'tareas_retrasadas': 0,
        },
        'trabajo': {
            'nombre': 'Trabajo y Proyectos',
            'icono': '💼',
            'color': '#a3e4d7',
            'iniciativas': [],
            'tareas_totales': 0,
            'tareas_completadas': 0,
            'tareas_retrasadas': 0,
        },
        'vinculos': {
            'nombre': 'Vínculos y Relaciones',
            'icono': '❤️',
            'color': '#f9e79f',
            'iniciativas': [],
            'tareas_totales': 0,
            'tareas_completadas': 0,
            'tareas_retrasadas': 0,
        },
        'salud': {
            'nombre': 'Salud Mental y Emocional',
            'icono': '🧘',
            'color': '#d7bde2',
            'iniciativas': [],
            'tareas_totales': 0,
            'tareas_completadas': 0,
            'tareas_retrasadas': 0,
        },
    }

    # Obtener iniciativas del usuario
    iniciativas = Iniciativa.objects.filter(usuario=request.user)

    # Procesar iniciativas
    for ini in iniciativas:
        cat = ini.categoria_maternal
        if cat not in categorias:
            continue

        fases = ini.fases.all().order_by('orden')

        ini_data = {
            'nombre': ini.nombre,
            'fases': [],
        }

        for fase in fases:

            # Procesar tareas y marcar retrasadas
            tareas = []
            for t in fase.tareas.all():
                t.retrasada = (
                    t.estado != 'completada'
                    and t.fecha_inicio
                    and (t.fecha_inicio + timedelta(days=t.duracion_dias)) < hoy
                )
                tareas.append(t)

            fase_data = {
                'nombre': fase.nombre,
                'tareas': tareas,
                'tareas_totales': len(tareas),
                'tareas_completadas': sum(1 for t in tareas if t.estado == 'completada'),
                'tareas_retrasadas': sum(1 for t in tareas if t.retrasada),
            }

            ini_data['fases'].append(fase_data)

            # Acumular KPIs por categoría
            categorias[cat]['tareas_totales'] += fase_data['tareas_totales']
            categorias[cat]['tareas_completadas'] += fase_data['tareas_completadas']
            categorias[cat]['tareas_retrasadas'] += fase_data['tareas_retrasadas']

        categorias[cat]['iniciativas'].append(ini_data)

    # Calcular % de carga mental por categoría
    for cat, data in categorias.items():
        if data['tareas_totales'] > 0:
            data['porcentaje'] = int((data['tareas_completadas'] / data['tareas_totales']) * 100)
        else:
            data['porcentaje'] = 0

    return render(request, 'mapa_maternal.html', {
        'categorias': categorias,
        'hoy': hoy,
    })
