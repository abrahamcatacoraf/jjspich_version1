from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taller_jjspich.decoradores import solo_admin
from auditoria.utils import registrar, generar_detalle_edicion
from .models import Cotizacion
from .forms import CotizacionForm
from .reportes import generar_pdf
from django.urls import reverse


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
    })


@login_required
def pdf_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return generar_pdf(cotizacion)


@login_required
def pdf_cotizacion_inline(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return generar_pdf(cotizacion, disposicion='inline')


@login_required
def preview_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    return render(request, 'cotizaciones/preview.html', {
        'cotizacion': cotizacion,
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
