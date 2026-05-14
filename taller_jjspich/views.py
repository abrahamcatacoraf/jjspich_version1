from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime
from clientes.models import Cliente
from vehiculos.models import Vehiculo
from ordenes.models import Orden
from inventario.models import Insumo, MovimientoInsumo
from pagos.models import Pago
from .reportes import reporte_ordenes, reporte_pagos, reporte_inventario, reporte_movimientos_inventario, reporte_pagos_orden

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
        'ultimas_ordenes': Orden.objects.all().order_by('-fecha_ingreso')[:5],
        'insumos_criticos': Insumo.objects.filter(
                                cantidad__lte=5
                            ).order_by('cantidad')[:5],
    }
    return render(request, 'base/dashboard.html', context)

@login_required
def vista_reportes(request):
    return render(request, 'base/reportes.html', {
        'insumos': Insumo.objects.all().order_by('nombre'),
        'ordenes': Orden.objects.all().select_related('cliente', 'vehiculo').order_by('-fecha_ingreso')[:100],
    })

@login_required
def pdf_ordenes(request):
    ordenes = Orden.objects.all().select_related('cliente', 'vehiculo')
    return reporte_ordenes(ordenes)

@login_required
def pdf_pagos(request):
    hoy = datetime.date.today()
    mes = request.GET.get('mes', str(hoy.month))
    anio = request.GET.get('anio', str(hoy.year))
    pagos = Pago.objects.filter(
        fecha__month=int(mes), fecha__year=int(anio)
    ).select_related('orden', 'orden__cliente')
    total_mes = pagos.aggregate(total=Sum('monto'))['total'] or 0
    return reporte_pagos(pagos, total_mes, int(mes), int(anio))

@login_required
def pdf_inventario(request):
    insumos = Insumo.objects.all()
    return reporte_inventario(insumos)

@login_required
def pdf_movimientos_inventario(request):
    insumo_id = request.GET.get('insumo')
    hoy = datetime.date.today()
    mes = request.GET.get('mes', str(hoy.month))
    anio = request.GET.get('anio', str(hoy.year))
    if insumo_id:
        movimientos = MovimientoInsumo.objects.filter(
            insumo_id=insumo_id,
            fecha__month=int(mes),
            fecha__year=int(anio),
        ).select_related('insumo')
        insumo = Insumo.objects.get(pk=insumo_id)
        nombre = str(insumo)
    else:
        movimientos = MovimientoInsumo.objects.filter(
            fecha__month=int(mes),
            fecha__year=int(anio),
        ).select_related('insumo')
        nombre = 'Todos los insumos'
    return reporte_movimientos_inventario(movimientos, nombre, mes, anio)

@login_required
def pdf_pagos_orden(request):
    orden_id = request.GET.get('orden')
    orden = get_object_or_404(Orden, pk=orden_id)
    pagos = Pago.objects.filter(orden=orden).select_related('orden', 'orden__cliente')
    total = pagos.aggregate(total=Sum('monto'))['total'] or 0
    return reporte_pagos_orden(pagos, total, orden)