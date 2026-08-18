from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from taller_jjspich.decoradores import solo_admin
from auditoria.utils import registrar
from .models import Pago
from .forms import PagoForm
from ordenes.models import Orden

@login_required
def lista_pagos(request):
    pagos = Pago.objects.all().select_related('orden', 'orden__cliente')
    total_mes = Pago.objects.filter(
        fecha__month=__import__('datetime').datetime.now().month
    ).aggregate(total=Sum('monto'))['total'] or 0
    return render(request, 'pagos/lista.html', {
        'pagos':     pagos,
        'total_mes': total_mes,
    })

def ordenes_info_context(queryset):
    ordenes = queryset.annotate(
        total_pagado=Coalesce(
            Sum('pagos__monto'), 0,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )
    return [
        {
            'id': o.pk,
            'label': f'#{o.pk} — {o.cliente}',
            'saldo': float(o.costo_estimado - o.total_pagado),
        }
        for o in ordenes
    ]


@login_required
def nuevo_pago(request):
    orden_fija = request.GET.get('orden') or request.POST.get('orden')
    if orden_fija:
        try:
            orden = Orden.objects.get(pk=orden_fija)
        except (Orden.DoesNotExist, ValueError, TypeError):
            orden = None
        if orden is None or orden.estado == 'finalizado':
            orden_fija = None
    if request.method == 'POST':
        form = PagoForm(request.POST, orden_fija=orden_fija)
        if form.is_valid():
            pago = form.save()
            orden = pago.orden
            total_pagado = orden.pagos.aggregate(total=Sum('monto'))['total'] or 0
            saldo = orden.costo_estimado - total_pagado
            if pago.es_adelanto:
                if saldo <= 0:
                    Orden.objects.filter(pk=orden.pk).update(estado='finalizado')
                elif orden.estado in ('recibido', 'en_proceso'):
                    Orden.objects.filter(pk=orden.pk).update(estado='en_proceso')
            else:
                Orden.objects.filter(pk=orden.pk).update(estado='finalizado')
            registrar(request.user, 'creacion', 'Pago', pago.pk, f"Se registró Pago de Bs.{pago.monto} — Orden #{pago.orden.pk}")
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('lista_pagos')
    else:
        form = PagoForm(orden_fija=orden_fija)
    return render(request, 'pagos/form.html', {
        'form': form, 'titulo': 'Registrar Pago',
        'orden_fija': orden_fija,
        'ordenes_info': ordenes_info_context(form.fields['orden'].queryset),
    })

@login_required
def detalle_orden_pagos(request, orden_pk):
    orden  = get_object_or_404(Orden, pk=orden_pk)
    pagos  = Pago.objects.filter(orden=orden)
    total_pagado   = pagos.aggregate(total=Sum('monto'))['total'] or 0
    saldo_pendiente = orden.costo_estimado - total_pagado
    return render(request, 'pagos/detalle_orden.html', {
        'orden':           orden,
        'pagos':           pagos,
        'total_pagado':    total_pagado,
        'saldo_pendiente': saldo_pendiente,
    })

@login_required
@solo_admin
def eliminar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        registrar(request.user, 'eliminacion', 'Pago', pago.pk, f"Se eliminó Pago de Bs.{pago.monto} — Orden #{pago.orden.pk}")
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente.')
        return redirect('lista_pagos')
    return render(request, 'pagos/confirmar_eliminar.html', {'pago': pago})