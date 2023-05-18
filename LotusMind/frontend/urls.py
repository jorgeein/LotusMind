from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('miusuario', views.paginausuario, name="miusuario"),
    path('menu', views.menu),
    path('index', views.index, name="index"),
    path('miencuesta/', views.encuesta),
    path('escala', views.escala),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register),
    path('auth', views.auth),
    path('encuesta/<int:pregunta_id>/<int:respuesta_encuesta_id>/',
         views.encuesta, name='encuesta'),
    path('resultado_encuesta/<int:respuesta_encuesta_id>/', views.resultado_encuesta, name='resultado_encuesta'),
    path('<str:nombre_mod>/', views.modulo, name='recurso'),
    path('<str:nombre_mod>/<str:nombre_rec>/',
         views.recurso, name='sigrecurso'),
    path('register', views.register, name="registro")
]
