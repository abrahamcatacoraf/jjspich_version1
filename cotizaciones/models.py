from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Cotizacion(models.Model):
    numero = models.CharField(max_length=20, unique=True, editable=False,
                              verbose_name='N° de cotización')
    fecha = models.DateField(default=timezone.localdate,
                             verbose_name='Fecha de emisión')
    plazo = models.CharField(max_length=50, verbose_name='Plazo de validez',
                             help_text='Ej: 15 días, 30 días')
    tecnico = models.CharField(max_length=100, verbose_name='Técnico')
    cliente_nombre = models.CharField(max_length=200, verbose_name='Cliente')
    vehiculo_marca = models.CharField(max_length=50, verbose_name='Marca')
    vehiculo_modelo = models.CharField(max_length=50, verbose_name='Modelo')
    vehiculo_placa = models.CharField(max_length=20, verbose_name='Placa')
    vehiculo_color = models.CharField(max_length=30, verbose_name='Color')
    vehiculo_anio = models.IntegerField(verbose_name='Año')
    diagnostico = models.TextField(verbose_name='Diagnóstico técnico')
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2,
                                         verbose_name='Costo estimado (Bs.)')
    notas = models.TextField(blank=True, null=True,
                             verbose_name='Notas adicionales',
                             help_text='Términos, garantía, condiciones')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Fecha de creación')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   verbose_name='Creado por')

    def save(self, *args, **kwargs):
        self.vehiculo_placa = self.vehiculo_placa.upper()
        if not self.numero:
            año = timezone.now().year
            ultima = Cotizacion.objects.filter(
                numero__startswith=f'COT-{año}-'
            ).order_by('numero').last()
            if ultima:
                sec = int(ultima.numero.split('-')[-1]) + 1
            else:
                sec = 1
            self.numero = f'COT-{año}-{sec:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero} — {self.cliente_nombre} ({self.vehiculo_placa})"

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ['-created_at']
