from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display  = ['orden', 'monto', 'metodo', 'tipo_pago', 'fecha']
    search_fields = ['orden__cliente__nombre']
    list_filter   = ['metodo', 'es_adelanto', 'fecha']
    date_hierarchy = 'fecha'
    list_per_page = 25

    def tipo_pago(self, obj):
        return "Adelanto" if obj.es_adelanto else "Pago final"
    tipo_pago.short_description = "Tipo"