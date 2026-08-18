from django.urls import path

from . import views

urlpatterns = [
    path('configurar/', views.configurar_2fa, name='configurar_2fa'),
    path('desactivar/', views.desactivar_2fa, name='desactivar_2fa'),
]