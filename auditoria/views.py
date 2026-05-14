from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from taller_jjspich.decoradores import solo_admin
from .models import Auditoria


@login_required
@solo_admin
def lista_auditoria(request):
    registros = Auditoria.objects.all().select_related('usuario')[:200]
    return render(request, 'auditoria/lista.html', {
        'registros': registros,
    })
