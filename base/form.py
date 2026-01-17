from django import forms
from .models import (
    MaquinaEquipo, Rol, Persona, Ubicacion,
    AtributoRevisar, TipoInventario, Recurso,
    PlanInventario
)

class MaquinaEquipoForm(forms.ModelForm):
    class Meta:
        model = MaquinaEquipo
        fields = '__all__'

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = '__all__'

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class AtributoRevisarForm(forms.ModelForm):
    class Meta:
        model = AtributoRevisar
        fields = '__all__'

class TipoInventarioForm(forms.ModelForm):
    class Meta:
        model = TipoInventario
        fields = '__all__'

from django import forms
from .models import Recurso

class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = ['tipo', 'nombre', 'costo']


class PlanInventarioForm(forms.ModelForm):
    fecha_inicio = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=['%d/%m/%Y'])
    fecha_fin = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=['%d/%m/%Y'])

    class Meta:
        model = PlanInventario
        fields = '__all__'