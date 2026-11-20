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

    def _datos_edicion(self, **cambios):
        datos = {
            'fecha': date.today().isoformat(),
            'plazo': '30 días',
            'tecnico': 'Luis Mamani',
            'cliente_nombre': 'Juan Pérez Actualizado',
            'vehiculo_marca': 'Toyota',
            'vehiculo_modelo': 'Corolla',
            'vehiculo_placa': '1234ABC',
            'vehiculo_color': 'Azul',
            'vehiculo_anio': 2020,
            'diagnostico': 'Reparación completa de carrocería',
            'costo_estimado': '950.00',
            'notas': '',
        }
        datos.update(cambios)
        return datos

    def test_editar_cotizacion_get(self):
        response = self.client.get(f'/cotizaciones/{self.cotizacion.pk}/editar/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editar Cotización')

    def test_editar_cotizacion_actualiza_datos(self):
        response = self.client.post(
            f'/cotizaciones/{self.cotizacion.pk}/editar/',
            self._datos_edicion(),
        )
        self.assertEqual(response.status_code, 302)
        self.cotizacion.refresh_from_db()
        self.assertEqual(self.cotizacion.cliente_nombre, 'Juan Pérez Actualizado')
        self.assertEqual(self.cotizacion.vehiculo_color, 'Azul')
        self.assertEqual(self.cotizacion.plazo, '30 días')
        self.assertEqual(self.cotizacion.tecnico, 'Luis Mamani')
        self.assertEqual(str(self.cotizacion.costo_estimado), '950.00')

    def test_editar_conserva_numero(self):
        numero_original = self.cotizacion.numero
        self.client.post(
            f'/cotizaciones/{self.cotizacion.pk}/editar/',
            self._datos_edicion(),
        )
        self.cotizacion.refresh_from_db()
        self.assertEqual(self.cotizacion.numero, numero_original)

    def test_editar_placa_se_guarda_en_mayusculas(self):
        self.client.post(
            f'/cotizaciones/{self.cotizacion.pk}/editar/',
            self._datos_edicion(vehiculo_placa='abcd123'),
        )
        self.cotizacion.refresh_from_db()
        self.assertEqual(self.cotizacion.vehiculo_placa, 'ABCD123')

    def test_editar_muestra_errores_si_falta_campo(self):
        datos = self._datos_edicion(cliente_nombre='')
        response = self.client.post(
            f'/cotizaciones/{self.cotizacion.pk}/editar/', datos)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid-feedback')
        self.cotizacion.refresh_from_db()
        self.assertEqual(self.cotizacion.cliente_nombre, 'Juan Pérez')

    def test_editar_requiere_login(self):
        self.client.logout()
        response = self.client.get(f'/cotizaciones/{self.cotizacion.pk}/editar/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)