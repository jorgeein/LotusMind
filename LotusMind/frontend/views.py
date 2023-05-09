from django.shortcuts import render
from Lotus.models import Modulo
# Create your views here.


def paginausuario(request):
    return render(request, 'frontend/Perfil_Usuario_Lotusmind.html')


def menu(request):
    return render(request, 'frontend/menu.html')


def index(request):
    return render(request, 'frontend/index.html')


def modulo(request, nombre_mod):
    objetos = Modulo.objects.filter(nombre_mod=nombre_mod).all()

    context = {
        'nombre_mod': nombre_mod,
        'objetos': objetos
    }
    return render(request, 'frontend/plantillamodulo.html', context)
