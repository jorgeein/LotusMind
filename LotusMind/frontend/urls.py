from django.urls import path, include

from . import views
urlpatterns = [
    path('miusuario', views.paginausuario),
    path('menu', views.menu),
    path('index', views.index),
    path('mi_ruta/<str:nombre_mod>/', views.modulo, name='mi_url'),

]
