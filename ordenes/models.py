from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from vehiculos.models import Vehiculo

class Orden(models.Model):
    ESTADOS = [
        ('recibido',   'Recibido'),
        ('en_proceso', 'En proceso'),
        ('terminado',  'Terminado'),
        ('entregado',  'Entregado'),
    ]

    cliente          = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    vehiculo         = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    descripcion      = models.TextField(verbose_name='Descripción del trabajo')
    diagnostico      = models.TextField(blank=True, null=True)
    estado           = models.CharField(max_length=20, choices=ESTADOS, default='recibido')
    fecha_recepcion  = models.DateField(blank=True, null=True,
                         verbose_name='Fecha de recepción del vehículo')
    fecha_ingreso    = models.DateTimeField(auto_now_add=True)
    fecha_entrega    = models.DateField(blank=True, null=True)
    costo_estimado   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    primer_adelanto  = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                         verbose_name='Primer adelanto (Bs.)')
    tecnico          = models.ForeignKey(User, on_delete=models.SET_NULL,
                         null=True, blank=True,
                         related_name='ordenes_asignadas',
                         verbose_name='Técnico asignado',
                         limit_choices_to={'groups__name': 'Tecnico'})
    observaciones    = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.pk} — {self.vehiculo} ({self.estado})"

    class Meta:
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Órdenes de trabajo"
        ordering = ['-fecha_ingreso']


class HistorialAdelanto(models.Model):
    ACCIONES = [
        ('registro', 'Registro'),
        ('edicion',  'Edición'),
    ]
    orden       = models.ForeignKey(Orden, on_delete=models.CASCADE,
                    related_name='historial_adelantos')
    usuario     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion      = models.CharField(max_length=20, choices=ACCIONES, default='registro')
    monto       = models.DecimalField(max_digits=10, decimal_places=2)
    fecha       = models.DateTimeField(auto_now_add=True)
    observacion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.accion} — Orden #{self.orden.pk} — {self.usuario}"

    class Meta:
        verbose_name = "Historial de adelanto"
        verbose_name_plural = "Historial de adelantos"
        ordering = ['-fecha']