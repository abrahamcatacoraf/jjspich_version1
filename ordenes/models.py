from django.db import models
from clientes.models import Cliente
from vehiculos.models import Vehiculo

class Orden(models.Model):
    ESTADOS = [
        ('recibido',    'Recibido'),
        ('en_proceso',  'En proceso'),
        ('terminado',   'Terminado'),
        ('entregado',   'Entregado'),
    ]

    cliente         = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vehiculo        = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    descripcion     = models.TextField(verbose_name='Descripción del trabajo')
    diagnostico     = models.TextField(blank=True, null=True)
    estado          = models.CharField(max_length=20, choices=ESTADOS, default='recibido')
    fecha_ingreso   = models.DateTimeField(auto_now_add=True)
    fecha_entrega   = models.DateField(blank=True, null=True)
    costo_estimado  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tecnico         = models.CharField(max_length=100, blank=True, null=True)
    observaciones   = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.pk} — {self.vehiculo} ({self.estado})"

    class Meta:
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Órdenes de trabajo"
        ordering = ['-fecha_ingreso']