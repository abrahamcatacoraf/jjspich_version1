# -*- coding: utf-8 -*-
import re


def normalizar_telefono(telefono):
    """Devuelve el número en formato internacional para WhatsApp (Bolivia).

    Ejemplos:
        72543915     -> 59172543915
        +591 72543915 -> 59172543915
        (sin número) -> ''
    """
    if not telefono:
        return ''
    digitos = re.sub(r'\D', '', str(telefono))
    if not digitos:
        return ''
    # Ya incluye el código de país de Bolivia
    if digitos.startswith('591') and len(digitos) >= 11:
        return digitos
    # Quita ceros iniciales de marcado local (ej. 072543915)
    digitos = digitos.lstrip('0')
    if len(digitos) == 8:
        return f'591{digitos}'
    return digitos


def construir_mensaje(cotizacion, enlace_publico):
    """Texto que se envía por WhatsApp con el resumen de la cotización."""
    diagnostico = ' '.join((cotizacion.diagnostico or '').split())
    if len(diagnostico) > 220:
        diagnostico = diagnostico[:217].rstrip() + '...'

    lineas = [
        f'Hola {cotizacion.cliente_nombre}, le compartimos la cotización '
        f'{cotizacion.numero} de JJ SPICH:',
        '',
        f'Vehículo: {cotizacion.vehiculo_marca} {cotizacion.vehiculo_modelo} '
        f'({cotizacion.vehiculo_placa})',
        f'Diagnóstico: {diagnostico}',
        f'Costo estimado: Bs. {cotizacion.costo_estimado:.2f}',
        f'Validez: {cotizacion.plazo}',
        '',
        f'Ver cotización: {enlace_publico}',
        '',
        'Taller de Chapa y Pintura JJ SPICH — ☎ 72543915',
    ]
    return '\n'.join(lineas)
