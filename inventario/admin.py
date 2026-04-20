from django.contrib import admin
from .models import Insumo

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'categoria', 'cantidad', 'unidad', 'precio_unitario']
    search_fields = ['nombre']
    list_filter   = ['categoria']