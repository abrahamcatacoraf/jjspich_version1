from django.contrib import admin
from .models import Orden

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display  = ['pk', 'cliente', 'vehiculo', 'estado', 'costo_estimado', 'fecha_ingreso']
    search_fields = ['cliente__nombre', 'vehiculo__placa']
    list_filter   = ['estado']