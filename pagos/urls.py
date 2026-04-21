from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pagos, name='lista_pagos'),
    path('nuevo/', views.nuevo_pago, name='nuevo_pago'),
    path('orden/<int:orden_pk>/', views.detalle_orden_pagos, name='detalle_orden_pagos'),
    path('eliminar/<int:pk>/', views.eliminar_pago, name='eliminar_pago'),
]