
from django.contrib import admin
from django.urls import path, include
from Lotus.api import UsuarioAPI
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    # Otras URLs de tu proyecto Django
    path('admin/', admin.site.urls),
    path('social-auth/', include('allauth.urls')),
    path('lotusmind', include('Lotus.urls')),
    path("accounts/", include("allauth.urls")),
    path('', include('frontend.urls'))
    # Otras URLs de tu proyecto Django
]
