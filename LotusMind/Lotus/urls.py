from rest_framework import routers
from .api import UsuarioViewSet
from Lotus.api import UsuarioAPI
from django.urls import path
router = routers.DefaultRouter()
router.register('api/Usuario', UsuarioViewSet, 'Usuario')

urlpatterns = [
    path('api/usuario/crearusuario/', UsuarioAPI.as_view(), name="crearusuario"),
]

urlpatterns += router.urls
