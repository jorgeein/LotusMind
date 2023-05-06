from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    uso_personal = models.BooleanField(default=True)
    uso_terceros = models.BooleanField(default=False)
    escala_usuario = models.PositiveIntegerField(blank=True, null=True)


class Modulo(models.Model):
    nombre_mod = models.CharField(max_length=100)
    desc_mod = models.CharField(max_length=2000)
    cant_recursos = models.PositiveIntegerField(blank=True, null=True)
    cant_temas = models.PositiveIntegerField(blank=True, null=True)
    esta_terminado = models.BooleanField(default=False)
