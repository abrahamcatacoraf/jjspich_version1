from django.db import models
from django.contrib.auth.models import User


class ClaveTOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='totp', verbose_name='Usuario')
    secreto = models.CharField(max_length=64, verbose_name='Secreto TOTP')
    activa = models.BooleanField(default=False, verbose_name='Activa')

    class Meta:
        verbose_name = 'Clave TOTP'
        verbose_name_plural = 'Claves TOTP'

    def __str__(self):
        estado = 'activa' if self.activa else 'inactiva'
        return f'2FA {estado} — {self.user.username}'