from django.shortcuts import render

# Create your views here.

def paginausuario(request):
    return render(request, 'frontend/Perfil_Uusario_Lotusmind.html')