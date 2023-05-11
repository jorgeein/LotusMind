from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('miusuario', views.paginausuario),
    path('menu', views.menu),
    path('index', views.index),
    path('/<str:nombre_mod>/', views.modulo, name='recurso'),
    path('<str:nombre_mod>/<str:nombre_rec>/', views.recurso, name='recurso'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
