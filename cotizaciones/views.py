from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.http import Http404
from taller_jjspich.decoradores import solo_admin
from auditoria.utils import registrar, generar_detalle_edicion
from .models import Cotizacion
from .forms import CotizacionForm
from .reportes import generar_pdf
from .telefono import normalizar_telefono, construir_mensaje
from django.urls import reverse
from urllib.parse import quote


PDF_TOKEN_SALT = 'cotizacion-pdf-publico'
PDF_TOKEN_MAX_AGE = 60 * 60 * 24 * 15  # 15 días


def generar_token_pdf(cotizacion):
    return signing.dumps(cotizacion.pk, salt=PDF_TOKEN_SALT, compress=True)


def enlace_publico_pdf(request, cotizacion):
    token = generar_token_pdf(cotizacion)
    return request.build_absolute_uri(
        reverse('pdf_cotizacion_publico', args=[token])
    )


def contexto_compartir(request, cotizacion):
    """Datos que usan las plantillas para el botón Compartir por WhatsApp."""
    telefono = normalizar_telefono(cotizacion.cliente_telefono)
    mensaje = construir_mensaje(
        cotizacion, enlace_publico_pdf(request, cotizacion))
    return {
        'telefono': telefono,
        'mensaje': mensaje,
        'pdf_url': reverse('pdf_cotizacion', args=[cotizacion.pk]),
        'wa_url': (f'https://wa.me/{telefono}?text={quote(mensaje)}'
                   if telefono else ''),
    }


@login_required
def lista_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'cotizaciones/lista.html', {
        'cotizaciones': cotizaciones,
    })


@login_required
def nueva_cotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.created_by = request.user
            cotizacion.save()
            registrar(request.user, 'creacion', 'Cotizacion', cotizacion.pk,
                      f"Se creó {cotizacion.numero} — {cotizacion.cliente_nombre}")
            messages.success(request, f'Cotización {cotizacion.numero} creada correctamente.')
            return redirect('detalle_cotizacion', pk=cotizacion.pk)
    else:
        form = CotizacionForm()
    return render(request, 'cotizaciones/form.html', {
        'form': form, 'titulo': 'Nueva Cotización',
    })


@login_required
def editar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        form = CotizacionForm(request.POST, instance=cotizacion)
        if form.is_valid():
            etiquetas = {
                'fecha': 'Fecha de emisión',
                'plazo': 'Plazo de validez',
                'tecnico': 'Técnico',
                'cliente_nombre': 'Cliente',
                'cliente_telefono': 'Teléfono del cliente',
                'vehiculo_marca': 'Marca',
                'vehiculo_modelo': 'Modelo',
                'vehiculo_placa': 'Placa',
                'vehiculo_color': 'Color',
                'vehiculo_anio': 'Año',
                'diagnostico': 'Diagnóstico técnico',
                'costo_estimado': 'Costo estimado',
                'notas': 'Notas adicionales',
            }
            cotizacion = form.save()
            detalle = generar_detalle_edicion(form, etiquetas)
            registrar(request.user, 'edicion', 'Cotizacion', cotizacion.pk,
                      f"Se editó {cotizacion.numero} — {cotizacion.cliente_nombre} — {detalle}")
            messages.success(
                request, f'Cotización {cotizacion.numero} actualizada correctamente.')
            return redirect('detalle_cotizacion', pk=cotizacion.pk)
    else:
        form = CotizacionForm(instance=cotizacion)
    return render(request, 'cotizaciones/form.html', {
        'form': form, 'titulo': f'Editar Cotización {cotizacion.numero}',
    })


@login_required
def detalle_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return render(request, 'cotizaciones/detalle.html', {
        'cotizacion': cotizacion,
        'whatsapp': contexto_compartir(request, cotizacion),
    })


@login_required
def pdf_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return generar_pdf(cotizacion)


@login_required
def pdf_cotizacion_inline(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return generar_pdf(cotizacion, disposicion='inline')


def pdf_cotizacion_publico(request, token):
    """PDF accesible por el cliente con un enlace firmado (caduca a los 15 días)."""
    try:
        pk = signing.loads(token, salt=PDF_TOKEN_SALT, max_age=PDF_TOKEN_MAX_AGE)
    except signing.BadSignature:
        raise Http404('Enlace de cotización inválido o expirado.')
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    response = generar_pdf(cotizacion, disposicion='inline')
    response['X-Robots-Tag'] = 'noindex'
    return response


@login_required
def preview_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return render(request, 'cotizaciones/preview.html', {
        'cotizacion': cotizacion,
        'whatsapp': contexto_compartir(request, cotizacion),
    })


@login_required
def ver_cotizacion_pdf(request, pk):
    return redirect('preview_cotizacion', pk=pk)


@login_required
@solo_admin
def eliminar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        registrar(request.user, 'eliminacion', 'Cotizacion', cotizacion.pk,
                  f"Se eliminó {cotizacion.numero} — {cotizacion.cliente_nombre}")
        cotizacion.delete()
        messages.success(request, 'Cotización eliminada correctamente.')
        return redirect('lista_cotizaciones')
    return render(request, 'cotizaciones/confirmar_eliminar.html', {
        'cotizacion': cotizacion,
    })
