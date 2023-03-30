from django.shortcuts import render

# Create your views here.


def paginausuario(request):
    return render(request, 'frontend/Perfil_Usuario_Lotusmind.html')

def menu(request):
    return render(request, 'frontend/menu.html')
