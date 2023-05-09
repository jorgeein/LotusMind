from django.forms import ModelForm
from .models import Usuario, Modulo
from django import forms


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'historial_recurso': forms.CheckboxSelectMultiple
        }
