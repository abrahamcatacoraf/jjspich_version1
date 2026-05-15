from django.contrib import admin
from .models import Orden
from pagos.models import Pago


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 0
    fields = ['monto', 'metodo', 'es_adelanto', 'fecha']
    readonly_fields = ['fecha']


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display  = ['pk', 'cliente', 'vehiculo', 'estado', 'costo_estimado', 'tecnico', 'fecha_ingreso']
    list_display_links = ['pk']
    search_fields = ['cliente__nombre', 'vehiculo__placa']
    list_filter   = ['estado', 'fecha_ingreso']
    date_hierarchy = 'fecha_ingreso'
    list_per_page = 25
    inlines = [PagoInline]
    fieldsets = [
        ('Cliente y vehículo', {
            'fields': ['cliente', 'vehiculo']
        }),
        ('Trabajo realizado', {
            'fields': ['descripcion', 'diagnostico', 'estado', 'tecnico']
        }),
        ('Fechas', {
            'fields': ['fecha_recepcion', 'fecha_entrega']
        }),
        ('Costos', {
            'fields': ['costo_estimado', 'primer_adelanto']
        }),
        ('Observaciones', {
            'fields': ['observaciones']
        }),
    ]