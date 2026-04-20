from django.db import models
from clientes.models import Cliente

class Vehiculo(models.Model):
    TIPOS = [
        ('sedan', 'Sedán'),
        ('suv', 'SUV'),
        ('pickup', 'Pickup'),
        ('hatchback', 'Hatchback'),
        ('camioneta', 'Camioneta'),
        ('otro', 'Otro'),
    ]
    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos')
    marca       = models.CharField(max_length=50)
    modelo      = models.CharField(max_length=50)
    anio        = models.IntegerField()
    placa       = models.CharField(max_length=20, unique=True)
    color       = models.CharField(max_length=30)
    tipo        = models.CharField(max_length=20, choices=TIPOS, default='sedan')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} — {self.placa}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['marca']