
from django.contrib import admin
from django.urls import path, include
from Lotus.api import UsuarioAPI
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Lotus.urls')),
    path('', include('frontend.urls'))
]
