from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordenes, name='lista_ordenes'),
    path('nueva/', views.nueva_orden, name='nueva_orden'),
    path('editar/<int:pk>/', views.editar_orden, name='editar_orden'),
    path('detalle/<int:pk>/', views.detalle_orden, name='detalle_orden'),
    path('eliminar/<int:pk>/', views.eliminar_orden, name='eliminar_orden'),
]