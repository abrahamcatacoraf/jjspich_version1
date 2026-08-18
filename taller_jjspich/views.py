from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse
import datetime
from clientes.models import Cliente
from vehiculos.models import Vehiculo
from ordenes.models import Orden
from inventario.models import Insumo, MovimientoInsumo
from pagos.models import Pago
from .reportes import reporte_ordenes, reporte_pagos, reporte_inventario, reporte_movimientos_inventario, reporte_pagos_orden

MESES = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

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

def fecha_generacion():
    return datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

@login_required
def preview_ordenes(request):
    ordenes = Orden.objects.all().select_related('cliente', 'vehiculo')
    columnas = ['#', 'Cliente', 'Vehículo', 'Técnico', 'Estado', 'Costo (Bs.)', 'Fecha']
    filas = [
        [f'#{o.pk}', str(o.cliente), f'{o.vehiculo.marca} {o.vehiculo.modelo}',
         o.tecnico or '—', o.get_estado_display(), f'{o.costo_estimado}',
         o.fecha_ingreso.strftime('%d/%m/%Y')]
        for o in ordenes
    ]
    return render(request, 'base/preview_reporte.html', {
        'titulo': 'Reporte de Órdenes de Trabajo',
        'subtitulo': '',
        'fecha_generacion': fecha_generacion(),
        'columnas': columnas,
        'filas': filas,
        'resumen': [f'<b>Total de órdenes:</b> {ordenes.count()}'],
        'url_descargar': reverse('pdf_ordenes'),
        'url_volver': reverse('reportes'),
    })

@login_required
def preview_pagos(request):
    hoy = datetime.date.today()
    mes = request.GET.get('mes', str(hoy.month))
    anio = request.GET.get('anio', str(hoy.year))
    pagos = Pago.objects.filter(
        fecha__month=int(mes), fecha__year=int(anio)
    ).select_related('orden', 'orden__cliente')
    total_mes = pagos.aggregate(total=Sum('monto'))['total'] or 0
    columnas = ['Orden', 'Cliente', 'Monto (Bs.)', 'Método', 'Tipo', 'Fecha']
    filas = [
        [f'#{p.orden.pk}', str(p.orden.cliente), f'{p.monto}',
         p.get_metodo_display(), 'Adelanto' if p.es_adelanto else 'Pago final',
         p.fecha.strftime('%d/%m/%Y')]
        for p in pagos
    ]
    return render(request, 'base/preview_reporte.html', {
        'titulo': 'Reporte de Pagos',
        'subtitulo': f'Período: {MESES[int(mes)]} {anio}',
        'fecha_generacion': fecha_generacion(),
        'columnas': columnas,
        'filas': filas,
        'resumen': [f'<b>Total recaudado:</b> Bs. {total_mes}'],
        'url_descargar': f"{reverse('pdf_pagos')}?mes={mes}&anio={anio}",
        'url_volver': reverse('reportes'),
    })

@login_required
def preview_inventario(request):
    insumos = Insumo.objects.all()
    columnas = ['Insumo', 'Categoría', 'Stock', 'Unidad', 'Precio Unit. (Bs.)', 'Valor Total (Bs.)']
    filas = [
        [i.nombre, i.get_categoria_display(), str(i.cantidad), i.unidad,
         str(i.precio_unitario), str(i.valor_total)]
        for i in insumos
    ]
    return render(request, 'base/preview_reporte.html', {
        'titulo': 'Reporte de Inventario',
        'subtitulo': '',
        'fecha_generacion': fecha_generacion(),
        'columnas': columnas,
        'filas': filas,
        'resumen': [f'<b>Total de insumos registrados:</b> {insumos.count()}'],
        'url_descargar': reverse('pdf_inventario'),
        'url_volver': reverse('reportes'),
    })

@login_required
def preview_movimientos_inventario(request):
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
    columnas = ['Fecha', 'Tipo', 'Precio Unit.', 'Stock Inicial', 'Ingresó', 'Salió', 'Stock Final']
    filas = [
        [m.fecha.strftime('%d/%m/%Y %H:%M'),
         'Ingreso' if m.tipo == 'entrada' else 'Salida',
         f'Bs. {m.precio_unitario:.2f}',
         str(m.cantidad_inicial),
         str(m.cantidad_movimiento) if m.tipo == 'entrada' else '—',
         str(m.cantidad_movimiento) if m.tipo == 'salida' else '—',
         str(m.cantidad_actual)]
        for m in movimientos
    ]
    total_entradas = sum(m.cantidad_movimiento for m in movimientos if m.tipo == 'entrada')
    total_salidas = sum(m.cantidad_movimiento for m in movimientos if m.tipo == 'salida')
    params = f"mes={mes}&anio={anio}"
    if insumo_id:
        params = f"insumo={insumo_id}&{params}"
    return render(request, 'base/preview_reporte.html', {
        'titulo': f'Movimientos de Inventario — {nombre}',
        'subtitulo': f'{MESES[int(mes)]} {anio}',
        'fecha_generacion': fecha_generacion(),
        'columnas': columnas,
        'filas': filas,
        'resumen': [f'<b>Total ingresos:</b> {total_entradas} | <b>Total salidas:</b> {total_salidas} | <b>Movimientos:</b> {movimientos.count()}'],
        'url_descargar': f"{reverse('pdf_movimientos_inventario')}?{params}",
        'url_volver': reverse('reportes'),
    })

@login_required
def preview_pagos_orden(request):
    orden_id = request.GET.get('orden')
    if not orden_id:
        messages.error(request, 'Seleccione una opción para continuar')
        return redirect('reportes')
    try:
        orden = Orden.objects.get(pk=orden_id)
    except (Orden.DoesNotExist, ValueError, TypeError):
        messages.error(request, 'Seleccione una orden válida para continuar')
        return redirect('reportes')
    pagos = Pago.objects.filter(orden=orden).select_related('orden', 'orden__cliente')
    total = pagos.aggregate(total=Sum('monto'))['total'] or 0
    columnas = ['Monto (Bs.)', 'Método', 'Tipo', 'Fecha', 'Observación']
    filas = [
        [f'{p.monto:.2f}', p.get_metodo_display(),
         'Adelanto' if p.es_adelanto else 'Pago final',
         p.fecha.strftime('%d/%m/%Y %H:%M'), p.observacion or '—']
        for p in pagos
    ]
    return render(request, 'base/preview_reporte.html', {
        'titulo': f'Pagos — Orden #{orden.pk}',
        'subtitulo': f'Cliente: {orden.cliente} — Vehículo: {orden.vehiculo}',
        'fecha_generacion': fecha_generacion(),
        'columnas': columnas,
        'filas': filas,
        'resumen': [
            f'<b>Costo estimado:</b> Bs. {orden.costo_estimado:.2f} | <b>Saldo pendiente:</b> Bs. {orden.costo_estimado - total:.2f}',
            f'<b>Total pagado:</b> Bs. {total:.2f}',
        ],
        'url_descargar': f"{reverse('pdf_pagos_orden')}?orden={orden.pk}",
        'url_volver': reverse('reportes'),
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


def manifest_web(request):
    contenido = render(request, 'pwa/manifest.json').content
    return HttpResponse(contenido, content_type='application/manifest+json')


def service_worker(request):
    contenido = render(request, 'pwa/sw.js').content
    return HttpResponse(contenido, content_type='application/javascript')