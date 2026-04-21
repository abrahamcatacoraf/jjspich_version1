from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.http import HttpResponse
import datetime


def get_response_pdf(nombre_archivo):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return response


def encabezado_taller(elementos, styles, titulo, subtitulo=''):
    titulo_style = ParagraphStyle(
        'titulo', parent=styles['Title'],
        fontSize=18, textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=4
    )
    sub_style = ParagraphStyle(
        'subtitulo', parent=styles['Normal'],
        fontSize=11, textColor=colors.grey,
        spaceAfter=4, alignment=TA_CENTER
    )
    fecha_style = ParagraphStyle(
        'fecha', parent=styles['Normal'],
        fontSize=9, textColor=colors.grey,
        spaceAfter=16, alignment=TA_CENTER
    )
    elementos.append(Paragraph("Taller de Chapa y Pintura JJ SPICH", titulo_style))
    elementos.append(Paragraph(titulo, sub_style))
    if subtitulo:
        elementos.append(Paragraph(subtitulo, sub_style))
    elementos.append(Paragraph(
        f"Generado el {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
        fecha_style
    ))
    elementos.append(Spacer(1, 0.2 * inch))


def reporte_ordenes(ordenes):
    response = get_response_pdf('ordenes_trabajo.pdf')
    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elementos = []

    encabezado_taller(elementos, styles, 'Reporte de Órdenes de Trabajo')

    # Tabla
    datos = [['#', 'Cliente', 'Vehículo', 'Técnico', 'Estado', 'Costo (Bs.)', 'Fecha']]
    for o in ordenes:
        datos.append([
            f'#{o.pk}',
            str(o.cliente),
            f'{o.vehiculo.marca} {o.vehiculo.modelo}',
            o.tecnico or '—',
            o.get_estado_display(),
            f'{o.costo_estimado}',
            o.fecha_ingreso.strftime('%d/%m/%Y'),
        ])

    tabla = Table(datos, colWidths=[35, 100, 100, 80, 70, 70, 65])
    tabla.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR',   (0, 0), (-1, 0), colors.white),
        ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, 0), 9),
        ('ALIGN',       (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE',    (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID',        (0, 0), (-1, -1), 0.3, colors.HexColor('#dee2e6')),
        ('ROWHEIGHT',   (0, 0), (-1, -1), 20),
        ('TOPPADDING',  (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)

    # Total
    elementos.append(Spacer(1, 0.2 * inch))
    total_style = ParagraphStyle('total', parent=styles['Normal'],
                                  fontSize=10, alignment=TA_LEFT)
    elementos.append(Paragraph(f"<b>Total de órdenes: {ordenes.count()}</b>", total_style))

    doc.build(elementos)
    return response


def reporte_pagos(pagos, total_mes):
    response = get_response_pdf('reporte_pagos.pdf')
    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elementos = []

    mes = datetime.datetime.now().strftime('%B %Y')
    encabezado_taller(elementos, styles,
                      'Reporte de Pagos',
                      f'Período: {mes}')

    datos = [['Orden', 'Cliente', 'Monto (Bs.)', 'Método', 'Tipo', 'Fecha']]
    for p in pagos:
        datos.append([
            f'#{p.orden.pk}',
            str(p.orden.cliente),
            f'{p.monto}',
            p.get_metodo_display(),
            'Adelanto' if p.es_adelanto else 'Pago final',
            p.fecha.strftime('%d/%m/%Y'),
        ])

    tabla = Table(datos, colWidths=[45, 130, 80, 80, 80, 70])
    tabla.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR',   (0, 0), (-1, 0), colors.white),
        ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, 0), 9),
        ('ALIGN',       (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE',    (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID',        (0, 0), (-1, -1), 0.3, colors.HexColor('#dee2e6')),
        ('ROWHEIGHT',   (0, 0), (-1, -1), 20),
        ('TOPPADDING',  (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)

    elementos.append(Spacer(1, 0.3 * inch))
    total_style = ParagraphStyle('total', parent=styles['Normal'],
                                  fontSize=11, alignment=TA_LEFT)
    elementos.append(Paragraph(
        f"<b>Total recaudado: Bs. {total_mes}</b>",
        total_style
    ))

    doc.build(elementos)
    return response


def reporte_inventario(insumos):
    response = get_response_pdf('inventario.pdf')
    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elementos = []

    encabezado_taller(elementos, styles, 'Reporte de Inventario')

    datos = [['Insumo', 'Categoría', 'Stock', 'Unidad', 'Precio Unit. (Bs.)', 'Valor Total (Bs.)']]
    for i in insumos:
        fila = [
            i.nombre,
            i.get_categoria_display(),
            str(i.cantidad),
            i.unidad,
            str(i.precio_unitario),
            str(i.valor_total),
        ]
        datos.append(fila)

    tabla = Table(datos, colWidths=[120, 80, 55, 55, 90, 90])
    tabla.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR',   (0, 0), (-1, 0), colors.white),
        ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, 0), 9),
        ('ALIGN',       (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE',    (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID',        (0, 0), (-1, -1), 0.3, colors.HexColor('#dee2e6')),
        ('ROWHEIGHT',   (0, 0), (-1, -1), 20),
        ('TOPPADDING',  (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)

    elementos.append(Spacer(1, 0.2 * inch))
    total_style = ParagraphStyle('total', parent=styles['Normal'],
                                  fontSize=10, alignment=TA_LEFT)
    elementos.append(Paragraph(
        f"<b>Total de insumos registrados: {insumos.count()}</b>",
        total_style
    ))

    doc.build(elementos)
    return response