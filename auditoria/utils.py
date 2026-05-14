from .models import Auditoria


def registrar(usuario, accion, modelo, objeto_id, detalle):
    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        modelo=modelo,
        objeto_id=objeto_id,
        detalle=detalle,
    )
