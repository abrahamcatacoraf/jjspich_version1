from django.core.management.base import BaseCommand
from taller_jjspich.perfiles import crear_grupos

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios del sistema'

    def handle(self, *args, **kwargs):
        crear_grupos()
        self.stdout.write(self.style.SUCCESS(
            'Grupos creados: Administrador, Tecnico, Recepcionista'
        ))