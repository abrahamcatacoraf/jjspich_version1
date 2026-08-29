from datetime import date

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase

from .models import Cotizacion


class CotizacionModelTest(TestCase):

    def test_numero_automatico_secuencial(self):
        c1 = Cotizacion.objects.create(
            fecha=date.today(), plazo='15 días', tecnico='Carlos',
            cliente_nombre='Juan Pérez', vehiculo_marca='Toyota',
            vehiculo_modelo='Corolla', vehiculo_placa='1234abc',
            vehiculo_color='Rojo', vehiculo_anio=2020,
            diagnostico='Reparación de guardabarros', costo_estimado=800,
        )
        c2 = Cotizacion.objects.create(
            fecha=date.today(), plazo='15 días', tecnico='Carlos',
            cliente_nombre='María Gómez', vehiculo_marca='Nissan',
            vehiculo_modelo='X-Trail', vehiculo_placa='9876zyx',
            vehiculo_color='Azul', vehiculo_anio=2021,
            diagnostico='Pintura de puerta', costo_estimado=1200,
        )
        self.assertEqual(c1.numero, f'COT-{date.today().year}-001')
        self.assertEqual(c2.numero, f'COT-{date.today().year}-002')

    def test_placa_se_guarda_en_mayusculas(self):
        cotizacion = Cotizacion.objects.create(
            fecha=date.today(), plazo='30 días', tecnico='Carlos',
            cliente_nombre='Juan Pérez', vehiculo_marca='Toyota',
            vehiculo_modelo='Corolla', vehiculo_placa='abc123',
            vehiculo_color='Rojo', vehiculo_anio=2020,
            diagnostico='Cambio de ópticas', costo_estimado=300,
        )
        self.assertEqual(cotizacion.vehiculo_placa, 'ABC123')

    def test_str_cotizacion(self):
        cotizacion = Cotizacion.objects.create(
            fecha=date.today(), plazo='15 días', tecnico='Carlos',
            cliente_nombre='Juan Pérez', vehiculo_marca='Toyota',
            vehiculo_modelo='Corolla', vehiculo_placa='1234ABC',
            vehiculo_color='Rojo', vehiculo_anio=2020,
            diagnostico='Reparación', costo_estimado=800,
        )
        self.assertIn('Juan Pérez', str(cotizacion))
        self.assertIn('1234ABC', str(cotizacion))


class CotizacionViewTest(TestCase):

    def setUp(self):
        call_command('crear_grupos')
        self.admin = User.objects.create_user(username='admin', password='clave1234')
        self.admin.groups.add(Group.objects.get(name='Administrador'))
        self.client.login(username='admin', password='clave1234')
        self.cotizacion = Cotizacion.objects.create(
            fecha=date.today(), plazo='15 días', tecnico='Carlos',
            cliente_nombre='Juan Pérez', vehiculo_marca='Toyota',
            vehiculo_modelo='Corolla', vehiculo_placa='1234ABC',
            vehiculo_color='Rojo', vehiculo_anio=2020,
            diagnostico='Reparación', costo_estimado=800,
        )

    def test_pdf_cotizacion_genera_archivo(self):
        response = self.client.get(f'/cotizaciones/{self.cotizacion.pk}/pdf/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_detalle_cotizacion_requiere_login(self):
        self.client.logout()
        response = self.client.get(f'/cotizaciones/{self.cotizacion.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_eliminar_cotizacion_solo_admin(self):
        tecnico = User.objects.create_user(username='tecnico', password='clave1234')
        tecnico.groups.add(Group.objects.get(name='Tecnico'))
        self.client.logout()
        self.client.login(username='tecnico', password='clave1234')
        response = self.client.get(f'/cotizaciones/{self.cotizacion.pk}/eliminar/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/sin-permiso/')
        self.assertTrue(Cotizacion.objects.filter(pk=self.cotizacion.pk).exists())