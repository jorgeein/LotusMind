from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms
from .models import Usuario
from .models import Modulo
from .models import Recurso
from .models import ModuloRecurso
from .models import Etiqueta, Pregunta, RespuestaEncuesta, RespuestaPreguntaEncuesta

User = get_user_model()


class BarInline(admin.TabularInline):
    model = Recurso.modulos.through


class UsuarioForm(forms.ModelForm):
    modulos = forms.ModelMultipleChoiceField(
        queryset=Modulo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = '__all__'


class ModuloAdmin(admin.ModelAdmin):
    model = Modulo
    inlines = [
        BarInline,
    ]


class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    filter_horizontal = ('historial_modulos',)
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'uso_terceros', 'uso_personal', 'escala_usuario',
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'uso_terceros', 'uso_personal', 'escala_usuario', 'historial_modulos'
            )
        })
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'uso_terceros', 'uso_personal', 'escala_usuario',
            )
        })
    )
# Register your models here.


admin.site.register(Modulo, ModuloAdmin)
admin.site.register(Recurso)
admin.site.register(ModuloRecurso)
admin.site.register(Etiqueta)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Pregunta)
admin.site.register(RespuestaEncuesta)
admin.site.register(RespuestaPreguntaEncuesta)
