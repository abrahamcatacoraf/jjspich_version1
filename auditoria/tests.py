from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase

from .models import Auditoria
from .utils import registrar


class AuditoriaModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='clave1234')

    def test_registrar_crea_auditoria(self):
        registrar(self.user, 'creacion', 'Cliente', 1, 'Se creó Cliente: Juan Pérez')
        self.assertEqual(Auditoria.objects.count(), 1)
        auditoria = Auditoria.objects.first()
        self.assertEqual(auditoria.accion, 'creacion')
        self.assertEqual(auditoria.modelo, 'Cliente')
        self.assertEqual(auditoria.usuario, self.user)

    def test_str_auditoria(self):
        auditoria = Auditoria.objects.create(
            usuario=self.user, accion='edicion', modelo='Vehiculo',
            objeto_id=5, detalle='Se editó la placa',
        )
        self.assertIn('Edición', str(auditoria))
        self.assertIn('Vehiculo #5', str(auditoria))


class AuditoriaViewTest(TestCase):

    def setUp(self):
        call_command('crear_grupos')
        self.admin = User.objects.create_user(username='admin', password='clave1234')
        self.admin.groups.add(Group.objects.get(name='Administrador'))

    def test_lista_auditoria_para_admin(self):
        self.client.login(username='admin', password='clave1234')
        registrar(self.admin, 'creacion', 'Cliente', 1, 'Se creó Cliente: Juan Pérez')
        response = self.client.get('/auditoria/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['registros'].count(), 1)

    def test_lista_auditoria_bloqueada_para_tecnico(self):
        tecnico = User.objects.create_user(username='tecnico', password='clave1234')
        tecnico.groups.add(Group.objects.get(name='Tecnico'))
        self.client.login(username='tecnico', password='clave1234')
        response = self.client.get('/auditoria/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/sin-permiso/')