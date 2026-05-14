from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_vehiculos, name='lista_vehiculos'),
    path('nuevo/', views.nuevo_vehiculo, name='nuevo_vehiculo'),
    path('editar/<int:pk>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('eliminar/<int:pk>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('api/por-cliente/', views.vehiculos_por_cliente, name='vehiculos_por_cliente'),
]