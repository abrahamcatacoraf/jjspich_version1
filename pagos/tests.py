from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from clientes.models import Cliente
from vehiculos.models import Vehiculo
from ordenes.models import Orden
from .forms import PagoForm
from .models import Pago


class PagoModelTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan', apellido='Pérez', ci='12345678', telefono='70012345'
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=self.cliente, categoria='vehiculo', tipo_vehiculo='sedan',
            marca='toyota', modelo='Corolla', anio=2020, placa='1234ABC', color='Rojo',
        )
        self.orden = Orden.objects.create(
            cliente=self.cliente, vehiculo=self.vehiculo,
            descripcion='Reparación general', costo_estimado=1000,
        )

    def test_es_adelanto_por_defecto_false(self):
        pago = Pago.objects.create(orden=self.orden, monto=400, metodo='efectivo')
        self.assertFalse(pago.es_adelanto)

    def test_pago_ligado_a_orden(self):
        Pago.objects.create(orden=self.orden, monto=400, metodo='efectivo')
        self.assertEqual(self.orden.pagos.count(), 1)


class PagoFormTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Juan', apellido='Pérez', ci='12345678', telefono='70012345'
        )
        self.vehiculo = Vehiculo.objects.create(
            cliente=self.cliente, categoria='vehiculo', tipo_vehiculo='sedan',
            marca='toyota', modelo='Corolla', anio=2020, placa='1234ABC', color='Rojo',
        )
        self.orden = Orden.objects.create(
            cliente=self.cliente, vehiculo=self.vehiculo,
            descripcion='Reparación general', costo_estimado=1000,
        )

    def test_adelanto_no_supera_saldo(self):
        form = PagoForm(data={
            'orden': self.orden.pk, 'monto': 1500, 'metodo': 'efectivo',
            'tipo_pago': 'adelanto',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('monto', form.errors)

    def test_pago_final_igual_al_saldo(self):
        form = PagoForm(data={
            'orden': self.orden.pk, 'monto': 1000, 'metodo': 'efectivo',
            'tipo_pago': 'final',
        })
        self.assertTrue(form.is_valid())

    def test_pago_final_distinto_del_saldo_invalido(self):
        form = PagoForm(data={
            'orden': self.orden.pk, 'monto': 500, 'metodo': 'efectivo',
            'tipo_pago': 'final',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('monto', form.errors)


class PagosViewTest(TestCase):

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
        self.orden = Orden.objects.create(
            cliente=self.cliente, vehiculo=self.vehiculo,
            descripcion='Reparación general', costo_estimado=1000,
        )

    def test_pago_final_finaliza_orden(self):
        response = self.client.post('/pagos/nuevo/', {
            'orden': self.orden.pk, 'monto': 1000, 'metodo': 'efectivo',
            'tipo_pago': 'final',
        })
        self.assertEqual(response.status_code, 302)
        self.orden.refresh_from_db()
        self.assertEqual(self.orden.estado, 'finalizado')

    def test_eliminar_pago_solo_admin(self):
        pago = Pago.objects.create(orden=self.orden, monto=400, metodo='efectivo')
        tecnico = User.objects.create_user(username='tecnico', password='clave1234')
        self.client.logout()
        self.client.login(username='tecnico', password='clave1234')
        response = self.client.get(f'/pagos/eliminar/{pago.pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pago.objects.filter(pk=pago.pk).exists())

    def test_lista_pagos_muestra_total(self):
        Pago.objects.create(orden=self.orden, monto=Decimal('400.00'), metodo='efectivo')
        response = self.client.get('/pagos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_mes'], Decimal('400.00'))