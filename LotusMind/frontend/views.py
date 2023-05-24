from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from Lotus.models import Modulo, Recurso, ModuloRecurso, Pregunta, RespuestaEncuesta, RespuestaPreguntaEncuesta, Usuario
# Create your views here.
from django.db.models import Sum
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import RegistrationForm


def inicio(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'frontend/inicio.html')


def google_auth(request):
    # Redirecciona directamente a la autenticación de Google
    return redirect('social:begin', backend='google-oauth2')


def paginausuario(request):
    return render(request, 'frontend/Perfil_Usuario_Lotusmind.html')


def menu(request):
    return render(request, 'frontend/menu.html')


def index(request):
    return render(request, 'frontend/index.html')


def conocer(request):
    return render(request, 'frontend/conocerte.html')


def escala(request):
    return render(request, 'frontend/Escala.html')


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
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'frontend/register.html', {'form': form})


def encuesta(request, pregunta_id=None, respuesta_encuesta_id=None):
    preguntas = Pregunta.objects.all()

    # Obtener la última respuesta del usuario, si existe

    # Si la respuesta del usuario es None o todas las preguntas ya han sido respondidas
    if respuesta_encuesta_id is None:
        # Crear una nueva respuesta de la encuesta
        respuesta_encuesta = RespuestaEncuesta.objects.create(
            usuario=request.user)

        # Eliminar las respuestas existentes del usuario
        RespuestaPreguntaEncuesta.objects.filter(
            respuesta_encuesta=respuesta_encuesta).delete()
    else:
        respuesta_encuesta = get_object_or_404(
            RespuestaEncuesta, id=respuesta_encuesta_id)
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
            print("Valor de respuesta_encuesta.id:", respuesta_encuesta.id)
            return redirect('resultado_encuestaafter', respuesta_encuesta_id=respuesta_encuesta.id)

        # Redirigir a la siguiente pregunta de la encuesta actual
        return redirect('encuesta', pregunta_id=pregunta_siguiente.id, respuesta_encuesta_id=respuesta_encuesta.id)

    context = {
        'pregunta': pregunta_actual,
        'respuesta_encuesta': respuesta_encuesta
    }
    print("Contexto de la encuesta:", context)
    return render(request, 'frontend/frecuencia.html', context)


def resultado_encuestaafter(request, respuesta_encuesta_id):
    respuestas_encuesta = get_object_or_404(
        RespuestaEncuesta, id=respuesta_encuesta_id)
    total_respuestas = RespuestaPreguntaEncuesta.objects.filter(
        respuesta_encuesta=respuestas_encuesta
    ).aggregate(total=Sum('respuesta')).get('total')
    respuestas_encuesta.total_respuestas = total_respuestas
    respuestas_encuesta.save()
    user = request.user
    ultimas_encuestas = RespuestaEncuesta.objects.filter(
        usuario=user).order_by('-fecha')[:5]
    for encuesta in ultimas_encuestas:
        encuesta.fecha = encuesta.fecha.strftime('%b %d')
    margenizq = 0
    porcentaje_circulo = 0
    porcentaje_numero = 0
    porcentaje_barra = 0
    if total_respuestas <= 44:
        porcentaje_barra = (((((total_respuestas-20)/25)*100)*30)/100)
        margenizq = 0
        porcentaje_circulo = porcentaje_barra + 0
        porcentaje_numero = porcentaje_circulo - 4

    if total_respuestas <= 59 and total_respuestas >= 45:
        porcentaje_barra = (((((total_respuestas-44)/15)*100)*30)/100)
        margenizq = 110
        porcentaje_circulo = porcentaje_barra + 30
        porcentaje_numero = porcentaje_circulo - 4

    if total_respuestas <= 74 and total_respuestas >= 60:
        porcentaje_barra = (((((total_respuestas-59)/15)*100)*30)/100)
        margenizq = 220
        porcentaje_circulo = porcentaje_barra + 70
        porcentaje_numero = porcentaje_circulo - 4

    if total_respuestas >= 75:
        porcentaje_barra = (((((total_respuestas-74)/15)*100)*30)/100)
        margenizq = 330
        porcentaje_circulo = porcentaje_barra + 100
        porcentaje_numero = porcentaje_circulo - 4
    context = {
        'respuestas_encuesta': respuestas_encuesta,
        'ultimas_encuestas': ultimas_encuestas,
        'total_respuestas': total_respuestas,
        'margen_izq': margenizq,
        'porcentaje_barra': porcentaje_barra,
        'porcentaje_circulo': porcentaje_circulo,
        'porcentaje_numero': porcentaje_numero

    }
    return render(request, 'frontend/resultado_encuesta.html', context)


def resultado_encuesta(request):
    user = request.user
    respuestas_encuesta = RespuestaEncuesta.objects.filter(
        usuario=user).order_by('-fecha')[:1]
    total_respuestas = RespuestaPreguntaEncuesta.objects.filter(
        respuesta_encuesta=respuestas_encuesta
    ).aggregate(total=Sum('respuesta')).get('total')
    user = request.user
    ultimas_encuestas = RespuestaEncuesta.objects.filter(
        usuario=user).order_by('-fecha')[:5]
    for encuesta in ultimas_encuestas:
        encuesta.fecha = encuesta.fecha.strftime('%b %d')
    margenizq = 0
    porcentaje_circulo = 0
    porcentaje_numero = 0
    porcentaje_barra = 0
    if total_respuestas <= 44:
        porcentaje_barra = (((((total_respuestas-20)/25)*100)*30)/100)
        margenizq = 0
        porcentaje_circulo = porcentaje_barra + 0
        porcentaje_numero = porcentaje_circulo - 4

    if total_respuestas <= 59 and total_respuestas >= 45:
        porcentaje_barra = (((((total_respuestas-44)/15)*100)*30)/100)
        margenizq = 110
        porcentaje_circulo = porcentaje_barra + 30
        porcentaje_numero = porcentaje_circulo - 4

    if total_respuestas <= 74 and total_respuestas >= 60:
        porcentaje_barra = (((((total_respuestas-59)/15)*100)*30)/100)
        margenizq = 220
        porcentaje_circulo = porcentaje_barra + 70
        porcentaje_numero = porcentaje_circulo - 4

    if total_respuestas >= 75:
        porcentaje_barra = (((((total_respuestas-74)/15)*100)*30)/100)
        margenizq = 330
        porcentaje_circulo = porcentaje_barra + 100
        porcentaje_numero = porcentaje_circulo - 4
    context = {
        'respuestas_encuesta': respuestas_encuesta,
        'ultimas_encuestas': ultimas_encuestas,
        'total_respuestas': total_respuestas,
        'margen_izq': margenizq,
        'porcentaje_barra': porcentaje_barra,
        'porcentaje_circulo': porcentaje_circulo,
        'porcentaje_numero': porcentaje_numero

    }
    return render(request, 'frontend/resultado_encuesta.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirige a la página de inicio después del login exitoso
            return redirect('index')
        else:
            # Mostrar mensaje de error de login inválido
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'frontend/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
