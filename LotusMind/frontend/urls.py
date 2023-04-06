from django.urls import path, include

from . import views
urlpatterns = [
    path('miusuario', views.paginausuario),
    path('menu', views.menu),
    path('index', views.index)
]
