from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ['marca', 'modelo', 'placa', 'color', 'categoria', 'cliente']
    list_display_links = ['marca', 'modelo', 'placa']
    search_fields = ['marca', 'modelo', 'placa', 'cliente__nombre', 'cliente__apellido']
    list_filter   = ['categoria', 'marca', 'anio']
    readonly_fields = ['fecha_registro']