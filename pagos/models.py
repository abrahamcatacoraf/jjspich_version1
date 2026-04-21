from django.db import models
from ordenes.models import Orden

class Pago(models.Model):
    METODOS = [
        ('efectivo',     'Efectivo'),
        ('transferencia','Transferencia'),
        ('qr',           'QR'),
        ('otro',         'Otro'),
    ]

    orden       = models.ForeignKey(Orden, on_delete=models.PROTECT, related_name='pagos')
    monto       = models.DecimalField(max_digits=10, decimal_places=2)
    metodo      = models.CharField(max_length=20, choices=METODOS, default='efectivo')
    es_adelanto = models.BooleanField(default=False)
    fecha       = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        tipo = "Adelanto" if self.es_adelanto else "Pago"
        return f"{tipo} de Bs.{self.monto} — Orden #{self.orden.pk}"

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha']