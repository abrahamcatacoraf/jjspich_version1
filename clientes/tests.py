from django.db import IntegrityError, transaction
from django.test import TestCase

from .forms import ClienteForm
from .models import Cliente


class ClienteModelTest(TestCase):

    def test_crear_cliente_valido(self):
        cliente = Cliente.objects.create(
            nombre='Juan',
            apellido='Pérez',
            ci='12345678',
            telefono='70012345',
            correo='juan@example.com',
            direccion='Calle 1 N° 100',
        )
        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(str(cliente), 'Juan Pérez')
        self.assertEqual(cliente.ci, '12345678')

    def test_ci_duplicado_rechazado(self):
        Cliente.objects.create(
            nombre='Juan', apellido='Pérez', ci='12345678', telefono='70012345'
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Cliente.objects.create(
                    nombre='María', apellido='Gómez', ci='12345678', telefono='70056789'
                )


class ClienteFormTest(TestCase):

    def test_formulario_valido(self):
        form = ClienteForm(data={
            'nombre': 'Ana', 'apellido': 'López', 'ci': '87654321',
            'telefono': '70111111', 'correo': 'ana@example.com', 'direccion': 'Av. Principal',
        })
        self.assertTrue(form.is_valid())

    def test_formulario_sin_ci_invalido(self):
        form = ClienteForm(data={
            'nombre': 'Ana', 'apellido': 'López', 'ci': '',
            'telefono': '70111111',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('ci', form.errors)