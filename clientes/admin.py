from django.contrib import admin
from .models import Cliente
from vehiculos.models import Vehiculo


class VehiculoInline(admin.TabularInline):
    model = Vehiculo
    extra = 0
    fields = ['marca', 'modelo', 'placa', 'color', 'categoria']
    readonly_fields = ['fecha_registro']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'apellido', 'ci', 'telefono', 'correo', 'fecha_registro']
    list_display_links = ['nombre', 'apellido']
    search_fields = ['nombre', 'apellido', 'ci', 'telefono']
    date_hierarchy = 'fecha_registro'
    list_per_page = 25
    inlines = [VehiculoInline]