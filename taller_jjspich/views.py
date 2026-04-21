from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime
from clientes.models import Cliente
from vehiculos.models import Vehiculo
from ordenes.models import Orden
from inventario.models import Insumo
from pagos.models import Pago
from .reportes import reporte_ordenes, reporte_pagos, reporte_inventario

@login_required
def dashboard(request):
    mes_actual = datetime.datetime.now().month
    total_pagos_mes = Pago.objects.filter(
        fecha__month=mes_actual
    ).aggregate(total=Sum('monto'))['total'] or 0

    context = {
        'total_clientes':  Cliente.objects.count(),
        'total_vehiculos': Vehiculo.objects.count(),
        'total_ordenes':   Orden.objects.filter(
                               estado__in=['recibido', 'en_proceso']
                           ).count(),
        'total_insumos':   Insumo.objects.count(),
        'stock_bajo':      Insumo.objects.filter(cantidad__lte=5).count(),
        'total_pagos_mes': total_pagos_mes,
    }
    return render(request, 'base/dashboard.html', context)

@login_required
def vista_reportes(request):
    return render(request, 'base/reportes.html')

@login_required
def pdf_ordenes(request):
    ordenes = Orden.objects.all().select_related('cliente', 'vehiculo')
    return reporte_ordenes(ordenes)

@login_required
def pdf_pagos(request):
    mes_actual = datetime.datetime.now().month
    pagos = Pago.objects.filter(
        fecha__month=mes_actual
    ).select_related('orden', 'orden__cliente')
    total_mes = pagos.aggregate(total=Sum('monto'))['total'] or 0
    return reporte_pagos(pagos, total_mes)

@login_required
def pdf_inventario(request):
    insumos = Insumo.objects.all()
    return reporte_inventario(insumos)