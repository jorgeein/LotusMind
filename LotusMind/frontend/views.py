from django.shortcuts import redirect, render
from Lotus.models import Modulo, Recurso, ModuloRecurso, Pregunta, RespuestaEncuesta, RespuestaPreguntaEncuesta
# Create your views here.


def paginausuario(request):
    return render(request, 'frontend/Perfil_Usuario_Lotusmind.html')


def menu(request):
    return render(request, 'frontend/menu.html')


def index(request):
    return render(request, 'frontend/index.html')


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


def encuesta(request):
    preguntas = Pregunta.objects.all()
    respuestas_usuario = RespuestaPreguntaEncuesta.objects.filter(
        respuesta_encuesta__usuario=request.user
    )
    respuestas_usuario_ids = respuestas_usuario.values_list(
        'pregunta__id', flat=True
    )
    preguntas_restantes = preguntas.exclude(id__in=respuestas_usuario_ids)
    siguiente_pregunta = preguntas_restantes.first()

    if request.method == 'POST':
        pregunta_id = request.POST.get('pregunta_id')
        respuesta = request.POST.get('respuesta')

        if pregunta_id and respuesta:
            pregunta = Pregunta.objects.get(id=pregunta_id)
            respuesta_encuesta = RespuestaEncuesta.objects.get_or_create(
                usuario=request.user
            )[0]

            RespuestaPreguntaEncuesta.objects.create(
                respuesta_encuesta=respuesta_encuesta,
                pregunta=pregunta,
                respuesta=respuesta
            )

        # Redireccionar a la siguiente pregunta o mostrar resultados
        if preguntas_restantes.exists():
            siguiente_pregunta = preguntas_restantes.first()
            return redirect('encuesta', pregunta_id=siguiente_pregunta.id)
        else:
            return redirect('resultado_encuesta')

    if preguntas_restantes.exists():
        siguiente_pregunta = preguntas_restantes.first()
        context = {
            'pregunta': siguiente_pregunta
        }
    else:
        context = {}

    return render(request, 'frontend/frecuencia.html', context)
