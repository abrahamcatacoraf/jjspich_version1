from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cotizaciones, name='lista_cotizaciones'),
    path('nueva/', views.nueva_cotizacion, name='nueva_cotizacion'),
    path('<int:pk>/', views.detalle_cotizacion, name='detalle_cotizacion'),
    path('<int:pk>/pdf/', views.pdf_cotizacion, name='pdf_cotizacion'),
    path('<int:pk>/preview/', views.preview_cotizacion, name='preview_cotizacion'),
    path('<int:pk>/ver/', views.ver_cotizacion_pdf, name='ver_cotizacion_pdf'),
    path('<int:pk>/editar/', views.editar_cotizacion, name='editar_cotizacion'),
    path('<int:pk>/eliminar/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
]
