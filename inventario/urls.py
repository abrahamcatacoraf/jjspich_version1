from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_inventario, name='lista_inventario'),
    path('nuevo/', views.nuevo_insumo, name='nuevo_insumo'),
    path('editar/<int:pk>/', views.editar_insumo, name='editar_insumo'),
    path('ajustar/<int:pk>/', views.ajustar_stock, name='ajustar_stock'),
    path('eliminar/<int:pk>/', views.eliminar_insumo, name='eliminar_insumo'),
]