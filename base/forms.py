from django import forms
from .models import Iniciativa

class IniciativaForm(forms.ModelForm):
    class Meta:
        model = Iniciativa
        fields = ['nombre', 'objetivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Mi búsqueda ejecutiva'}),
            'objetivo': forms.TextInput(attrs={'placeholder': 'Ej: Conseguir empleo logístico en 60 días'}),
        }

from django import forms
from .models import Iniciativa

class IniciativaForm(forms.ModelForm):
    class Meta:
        model = Iniciativa
        fields = ['nombre', 'objetivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'id_nombre'}),
            'objetivo': forms.TextInput(attrs={'id': 'id_objetivo'}),
        }

from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'fecha_inicio', 'duracion_dias']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        }


# forms.py

from django import forms
from .models import Hito

class HitoForm(forms.ModelForm):
    class Meta:
        model = Hito
        fields = ['descripcion', 'archivo', 'series', 'repeticiones', 'carga']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': "Describe brevemente este hito o aprendizaje…"
            }),
            'series': forms.NumberInput(attrs={'placeholder': 'Ej: 4'}),
            'repeticiones': forms.NumberInput(attrs={'placeholder': 'Ej: 12'}),
            'carga': forms.NumberInput(attrs={'placeholder': 'Ej: 25.0'}),
        }

from django import forms
from .models import Fase

ICONOS_FASE = [
    ('📌', '📌 Tarea'),
    ('🚀', '🚀 Lanzamiento'),
    ('🧱', '🧱 Bloque'),
    ('📈', '📈 Progreso'),
    ('🧩', '🧩 Modulo'),
    ('🔧', '🔧 Ajuste'),
    ('🗂️', '🗂️ Organización'),
    ('⚙️', '⚙️ Sistema'),
    ('🎯', '🎯 Objetivo'),
]

class FaseForm(forms.ModelForm):
    icono = forms.ChoiceField(choices=ICONOS_FASE, label='Icono visual')

    class Meta:
        model = Fase
        fields = ['nombre', 'orden', 'icono', 'color_hex']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la fase'}),
            'orden': forms.NumberInput(attrs={'min': 1}),
            'color_hex': forms.TextInput(attrs={'type': 'color'}),
        }

from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'fecha_inicio', 'duracion_dias', 'estado', 'notas']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la tarea'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'duracion_dias': forms.NumberInput(attrs={'min': 1}),
            'estado': forms.Select(),
            'notas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notas opcionales'}),
        }

from django import forms
from .models import EventoAgenda

class EventoAgendaForm(forms.ModelForm):
    class Meta:
        model = EventoAgenda
        fields = ['tipo_evento', 'empresa', 'fecha_evento', 'comentario', 'mostrar_en_feed']
        widgets = {
            'fecha_evento': forms.DateInput(attrs={'type': 'date'}),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }

from django import forms
from .models import ProcesoSeleccion, HitoProceso

class ProcesoSeleccionForm(forms.ModelForm):
    class Meta:
        model = ProcesoSeleccion
        fields = ['empresa', 'cargo', 'fecha_ingreso']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }

class HitoProcesoForm(forms.ModelForm):
    class Meta:
        model = HitoProceso
        fields = ['tipo', 'fecha', 'comentario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'comentario': forms.Textarea(attrs={'rows': 2}),
        }

from django import forms
from .models import ProcesoSeleccion

class CierreProcesoForm(forms.ModelForm):
    class Meta:
        model = ProcesoSeleccion
        fields = ['resultado', 'comentario_final', 'fecha_cierre']
        widgets = {
            'resultado': forms.Select(attrs={'class': 'form-control'}),
            'comentario_final': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Feedback o aprendizaje recibido...'}),
            'fecha_cierre': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'resultado': 'Resultado final del proceso',
            'comentario_final': 'Comentario o feedback recibido',
            'fecha_cierre': 'Fecha de cierre del proceso',
        }


from django import forms

