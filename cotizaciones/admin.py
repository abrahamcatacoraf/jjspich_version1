from django.contrib import admin
from .models import Cotizacion


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'fecha', 'cliente_nombre', 'vehiculo_placa', 'costo_estimado', 'created_by']
    list_filter = ['fecha']
    search_fields = ['numero', 'cliente_nombre', 'vehiculo_placa']
    readonly_fields = ['numero', 'created_at', 'created_by']
