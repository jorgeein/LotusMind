from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    uso_personal = models.BooleanField(default=True)
    uso_terceros = models.BooleanField(default = False)
    escala_usuario = models.PositiveIntegerField(blank = True, null = True)