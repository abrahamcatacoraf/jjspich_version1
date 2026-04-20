from django.shortcuts import render
from clientes.models import Cliente
from vehiculos.models import Vehiculo

def dashboard(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_vehiculos': Vehiculo.objects.count(),
        'total_ordenes': 0,
        'total_pagos': 0,
    }
    return render(request, 'base/dashboard.html', context)