class ClasificadorForm(forms.Form):
    archivo_excel = forms.FileField(label="Archivo Excel (.xlsx)")
    columnas_analizar = forms.CharField(
        label="Columnas del Excel donde buscar (separadas por coma)",
        help_text="Ej: descripcion,cargo,funciones"
    )

    # Categorías por sector funcional
    logistica1 = forms.CharField(label="Palabra 1 para Logística", required=False)
    logistica2 = forms.CharField(label="Palabra 2 para Logística", required=False)
    logistica3 = forms.CharField(label="Palabra 3 para Logística", required=False)

    rrhh1 = forms.CharField(label="Palabra 1 para RRHH", required=False)
    rrhh2 = forms.CharField(label="Palabra 2 para RRHH", required=False)
    rrhh3 = forms.CharField(label="Palabra 3 para RRHH", required=False)

    ventas1 = forms.CharField(label="Palabra 1 para Ventas", required=False)
    ventas2 = forms.CharField(label="Palabra 2 para Ventas", required=False)
    ventas3 = forms.CharField(label="Palabra 3 para Ventas", required=False)
    ventas4 = forms.CharField(label="Palabra 4 para Ventas", required=False)  # Nueva palabra clave

    tecnologia1 = forms.CharField(label="Palabra 1 para Tecnología", required=False)
    tecnologia2 = forms.CharField(label="Palabra 2 para Tecnología", required=False)
    tecnologia3 = forms.CharField(label="Palabra 3 para Tecnología", required=False)

    administracion1 = forms.CharField(label="Palabra 1 para Administración", required=False)
    administracion2 = forms.CharField(label="Palabra 2 para Administración", required=False)
    administracion3 = forms.CharField(label="Palabra 3 para Administración", required=False)

    compras1 = forms.CharField(label="Palabra 1 para Compras", required=False)
    compras2 = forms.CharField(label="Palabra 2 para Compras", required=False)
    compras3 = forms.CharField(label="Palabra 3 para Compras", required=False)

    direccion1 = forms.CharField(label="Palabra 1 para Alta Dirección", required=False)
    direccion2 = forms.CharField(label="Palabra 2 para Alta Dirección", required=False)
    direccion3 = forms.CharField(label="Palabra 3 para Alta Dirección", required=False)

    # Palabras clave por nivel jerárquico
    director1 = forms.CharField(label="Palabra 1 para Director", required=False)
    director2 = forms.CharField(label="Palabra 2 para Director", required=False)
    director3 = forms.CharField(label="Palabra 3 para Director", required=False)

    gerente1 = forms.CharField(label="Palabra 1 para Gerente", required=False)
    gerente2 = forms.CharField(label="Palabra 2 para Gerente", required=False)
    gerente3 = forms.CharField(label="Palabra 3 para Gerente", required=False)

    jefe1 = forms.CharField(label="Palabra 1 para Jefe", required=False)
    jefe2 = forms.CharField(label="Palabra 2 para Jefe", required=False)
    jefe3 = forms.CharField(label="Palabra 3 para Jefe", required=False)

    supervisor1 = forms.CharField(label="Palabra 1 para Supervisor", required=False)
    supervisor2 = forms.CharField(label="Palabra 2 para Supervisor", required=False)
    supervisor3 = forms.CharField(label="Palabra 3 para Supervisor", required=False)

    junior1 = forms.CharField(label="Palabra 1 para Junior", required=False)
    junior2 = forms.CharField(label="Palabra 2 para Junior", required=False)
    junior3 = forms.CharField(label="Palabra 3 para Junior", required=False)


from django import forms
from .models import PublicacionFeed

class PublicacionFeedForm(forms.ModelForm):
    class Meta:
        model = PublicacionFeed
        fields = ['contenido', 'imagen']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'placeholder': 'Comparte tu avance, reflexión o motivación aquí...',
                'rows': 4,
                'class': 'form-control'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        help_text="Requerido. Solo letras, números y @/./+/-/_",
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="Debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y algún símbolo (como @, #, $...)"
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        help_text="Repite la contraseña exactamente igual"
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")