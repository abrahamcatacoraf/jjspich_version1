from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ordenes.models import Orden
from clientes.models import Cliente
from vehiculos.models import Vehiculo
from inventario.models import Insumo
from pagos.models import Pago

def crear_grupos():
    # ── ADMINISTRADOR ──────────────────────────────────────────
    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    # Acceso total — se maneja desde is_staff en Django

    # ── TÉCNICO ────────────────────────────────────────────────
    tecnico_group, _ = Group.objects.get_or_create(name='Tecnico')
    tecnico_perms = []
    for model in [Orden]:
        ct = ContentType.objects.get_for_model(model)
        tecnico_perms += Permission.objects.filter(
            content_type=ct,
            codename__in=[f'view_{model.__name__.lower()}',
                          f'change_{model.__name__.lower()}']
        )
    tecnico_group.permissions.set(tecnico_perms)

    # ── RECEPCIONISTA ──────────────────────────────────────────
    recep_group, _ = Group.objects.get_or_create(name='Recepcionista')
    recep_perms = []
    for model in [Cliente, Vehiculo, Orden, Insumo]:
        ct = ContentType.objects.get_for_model(model)
        recep_perms += Permission.objects.filter(
            content_type=ct,
            codename__in=[
                f'add_{model.__name__.lower()}',
                f'view_{model.__name__.lower()}',
                f'change_{model.__name__.lower()}',
            ]
        )
    recep_group.permissions.set(recep_perms)