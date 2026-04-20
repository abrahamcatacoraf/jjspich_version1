from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('clientes/', include('clientes.urls')),
    path('vehiculos/', include('vehiculos.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('inventario/', include('inventario.urls')),
]