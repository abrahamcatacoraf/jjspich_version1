import pyotp

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase

from .models import ClaveTOTP
from .views import MAX_INTENTOS


class LoginSeguroTest(TestCase):

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='juan', password='clave1234')

    def test_login_correcto_sin_2fa(self):
        response = self.client.post('/login/', {
            'username': 'juan', 'password': 'clave1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_login_con_2fa_redirige_a_verificacion(self):
        ClaveTOTP.objects.create(user=self.user, secreto=pyotp.random_base32(), activa=True)
        response = self.client.post('/login/', {
            'username': 'juan', 'password': 'clave1234',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/2fa/')

    def test_cuenta_se_bloquea_despues_de_intentos(self):
        for _ in range(MAX_INTENTOS):
            self.client.post('/login/', {'username': 'juan', 'password': 'incorrecta'})
        self.assertEqual(cache.get('intentos_juan', 0), MAX_INTENTOS)

        # Incluso con la contraseña correcta, la cuenta sigue bloqueada
        response = self.client.post('/login/', {
            'username': 'juan', 'password': 'clave1234',
        })
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(cache.get('intentos_juan', 0), MAX_INTENTOS)

    def test_login_correcto_limpia_intentos(self):
        self.client.post('/login/', {'username': 'juan', 'password': 'incorrecta'})
        self.assertEqual(cache.get('intentos_juan', 0), 1)
        self.client.post('/login/', {'username': 'juan', 'password': 'clave1234'})
        self.assertIsNone(cache.get('intentos_juan'))


class Verificar2FATest(TestCase):

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='juan', password='clave1234')
        self.totp = ClaveTOTP.objects.create(
            user=self.user, secreto=pyotp.random_base32(), activa=True
        )

    def test_codigo_incorrecto_muestra_error(self):
        session = self.client.session
        session['otp_user_pk'] = self.user.pk
        session.save()
        response = self.client.post('/login/2fa/', {'codigo': '000000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)

    def test_codigo_correcto_inicia_sesion(self):
        session = self.client.session
        session['otp_user_pk'] = self.user.pk
        session.save()
        codigo = pyotp.TOTP(self.totp.secreto).now()
        response = self.client.post('/login/2fa/', {'codigo': codigo})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_sin_sesion_redirige_a_login(self):
        response = self.client.get('/login/2fa/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')


class Configurar2FATest(TestCase):

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='juan', password='clave1234')
        self.client.login(username='juan', password='clave1234')

    def test_configurar_2fa_requiere_login(self):
        self.client.logout()
        response = self.client.get('/seguridad/configurar/')
        self.assertEqual(response.status_code, 302)

    def test_configurar_2fa_genera_qr_y_secreto(self):
        response = self.client.get('/seguridad/configurar/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('qr_data', response.context)
        self.assertIn('secreto', response.context)

    def test_desactivar_2fa(self):
        ClaveTOTP.objects.create(user=self.user, secreto=pyotp.random_base32(), activa=True)
        response = self.client.post('/seguridad/desactivar/')
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.totp.activa)