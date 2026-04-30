from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'apellido', 'ci', 'telefono', 'correo', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'ci', 'telefono']