from django.shortcuts import render
from Lotus.models import Modulo, Recurso, ModuloRecurso
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
