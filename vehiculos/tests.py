from django.contrib.auth.models import User
from django.test import TestCase

from clientes.models import Cliente
from .forms import VehiculoForm
from .models import Vehiculo


class VehiculoModelTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan', apellido='Pérez', ci='12345678', telefono='70012345'
        )

    def _crear_vehiculo(self, **kwargs):
        datos = {
            'cliente': self.cliente,
            'categoria': 'vehiculo',
            'tipo_vehiculo': 'sedan',
            'marca': 'toyota',
            'modelo': 'Corolla',
            'anio': 2020,
            'placa': '1234abc',
            'color': 'Rojo',
        }
        datos.update(kwargs)
        return Vehiculo.objects.create(**datos)

    def test_placa_se_guarda_en_mayusculas(self):
        vehiculo = self._crear_vehiculo(placa='1234abc')
        self.assertEqual(vehiculo.placa, '1234ABC')

    def test_tipo_moto_nulo_si_categoria_vehiculo(self):
        vehiculo = self._crear_vehiculo(
            categoria='vehiculo', tipo_vehiculo='sedan', tipo_moto='estandar'
        )
        self.assertEqual(vehiculo.tipo_vehiculo, 'sedan')
        self.assertIsNone(vehiculo.tipo_moto)

    def test_tipo_vehiculo_nulo_si_categoria_moto(self):
        vehiculo = self._crear_vehiculo(
            categoria='motocicleta', tipo_moto='estandar', tipo_vehiculo='sedan'
        )
        self.assertEqual(vehiculo.tipo_moto, 'estandar')
        self.assertIsNone(vehiculo.tipo_vehiculo)

    def test_str_vehiculo(self):
        vehiculo = self._crear_vehiculo()
        self.assertIn('toyota', str(vehiculo))
        self.assertIn('1234ABC', str(vehiculo))

    def test_get_tipo_display_completo_vehiculo(self):
        vehiculo = self._crear_vehiculo(categoria='vehiculo', tipo_vehiculo='sedan')
        self.assertEqual(vehiculo.get_tipo_display_completo(), 'Sedán')


class VehiculoFormTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan', apellido='Pérez', ci='12345678', telefono='70012345'
        )

    def test_formulario_valido(self):
        form = VehiculoForm(data={
            'cliente': self.cliente.pk,
            'categoria': 'vehiculo',
            'tipo_vehiculo': 'sedan',
            'marca': 'toyota',
            'modelo': 'Corolla',
            'anio': 2020,
            'placa': '1234ABC',
            'color': 'Rojo',
            'kilometraje': '45000',
            'gasolina': '60',
        })
        self.assertTrue(form.is_valid())

    def test_formulario_sin_placa_invalido(self):
        form = VehiculoForm(data={
            'cliente': self.cliente.pk,
            'categoria': 'vehiculo',
            'tipo_vehiculo': 'sedan',
            'marca': 'toyota',
            'modelo': 'Corolla',
            'anio': 2020,
            'placa': '',
            'color': 'Rojo',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('placa', form.errors)


class VehiculosViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='clave1234')
        self.client.login(username='admin', password='clave1234')
        self.cliente = Cliente.objects.create(
            nombre='Juan', apellido='Pérez', ci='12345678', telefono='70012345'
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=self.cliente, categoria='vehiculo', tipo_vehiculo='sedan',
            marca='toyota', modelo='Corolla', anio=2020, placa='1234ABC', color='Rojo',
        )

    def test_ajax_vehiculos_por_cliente(self):
        response = self.client.get(
            '/vehiculos/api/por-cliente/', {'cliente_id': self.cliente.pk}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['placa'], '1234ABC')

    def test_lista_vehiculos_requiere_login(self):
        self.client.logout()
        response = self.client.get('/vehiculos/')
        self.assertEqual(response.status_code, 302)

    def test_eliminar_vehiculo_solo_admin(self):
        tecnico = User.objects.create_user(username='tecnico', password='clave1234')
        self.client.logout()
        self.client.login(username='tecnico', password='clave1234')
        response = self.client.get(f'/vehiculos/eliminar/{self.vehiculo.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vehiculo.objects.filter(pk=self.vehiculo.pk).exists())