from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario

class UsuarioAdmin(UserAdmin):

    list_display = (
        'username', 'email', 'first_name', 'last_name', 'uso_terceros', 'uso_personal','escala_usuario'
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
                'uso_terceros', 'uso_personal','escala_usuario'
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
                'uso_terceros', 'uso_personal','escala_usuario'
                )
        })
    )
# Register your models here.
admin.site.register(Usuario, UsuarioAdmin)
