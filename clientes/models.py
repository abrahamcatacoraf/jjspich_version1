from django.db import models

class Cliente(models.Model):
    nombre      = models.CharField(max_length=100)
    apellido    = models.CharField(max_length=100)
    ci          = models.CharField(max_length=20, unique=True,
                    verbose_name='Carnet de Identidad')
    telefono    = models.CharField(max_length=20)
    correo      = models.EmailField(blank=True, null=True)
    direccion   = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido']