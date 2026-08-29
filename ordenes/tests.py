from django.contrib.auth.models import User
from django.test import TestCase

from clientes.models import Cliente
from vehiculos.models import Vehiculo
from .models import HistorialAdelanto, Orden


class OrdenModelTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan', apellido='Pérez', ci='12345678', telefono='70012345'
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=self.cliente, categoria='vehiculo', tipo_vehiculo='sedan',
            marca='toyota', modelo='Corolla', anio=2020, placa='1234ABC', color='Rojo',
        )

    def test_estado_por_defecto_recibido(self):
        orden = Orden.objects.create(
            cliente=self.cliente, vehiculo=self.vehiculo,
            descripcion='Reparación de guardabarros',
        )
        self.assertEqual(orden.estado, 'recibido')

    def test_crear_orden_completa(self):
        orden = Orden.objects.create(
            cliente=self.cliente, vehiculo=self.vehiculo,
            descripcion='Pintura de puerta', costo_estimado=800,
            primer_adelanto=300,
        )
        self.assertEqual(Orden.objects.count(), 1)
        self.assertEqual(orden.costo_estimado, 800)
        self.assertIn('Orden', str(orden))

    def test_historial_adelanto(self):
        tecnico = User.objects.create_user(username='tecnico', password='clave1234')
        orden = Orden.objects.create(
            cliente=self.cliente, vehiculo=self.vehiculo,
            descripcion='Cambio de aceite',
        )
        historial = HistorialAdelanto.objects.create(
            orden=orden, usuario=tecnico, accion='registro', monto=200,
            observacion='Primer adelanto',
        )
        self.assertEqual(orden.historial_adelantos.count(), 1)
        self.assertEqual(historial.monto, 200)


class FlujoIntegracionTest(TestCase):
    """Prueba de integración: flujo completo cliente → vehículo → orden → pago."""

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='clave1234')
        self.client.login(username='admin', password='clave1234')

    def test_flujo_completo_via_formularios(self):
        # 1. Crear cliente
        response = self.client.post('/clientes/nuevo/', {
            'nombre': 'María', 'apellido': 'Gómez', 'ci': '87654321',
            'telefono': '70123456', 'correo': 'maria@example.com', 'direccion': 'Av. Bolívar',
        })
        self.assertEqual(response.status_code, 302)
        cliente = Cliente.objects.get(ci='87654321')

        # 2. Crear vehículo
        response = self.client.post('/vehiculos/nuevo/', {
            'cliente': cliente.pk, 'categoria': 'vehiculo', 'tipo_vehiculo': 'suv',
            'marca': 'nissan', 'modelo': 'X-Trail', 'anio': 2021,
            'placa': '9876zyx', 'color': 'Azul',
            'kilometraje': '45000', 'gasolina': '60',
        })
        self.assertEqual(response.status_code, 302)
        vehiculo = Vehiculo.objects.get(placa='9876ZYX')

        # 3. Crear orden de trabajo
        response = self.client.post('/ordenes/nueva/', {
            'cliente': cliente.pk, 'vehiculo': vehiculo.pk,
            'descripcion': 'Reparación de chapa y pintura',
            'diagnostico': 'Abolladura en puerta izquierda',
            'estado': 'recibido', 'costo_estimado': 1500, 'primer_adelanto': 0,
        })
        self.assertEqual(response.status_code, 302)
        orden = Orden.objects.get(vehiculo=vehiculo)
        self.assertEqual(orden.pagos.count(), 0)

        # 4. Registrar un pago (adelanto)
        response = self.client.post('/pagos/nuevo/', {
            'orden': orden.pk, 'monto': 500, 'metodo': 'efectivo',
            'tipo_pago': 'adelanto', 'observacion': '',
        })
        self.assertEqual(response.status_code, 302)
        orden.refresh_from_db()
        self.assertEqual(orden.pagos.count(), 1)
        self.assertTrue(orden.pagos.first().es_adelanto)
        self.assertEqual(orden.estado, 'en_proceso')

    def test_flujo_sin_login_redirige(self):
        self.client.logout()
        response = self.client.get('/clientes/')
        self.assertEqual(response.status_code, 302)