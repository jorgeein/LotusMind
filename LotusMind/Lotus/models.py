from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .validators import validate_svg
import os
from django.conf import settings


def image_upload_path(instance, filename):
    return os.path.join(settings.BASE_DIR, 'frontend', 'static', 'frontend', 'figuras', filename)


class Usuario(AbstractUser, PermissionsMixin):
    uso_personal = models.BooleanField(default=True)
    uso_terceros = models.BooleanField(default=False)
    escala_usuario = models.PositiveIntegerField(blank=True, null=True)
    historial_recursos = models.ManyToManyField('Recurso', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def tiene_modulo(self, recurso):
        return self.historial_recursos.filter(pk=recurso.pk).exists()


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
    MEDITACION = 'Meditación'
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
    imagen = models.FileField(upload_to='frontend/static/frontend/figuras',
                              validators=[validate_svg], null=True, blank=True)
    tiempo_recurso = models.IntegerField(default=3)
    color_hexadecimal = models.CharField(
        max_length=7, help_text='Color en formato hexadecimal (#RRGGBB)', default=" #FF0000")

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


class Pregunta(models.Model):
    texto = models.CharField(max_length=255)
    respuesta = models.IntegerField()  # Campo de respuesta como IntegerField

    def __str__(self):
        return self.texto


class RespuestaEncuesta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    preguntas = models.ManyToManyField(
        Pregunta, through='RespuestaPreguntaEncuesta')
    fecha = models.DateTimeField(auto_now_add=True)
    total_respuestas = models.IntegerField(default=0)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario.username} - Encuesta {self.id}'


class RespuestaPreguntaEncuesta(models.Model):
    respuesta_encuesta = models.ForeignKey(
        RespuestaEncuesta, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.IntegerField()  # Campo de respuesta como IntegerField

    def __str__(self):
        return f'{self.pregunta.texto} - {self.respuesta_encuesta}'
