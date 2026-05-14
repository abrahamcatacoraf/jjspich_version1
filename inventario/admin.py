from django.contrib import admin
from .models import Insumo, MovimientoInsumo

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'categoria', 'cantidad', 'unidad', 'precio_unitario']
    search_fields = ['nombre']
    list_filter   = ['categoria']

@admin.register(MovimientoInsumo)
class MovimientoInsumoAdmin(admin.ModelAdmin):
    list_display  = ['fecha', 'insumo', 'tipo', 'cantidad_movimiento', 'cantidad_actual']
    list_filter   = ['tipo', 'fecha']
    readonly_fields = ['insumo', 'tipo', 'precio_unitario', 'cantidad_inicial', 'cantidad_movimiento', 'cantidad_actual', 'fecha']