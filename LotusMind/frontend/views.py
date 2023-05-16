from django.shortcuts import get_object_or_404, redirect, render
from Lotus.models import Modulo, Recurso, ModuloRecurso, Pregunta, RespuestaEncuesta, RespuestaPreguntaEncuesta, Usuario
# Create your views here.
from django.db.models import Sum
from django.contrib.auth import authenticate, login


def paginausuario(request):
    return render(request, 'frontend/Perfil_Usuario_Lotusmind.html')


def menu(request):
    return render(request, 'frontend/menu.html')


def index(request):
    return render(request, 'frontend/index.html')


def conocer(request):
    return render(request, 'frontend/conocerte.html')


def login(request):
    return render(request, 'frontend/login.html')


def escala(request):
    return render(request, 'frontend/Escala.html')


def register(request):
    return render(request, 'frontend/register.html')


def auth(request):
    return render(request, 'frontend/authentification.html')


def modulo(request, nombre_mod):
    modulo = Modulo.objects.get(nombre_mod=nombre_mod)
    recursos = Recurso.objects.filter(modulos=modulo).order_by(
        'modulorecurso__orden')
    primer_recurso = recursos.first()
    recurso_anterior = None
    if len(recursos) > 1:
        recurso_siguiente = recursos[1]
    else:
        recurso_siguiente = None
    context = {
        'modulo': modulo,
        'recursos': recursos,
        'recurso': primer_recurso,
        'recurso_anterior': recurso_anterior,
        'recurso_siguiente': recurso_siguiente
    }
    return render(request, 'frontend/plantillamodulo.html', context)


def recurso(request, nombre_mod, nombre_rec):

    modulo = Modulo.objects.get(nombre_mod=nombre_mod)
    recurso = Recurso.objects.filter(
        modulos=modulo, nombre_rec=nombre_rec).first()
    modulo_recurso = ModuloRecurso.objects.get(modulo=modulo, recurso=recurso)
    orden = modulo_recurso.orden

    # Obtener el recurso anterior y el siguiente
    recursos = Recurso.objects.filter(
        modulos=modulo).order_by('modulorecurso__orden')
    if orden == 0:
        recurso_anterior = None
    else:
        recurso_anterior = recursos[orden-1]
    if orden < len(recursos) - 1:
        recurso_siguiente = recursos[orden+1]
    else:
        recurso_siguiente = None

    context = {
        'nombre_mod': nombre_mod,
        'recurso': recurso,
        'recurso_anterior': recurso_anterior,
        'recurso_siguiente': recurso_siguiente
    }
    return render(request, 'frontend/plantillarecurso.html', context)


def register(request):
    return render(request, 'frontend/register.html')


def encuesta(request, pregunta_id=None):
    preguntas = Pregunta.objects.all()
    if not request.user.is_authenticated:
        user = Usuario.objects.get(username='Andreach')
        login(request, user)

    # Obtener la última respuesta del usuario, si existe
    try:
        respuesta_encuesta = RespuestaEncuesta.objects.filter(
            usuario=request.user).latest('fecha')
    except RespuestaEncuesta.DoesNotExist:
        respuesta_encuesta = None

    # Si la respuesta del usuario es None o todas las preguntas ya han sido respondidas
    if respuesta_encuesta is None or respuesta_encuesta.preguntas.count() == preguntas.count():
        # Crear una nueva respuesta de la encuesta
        respuesta_encuesta = RespuestaEncuesta.objects.create(
            usuario=request.user)

    # Eliminar las respuestas existentes del usuario
        RespuestaPreguntaEncuesta.objects.filter(
            respuesta_encuesta=respuesta_encuesta).delete()

        # Obtener la siguiente pregunta que aún no ha sido respondida en la encuesta actual
    if pregunta_id is not None:
        pregunta_actual = get_object_or_404(preguntas, id=pregunta_id)
    else:
        # Obtener la primera pregunta que aún no ha sido respondida
        pregunta_actual = preguntas.exclude(
            respuestapreguntaencuesta__respuesta_encuesta=respuesta_encuesta
        ).first()

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta:
            respuesta = int(respuesta)  # Convertir la respuesta a entero
            # Actualizar la respuesta de la pregunta actual o crear una nueva respuesta
            respuesta_pregunta_encuesta, created = RespuestaPreguntaEncuesta.objects.get_or_create(
                respuesta_encuesta=respuesta_encuesta,
                pregunta=pregunta_actual,
                defaults={'respuesta': respuesta}
            )
            if not created:
                respuesta_pregunta_encuesta.respuesta = respuesta
                respuesta_pregunta_encuesta.save()

        # Obtener la siguiente pregunta que aún no ha sido respondida en la encuesta actual
        pregunta_siguiente = preguntas.exclude(
            respuestapreguntaencuesta__respuesta_encuesta=respuesta_encuesta
        ).exclude(id=pregunta_actual.id).first()

        # Si no hay más preguntas por responder en la encuesta actual, marcar la encuesta como completada
        if pregunta_siguiente is None:
            respuesta_encuesta.completada = True
            respuesta_encuesta.save()
            return redirect('resultado_encuesta')

        # Redirigir a la siguiente pregunta de la encuesta actual
        return redirect('encuesta', pregunta_id=pregunta_siguiente.id)

    context = {
        'pregunta': pregunta_actual
    }
    return render(request, 'frontend/frecuencia.html', context)


def resultado_encuesta(request):
    respuestas_encuesta = RespuestaEncuesta.objects.filter(
        usuario=request.user)
    total_respuestas = RespuestaPreguntaEncuesta.objects.filter(
        respuesta_encuesta__in=respuestas_encuesta).aggregate(total=Sum('respuesta'))

    context = {
        'respuestas_encuesta': respuestas_encuesta,
        'total_respuestas': total_respuestas['total']
    }
    return render(request, 'frontend/resultado_encuesta.html', context)
