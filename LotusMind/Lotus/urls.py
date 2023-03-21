from rest_framework import routers
from .api import UsuarioViewSet
from Lotus.api import UsuarioAPI
from django.urls import path
router = routers.DefaultRouter()
router.register('api/User', UsuarioViewSet, 'usuario')

urlpatterns = router.urls

urlpatterns = [
    path('api/usuario/crearusuario/', UsuarioAPI.as_view(), name="crearusuario"),
]
