from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import render

def sin_permiso(request):
    return render(request, 'base/sin_permiso.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login y logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Sistema
    path('', views.dashboard, name='dashboard'),
    path('clientes/', include('clientes.urls')),
    path('vehiculos/', include('vehiculos.urls')),
    path('ordenes/', include('ordenes.urls')),
    path('inventario/', include('inventario.urls')),
    path('pagos/', include('pagos.urls')),

    # Reportes
    path('reportes/', views.vista_reportes, name='reportes'),
    path('reportes/pdf/ordenes/', views.pdf_ordenes, name='pdf_ordenes'),
    path('reportes/pdf/pagos/', views.pdf_pagos, name='pdf_pagos'),
    path('reportes/pdf/inventario/', views.pdf_inventario, name='pdf_inventario'),

    path('sin-permiso/', sin_permiso, name='sin_permiso'),
]