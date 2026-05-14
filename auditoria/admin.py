from django.contrib import admin
from .models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'modelo', 'objeto_id')
    list_filter = ('accion', 'modelo', 'fecha')
    search_fields = ('detalle', 'usuario__username')
    readonly_fields = ('usuario', 'accion', 'modelo', 'objeto_id', 'detalle', 'fecha')
