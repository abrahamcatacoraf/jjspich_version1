from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ['marca', 'modelo', 'placa', 'color', 'cliente']
    search_fields = ['marca', 'modelo', 'placa']
    list_filter   = ['tipo', 'marca']