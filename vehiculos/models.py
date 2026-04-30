from django.db import models
from clientes.models import Cliente

class Vehiculo(models.Model):
    TIPOS_VEHICULO = [
        ('sedan',     'Sedán'),
        ('suv',       'SUV'),
        ('pickup',    'Pickup'),
        ('hatchback', 'Hatchback'),
        ('camioneta', 'Camioneta'),
        ('minibus',   'Minibús'),
        ('vagoneta',  'Vagoneta'),
        ('automovil', 'Automóvil'),
        ('otro',      'Otro'),
    ]
    TIPOS_MOTO = [
        ('estandar',    'Estándar'),
        ('chopper',     'Chopper'),
        ('deportivo',   'Deportivo'),
        ('cuadratrack', 'Cuadratrack'),
        ('otro_moto',   'Otro'),
    ]
    CATEGORIA = [
        ('vehiculo',    'Vehículo'),
        ('motocicleta', 'Motocicleta'),
    ]

    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE,
                    related_name='vehiculos')
    categoria   = models.CharField(max_length=20, choices=CATEGORIA,
                    default='vehiculo', verbose_name='Categoría')
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPOS_VEHICULO,
                    blank=True, null=True, verbose_name='Tipo de vehículo')
    tipo_moto   = models.CharField(max_length=20, choices=TIPOS_MOTO,
                    blank=True, null=True, verbose_name='Tipo de motocicleta')
    marca       = models.CharField(max_length=50)
    modelo      = models.CharField(max_length=50)
    anio        = models.IntegerField(verbose_name='Año')
    placa       = models.CharField(max_length=20, unique=True)
    color       = models.CharField(max_length=30)
    kilometraje = models.DecimalField(max_digits=10, decimal_places=2,
                    default=0, verbose_name='Kilometraje (km)')
    gasolina    = models.DecimalField(max_digits=5, decimal_places=2,
                    default=0, verbose_name='Gasolina en tanque (%)',
                    help_text='Porcentaje de gasolina, de 0 a 100')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Convertir placa a mayúsculas automáticamente
        self.placa = self.placa.upper()
        # Limpiar el tipo que no corresponde
        if self.categoria == 'vehiculo':
            self.tipo_moto = None
        elif self.categoria == 'motocicleta':
            self.tipo_vehiculo = None
        super().save(*args, **kwargs)

    def get_tipo_display_completo(self):
        if self.categoria == 'vehiculo' and self.tipo_vehiculo:
            return dict(self.TIPOS_VEHICULO).get(self.tipo_vehiculo, '—')
        elif self.categoria == 'motocicleta' and self.tipo_moto:
            return dict(self.TIPOS_MOTO).get(self.tipo_moto, '—')
        return '—'

    def __str__(self):
        return f"{self.marca} {self.modelo} — {self.placa}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['marca']