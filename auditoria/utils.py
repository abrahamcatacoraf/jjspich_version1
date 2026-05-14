from .models import Auditoria


def registrar(usuario, accion, modelo, objeto_id, detalle):
    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        modelo=modelo,
        objeto_id=objeto_id,
        detalle=detalle,
    )


def generar_detalle_edicion(form, etiquetas):
    cambios = []
    for field in form.changed_data:
        etiqueta = etiquetas.get(field, field)
        viejo = form.initial.get(field)
        nuevo = form.cleaned_data.get(field)
        cambios.append(f"{etiqueta}: '{viejo}' → '{nuevo}'")
    return ', '.join(cambios)
