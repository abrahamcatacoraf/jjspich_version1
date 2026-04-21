from django.contrib import admin
from .models import Pago

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display  = ['orden', 'monto', 'metodo', 'es_adelanto', 'fecha']
    search_fields = ['orden__cliente__nombre']
    list_filter   = ['metodo', 'es_adelanto']