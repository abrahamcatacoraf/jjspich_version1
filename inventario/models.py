from django.db import models

class Insumo(models.Model):
    CATEGORIAS = [
        ('pintura',    'Pintura'),
        ('lija',       'Lija'),
        ('masilla',    'Masilla'),
        ('soldadura',  'Soldadura'),
        ('quimico',    'Químico'),
        ('herramienta','Herramienta'),
        ('otro',       'Otro'),
    ]
    nombre      = models.CharField(max_length=100)
    categoria   = models.CharField(max_length=20, choices=CATEGORIAS, default='otro')
    descripcion = models.TextField(blank=True, null=True)
    cantidad    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad      = models.CharField(max_length=20, default='unidad',
                    help_text='Ej: litro, unidad, kilo, metro')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo    = models.DecimalField(max_digits=10, decimal_places=2, default=5,
                    help_text='Alerta cuando el stock baje de este número')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad} {self.unidad})"

    @property
    def stock_bajo(self):
        return self.cantidad <= self.stock_minimo

    @property
    def valor_total(self):
        return self.cantidad * self.precio_unitario

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Inventario"
        ordering = ['categoria', 'nombre']