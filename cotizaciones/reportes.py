from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                 Paragraph, Spacer, Image, HRFlowable)
from reportlab.lib.utils import ImageReader
from reportlab.graphics.shapes import Drawing, Rect, Image as RlImage
from django.http import HttpResponse
from django.conf import settings
import datetime
import os


def generar_pdf(cotizacion, disposicion='attachment'):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'{disposicion}; filename="cotizacion_{cotizacion.numero}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=45, leftMargin=45,
                            topMargin=40, bottomMargin=36)

    styles = getSampleStyleSheet()
    ancho = letter[0] - 90

    elementos = []

    # ── Estilos personalizados ──
    estilo_taller = ParagraphStyle(
        'taller', parent=styles['Normal'],
        fontSize=22, textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=4, alignment=TA_CENTER,
        leading=26,
    )
    estilo_subtaller = ParagraphStyle(
        'subtaller', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#666666'),
        spaceAfter=6, alignment=TA_CENTER,
    )
    estilo_cotizacion = ParagraphStyle(
        'cotitulo', parent=styles['Normal'],
        fontSize=16, textColor=colors.HexColor('#e67e22'),
        spaceBefore=0, spaceAfter=0, alignment=TA_CENTER,
    )
    estilo_seccion = ParagraphStyle(
        'seccion', parent=styles['Normal'],
        fontSize=10, textColor=colors.white,
        spaceAfter=4, alignment=TA_LEFT,
    )
    estilo_label = ParagraphStyle(
        'label', parent=styles['Normal'],
        fontSize=8, textColor=colors.HexColor('#888888'),
        spaceAfter=1,
    )
    estilo_valor = ParagraphStyle(
        'valor', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=4,
    )
    estilo_diagnostico = ParagraphStyle(
        'diagnostico', parent=styles['Normal'],
        fontSize=9, textColor=colors.HexColor('#333333'),
        leading=14, alignment=TA_LEFT,
    )
    estilo_costo_label = ParagraphStyle(
        'costo_label', parent=styles['Normal'],
        fontSize=11, textColor=colors.HexColor('#555555'),
        alignment=TA_RIGHT,
    )
    estilo_costo_monto = ParagraphStyle(
        'costo_monto', parent=styles['Normal'],
        fontSize=20, textColor=colors.HexColor('#1a1a2e'),
        alignment=TA_RIGHT, spaceAfter=2,
    )
    estilo_footer = ParagraphStyle(
        'footer', parent=styles['Normal'],
        fontSize=7, textColor=colors.HexColor('#aaaaaa'),
        alignment=TA_CENTER,
    )

    # ── Header con logo (fondo negro redondeado + borde degradado) ──
    logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'logo_jjspich.png')
    if os.path.exists(logo_path):
        logo_ancho = 1.0 * inch
        logo_alto = 1.0 * inch
        pad = 4
        borde = 4
        radius = 10
        total_w = logo_ancho + pad * 2 + borde * 2
        total_h = logo_alto + pad * 2 + borde * 2

        d = Drawing(total_w, total_h)
        d.hAlign = 'CENTER'

        # Degradado naranja → negro (capas concéntricas, de afuera hacia adentro)
        naranja = (230/255, 126/255, 34/255)
        negro = (0, 0, 0)
        capas = 10
        for i in range(capas):
            t = i / (capas - 1)
            r_color = naranja[0] + (negro[0] - naranja[0]) * t
            g_color = naranja[1] + (negro[1] - naranja[1]) * t
            b_color = naranja[2] + (negro[2] - naranja[2]) * t
            ins = (capas - 1 - i) * 0.5
            r = max(radius - ins * 0.3, 3)
            rect = Rect(
                borde + ins, borde + ins,
                total_w - (borde + ins) * 2,
                total_h - (borde + ins) * 2,
                rx=r, ry=r
            )
            rect.fillColor = None
            rect.strokeColor = colors.HexColor(
                '#%02x%02x%02x' % tuple(int(c * 255) for c in (r_color, g_color, b_color))
            )
            rect.strokeWidth = 1.0
            d.add(rect)

        # Fondo negro redondeado
        bg = Rect(borde, borde, total_w - borde * 2, total_h - borde * 2, rx=radius, ry=radius)
        bg.fillColor = colors.HexColor('#000000')
        bg.strokeColor = None
        d.add(bg)

        # Logo centrado
        img = RlImage(borde + pad, borde + pad, logo_ancho, logo_alto, logo_path)
        d.add(img)

        elementos.append(d)
        elementos.append(Spacer(1, 2))

    elementos.append(Paragraph("Taller de Chapa y Pintura", estilo_taller))
    elementos.append(Paragraph("JJ SPICH", estilo_taller))
    elementos.append(Paragraph("Mecánica General · Chapa y Pintura · Servicio Especializado",
                               estilo_subtaller))
    elementos.append(Spacer(1, 4))

    # Línea decorativa + título de cotización
    elementos.append(HRFlowable(width="100%", thickness=2,
                                 color=colors.HexColor('#e67e22'),
                                 spaceAfter=0))
    elementos.append(Spacer(1, 6))
    elementos.append(Paragraph(f"COTIZACIÓN {cotizacion.numero}", estilo_cotizacion))
    elementos.append(Spacer(1, 6))
    elementos.append(HRFlowable(width="100%", thickness=2,
                                 color=colors.HexColor('#e67e22'),
                                 spaceAfter=0))
    elementos.append(Spacer(1, 10))

    # ── Fecha y plazo ──
    fecha_data = [
        [Paragraph(f'<b>Fecha de emisión:</b>  {cotizacion.fecha.strftime("%d/%m/%Y")}', estilo_valor),
         Paragraph(f'<b>Plazo de validez:</b>  {cotizacion.plazo}', estilo_valor)],
    ]
    fecha_tabla = Table(fecha_data, colWidths=[ancho * 0.5, ancho * 0.5])
    fecha_tabla.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elementos.append(fecha_tabla)
    elementos.append(Spacer(1, 4))

    # ── Técnico ──
    tec_data = [
        [Paragraph(f'<b>Técnico:</b>  {cotizacion.tecnico}', estilo_valor)],
    ]
    tec_tabla = Table(tec_data, colWidths=[ancho])
    elementos.append(tec_tabla)
    elementos.append(Spacer(1, 6))

    # ── Sección: Datos del Cliente ──
    encabezado_cliente = [[Paragraph('DATOS DEL CLIENTE Y VEHÍCULO', estilo_seccion)]]
    tbl_enc_cliente = Table(encabezado_cliente, colWidths=[ancho])
    tbl_enc_cliente.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tbl_enc_cliente)

    datos_cliente = [
        [Paragraph('<b>Cliente</b>', estilo_label),
         Paragraph('<b>Vehículo</b>', estilo_label),
         Paragraph('<b>Placa</b>', estilo_label)],
        [Paragraph(cotizacion.cliente_nombre, estilo_valor),
         Paragraph(f'{cotizacion.vehiculo_marca} {cotizacion.vehiculo_modelo}', estilo_valor),
         Paragraph(cotizacion.vehiculo_placa, estilo_valor)],
        [Paragraph('<b>Color</b>', estilo_label),
         Paragraph('<b>Modelo</b>', estilo_label),
         Paragraph('<b>Año</b>', estilo_label)],
        [Paragraph(cotizacion.vehiculo_color, estilo_valor),
         Paragraph(cotizacion.vehiculo_modelo, estilo_valor),
         Paragraph(str(cotizacion.vehiculo_anio), estilo_valor)],
    ]
    tbl_cliente = Table(datos_cliente, colWidths=[ancho * 0.33, ancho * 0.34, ancho * 0.33])
    tbl_cliente.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f8f9fa')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tbl_cliente)
    elementos.append(Spacer(1, 8))

    # ── Sección: Diagnóstico ──
    encabezado_diag = [[Paragraph('DIAGNÓSTICO TÉCNICO', estilo_seccion)]]
    tbl_enc_diag = Table(encabezado_diag, colWidths=[ancho])
    tbl_enc_diag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tbl_enc_diag)

    diag_cell = [[Paragraph(cotizacion.diagnostico.replace('\n', '<br/>'), estilo_diagnostico)]]
    tbl_diag = Table(diag_cell, colWidths=[ancho])
    tbl_diag.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fafafa')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elementos.append(tbl_diag)
    elementos.append(Spacer(1, 8))

    # ── Costo estimado ──
    encabezado_costo = [[Paragraph('COSTO ESTIMADO', estilo_seccion)]]
    tbl_enc_costo = Table(encabezado_costo, colWidths=[ancho])
    tbl_enc_costo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tbl_enc_costo)

    monto_formateado = f'Bs. {cotizacion.costo_estimado:,.2f}'
    costo_data = [
        [Paragraph('Total estimado de reparación:', estilo_costo_label),
         Paragraph(monto_formateado, estilo_costo_monto)],
    ]
    tbl_costo = Table(costo_data, colWidths=[ancho * 0.35, ancho * 0.65])
    tbl_costo.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e67e22')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elementos.append(tbl_costo)

    if cotizacion.notas:
        elementos.append(Spacer(1, 6))
        notas_style = ParagraphStyle(
            'notas', parent=styles['Normal'],
            fontSize=8, textColor=colors.HexColor('#666666'),
            alignment=TA_LEFT, leading=12,
        )
        elementos.append(Paragraph(f'<b>Notas:</b>  {cotizacion.notas.replace(chr(10), "<br/>")}', notas_style))

    elementos.append(Spacer(1, 12))

    # ── Línea de firmas ──
    elementos.append(HRFlowable(width="100%", thickness=1,
                                 color=colors.HexColor('#cccccc'),
                                 spaceAfter=0))
    elementos.append(Spacer(1, 12))

    firma_data = [
        [Paragraph('____________________________', ParagraphStyle('f1', parent=styles['Normal'],
                    fontSize=9, alignment=TA_CENTER)),
         Paragraph('____________________________', ParagraphStyle('f2', parent=styles['Normal'],
                    fontSize=9, alignment=TA_CENTER))],
        [Paragraph('Firma del Técnico', ParagraphStyle('f1l', parent=styles['Normal'],
                    fontSize=8, textColor=colors.HexColor('#888888'), alignment=TA_CENTER)),
         Paragraph('Firma del Cliente', ParagraphStyle('f2l', parent=styles['Normal'],
                    fontSize=8, textColor=colors.HexColor('#888888'), alignment=TA_CENTER))],
    ]
    tbl_firma = Table(firma_data, colWidths=[ancho * 0.5, ancho * 0.5])
    tbl_firma.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tbl_firma)

    # ── Footer ──
    elementos.append(Spacer(1, 12))
    elementos.append(HRFlowable(width="100%", thickness=0.5,
                                 color=colors.HexColor('#dddddd'),
                                 spaceAfter=4))
    elementos.append(Paragraph(
        f"JJ SPICH — Taller de Chapa y Pintura  |  "
        f"Generado el {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}  |  "
        f"Documento sin valor fiscal",
        estilo_footer))

    doc.build(elementos)
    return response
