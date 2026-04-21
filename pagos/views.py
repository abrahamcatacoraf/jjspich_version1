from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
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

@login_required
def nuevo_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('lista_pagos')
    else:
        form = PagoForm()
    return render(request, 'pagos/form.html', {
        'form': form, 'titulo': 'Registrar Pago'
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
def eliminar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente.')
        return redirect('lista_pagos')
    return render(request, 'pagos/confirmar_eliminar.html', {'pago': pago})