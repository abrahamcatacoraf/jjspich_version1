import io
import base64

import pyotp
import qrcode

from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import ClaveTOTP

MAX_INTENTOS = 5
TIEMPO_BLOQUEO = 900  # 15 minutos


def _clave_intentos(username):
    return f'intentos_{username}'


def _cuenta_bloqueada(username):
    return cache.get(_clave_intentos(username), 0) >= MAX_INTENTOS


def _registrar_fallo(username):
    actual = cache.get(_clave_intentos(username), 0)
    cache.set(_clave_intentos(username), actual + 1, TIEMPO_BLOQUEO)


def _limpiar_intentos(username):
    cache.delete(_clave_intentos(username))


def LoginViewSeguro(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username', '')
        if _cuenta_bloqueada(username):
            messages.error(
                request,
                'Cuenta bloqueada temporalmente por demasiados intentos fallidos. '
                'Intente nuevamente en unos minutos.'
            )
        elif form.is_valid():
            user = form.get_user()
            _limpiar_intentos(username)
            totp = getattr(user, 'totp', None)
            if totp and totp.activa:
                request.session['otp_user_pk'] = user.pk
                return redirect('verificar_2fa')
            login(request, user)
            return redirect('/')
        elif username:
            _registrar_fallo(username)
    else:
        form = AuthenticationForm(request)
    return render(request, 'registration/login.html', {'form': form})


def verificar_2fa(request):
    user_pk = request.session.get('otp_user_pk')
    if not user_pk:
        return redirect('login')
    try:
        user = User.objects.get(pk=user_pk)
        totp = user.totp
    except (User.DoesNotExist, ClaveTOTP.DoesNotExist):
        request.session.pop('otp_user_pk', None)
        return redirect('login')
    error = None
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        if pyotp.TOTP(totp.secreto).verify(codigo):
            request.session.pop('otp_user_pk', None)
            login(request, user)
            return redirect('/')
        error = 'El código es incorrecto o ha expirado.'
    return render(request, 'seguridad/verificar.html',
                  {'error': error, 'usuario': user.username})


@login_required
def configurar_2fa(request):
    totp, _ = ClaveTOTP.objects.get_or_create(user=request.user)
    if not totp.secreto:
        totp.secreto = pyotp.random_base32()
        totp.save()
    uri = pyotp.TOTP(totp.secreto).provisioning_uri(
        name=request.user.username, issuer_name='JJ SPICH')
    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_data = base64.b64encode(buffer.getvalue()).decode()
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        if pyotp.TOTP(totp.secreto).verify(codigo):
            totp.activa = True
            totp.save()
            messages.success(
                request, 'Autenticación de doble factor activada correctamente.')
            return redirect('configurar_2fa')
        messages.error(
            request, 'El código es incorrecto. No se activó la doble verificación.')
    return render(request, 'seguridad/configurar.html', {
        'qr_data': qr_data,
        'secreto': totp.secreto,
        'activa': totp.activa,
    })


@login_required
@require_POST
def desactivar_2fa(request):
    totp = get_object_or_404(ClaveTOTP, user=request.user)
    totp.activa = False
    totp.save()
    messages.success(request, 'Autenticación de doble factor desactivada.')
    return redirect('configurar_2fa')