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
    path('auditoria/', include('auditoria.urls')),
    path('cotizaciones/', include('cotizaciones.urls')),

    path('reportes/', views.vista_reportes, name='reportes'),
    path('reportes/preview/ordenes/', views.preview_ordenes, name='preview_ordenes'),
    path('reportes/preview/pagos/', views.preview_pagos, name='preview_pagos'),
    path('reportes/preview/inventario/', views.preview_inventario, name='preview_inventario'),
    path('reportes/preview/inventario/movimientos/', views.preview_movimientos_inventario, name='preview_movimientos_inventario'),
    path('reportes/preview/pagos/orden/', views.preview_pagos_orden, name='preview_pagos_orden'),
    path('reportes/pdf/ordenes/', views.pdf_ordenes, name='pdf_ordenes'),
    path('reportes/pdf/pagos/', views.pdf_pagos, name='pdf_pagos'),
    path('reportes/pdf/inventario/', views.pdf_inventario, name='pdf_inventario'),
    path('reportes/pdf/inventario/movimientos/', views.pdf_movimientos_inventario, name='pdf_movimientos_inventario'),

    path('reportes/pdf/pagos/orden/', views.pdf_pagos_orden, name='pdf_pagos_orden'),

    path('sin-permiso/', sin_permiso, name='sin_permiso'),
]