from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('miusuario', views.paginausuario, name="miusuario"),
    path('menu', views.menu),
    path('index', views.index, name="index"),
<<<<<<< HEAD
    path('miencuesta', views.encuesta, name='encuesta'),
    path('<str:nombre_mod>/', views.modulo, name='recurso'),
=======
    path('escala', views.escala),
    path('login', views.login),
    path('register', views.register),
    path('auth', views.auth),
    path('/<str:nombre_mod>/', views.modulo, name='recurso'),
>>>>>>> 0aab0199331b29c7abe43026a38d2bcf3a14ef82
    path('<str:nombre_mod>/<str:nombre_rec>/',
         views.recurso, name='sigrecurso'),
    path('register', views.register, name="registro")

]
