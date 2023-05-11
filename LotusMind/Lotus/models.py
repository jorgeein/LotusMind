from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .validators import validate_svg


class Usuario(AbstractUser, PermissionsMixin):
    uso_personal = models.BooleanField(default=True)
    uso_terceros = models.BooleanField(default=False)
    escala_usuario = models.PositiveIntegerField(blank=True, null=True)
    historial_modulos = models.ManyToManyField('Modulo', blank=True)

    def tiene_modulo(self, modulo):
        return self.historial_modulos.filter(pk=modulo.pk).exists()


class Modulo(models.Model):
    nombre_mod = models.CharField(max_length=100)
    desc_mod = models.CharField(max_length=2000)
    cant_recursos = models.PositiveIntegerField(blank=True, null=True)
    cant_temas = models.PositiveIntegerField(blank=True, null=True)
    esta_terminado = models.BooleanField(default=False)


class Recurso(models.Model):
    nombre_rec = models.CharField(max_length=100)
    VIDEO = 'Video'
    MUSICA = 'Musica'
    LIBRO = 'Libro'
    ORIENTACIONEDUCATIVA = 'Orientacion Educativa'
    CURSO = 'Curso'
    MEDITACION = 'MEDITACION'
    TIPO_CHOICES = [
        (VIDEO, 'Video'),
        (MUSICA, 'Música'),
        (LIBRO, 'Libro'),
        (ORIENTACIONEDUCATIVA, 'Orientacion Educativa'),
        (CURSO, 'Curso'),
        (MEDITACION, 'Meditacion')
    ]
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default=VIDEO)
    descripcion = models.TextField()
    modulos = models.ManyToManyField(Modulo, through='ModuloRecurso')
    cant_temas = models.IntegerField(blank=True, null=True)
    imagen = models.FileField(
        upload_to='LotusMind/frontend/static/frontend/figuras', validators=[validate_svg], null=True, blank=True)
    tiempo_recurso = models.IntegerField(default=3)

    def __str__(self):
        return self.nombre_rec


class ModuloRecurso(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    orden = models.IntegerField(default=1)


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100)
    modulos = models.ManyToManyField(Modulo)
    recursos = models.ManyToManyField(Recurso)
