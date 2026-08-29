from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Insumo, MovimientoInsumo


class InsumoModelTest(TestCase):

    def setUp(self):
        self.insumo = Insumo.objects.create(
            nombre='Pintura azul', categoria='pintura', cantidad=10,
            unidad='litro', precio_unitario=50, stock_minimo=5,
        )

    def test_stock_bajo(self):
        self.assertFalse(self.insumo.stock_bajo)
        self.insumo.cantidad = 3
        self.assertTrue(self.insumo.stock_bajo)

    def test_valor_total(self):
        self.assertEqual(self.insumo.valor_total, Decimal('500.00'))

    def test_str_insumo(self):
        self.assertIn('Pintura azul', str(self.insumo))
        self.assertIn('10 litro', str(self.insumo))


class InventarioViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='clave1234')
        self.client.login(username='admin', password='clave1234')
        self.insumo = Insumo.objects.create(
            nombre='Lija N° 80', categoria='lija', cantidad=20,
            unidad='unidad', precio_unitario=2, stock_minimo=10,
        )

    def test_ajustar_stock_entrada(self):
        response = self.client.post(f'/inventario/ajustar/{self.insumo.pk}/', {
            'tipo': 'entrada', 'cantidad': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.cantidad, 25)
        self.assertEqual(self.insumo.movimientos.count(), 1)
        movimiento = self.insumo.movimientos.first()
        self.assertEqual(movimiento.tipo, 'entrada')
        self.assertEqual(movimiento.cantidad_actual, 25)

    def test_ajustar_stock_salida(self):
        response = self.client.post(f'/inventario/ajustar/{self.insumo.pk}/', {
            'tipo': 'salida', 'cantidad': 8,
        })
        self.assertEqual(response.status_code, 302)
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.cantidad, 12)
        self.assertEqual(self.insumo.movimientos.count(), 1)
        self.assertEqual(self.insumo.movimientos.first().tipo, 'salida')

    def test_ajustar_stock_salida_excede_stock(self):
        response = self.client.post(f'/inventario/ajustar/{self.insumo.pk}/', {
            'tipo': 'salida', 'cantidad': 999,
        })
        self.assertEqual(response.status_code, 302)
        self.insumo.refresh_from_db()
        self.assertEqual(self.insumo.cantidad, 20)
        self.assertEqual(self.insumo.movimientos.count(), 0)

    def test_movimientos_insumo_solo_admin(self):
        MovimientoInsumo.objects.create(
            insumo=self.insumo, tipo='entrada', precio_unitario=2,
            cantidad_inicial=20, cantidad_movimiento=5, cantidad_actual=25,
        )
        tecnico = User.objects.create_user(username='tecnico', password='clave1234')
        self.client.logout()
        self.client.login(username='tecnico', password='clave1234')
        response = self.client.get(f'/inventario/movimientos/{self.insumo.pk}/')
        self.assertEqual(response.status_code, 302)