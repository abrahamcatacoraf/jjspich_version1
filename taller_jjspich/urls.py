from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

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
]