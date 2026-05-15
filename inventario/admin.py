from django.contrib import admin
from .models import Insumo, MovimientoInsumo

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'categoria', 'cantidad', 'unidad', 'precio_unitario', 'stock_bajo_admin', 'valor_total']
    list_display_links = ['nombre']
    search_fields = ['nombre']
    list_filter   = ['categoria', 'stock_minimo']
    list_per_page = 25

    def stock_bajo_admin(self, obj):
        return obj.stock_bajo
    stock_bajo_admin.short_description = "Stock bajo"
    stock_bajo_admin.boolean = True

@admin.register(MovimientoInsumo)
class MovimientoInsumoAdmin(admin.ModelAdmin):
    list_display  = ['fecha', 'insumo', 'tipo', 'cantidad_movimiento', 'cantidad_actual']
    list_filter   = ['tipo', 'fecha', 'insumo']
    date_hierarchy = 'fecha'
    readonly_fields = ['insumo', 'tipo', 'precio_unitario', 'cantidad_inicial', 'cantidad_movimiento', 'cantidad_actual', 'fecha']