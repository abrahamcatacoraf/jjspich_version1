from django.db import models
from django.contrib.auth.models import User


class Auditoria(models.Model):
    ACCIONES = [
        ('creacion',    'Creación'),
        ('edicion',     'Edición'),
        ('eliminacion', 'Eliminación'),
    ]

    usuario   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion    = models.CharField(max_length=20, choices=ACCIONES)
    modelo    = models.CharField(max_length=50)
    objeto_id = models.PositiveIntegerField(blank=True, null=True)
    detalle   = models.TextField()
    fecha     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_accion_display()} — {self.modelo} #{self.objeto_id} — {self.usuario}"

    class Meta:
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Auditoría"
        ordering = ['-fecha']
