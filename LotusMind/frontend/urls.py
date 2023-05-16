from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('miusuario', views.paginausuario, name="miusuario"),
    path('menu', views.menu),
    path('index', views.index, name="index"),
    path('miencuesta', views.encuesta, name='encuesta'),
    path('<str:nombre_mod>/', views.modulo, name='recurso'),
    path('<str:nombre_mod>/<str:nombre_rec>/',
         views.recurso, name='sigrecurso'),
    path('register', views.register, name="registro")

]
