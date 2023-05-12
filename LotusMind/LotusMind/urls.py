
from django.contrib import admin
from django.urls import path, include
from Lotus.api import UsuarioAPI
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Lotus.urls')),
    path('', include('frontend.urls'))
]
