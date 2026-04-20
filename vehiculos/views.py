from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Vehiculo
from .forms import VehiculoForm

def lista_vehiculos(request):
    busqueda = request.GET.get('buscar', '')
    if busqueda:
        vehiculos = Vehiculo.objects.filter(
            marca__icontains=busqueda
        ) | Vehiculo.objects.filter(
            placa__icontains=busqueda
        ) | Vehiculo.objects.filter(
            cliente__nombre__icontains=busqueda
        )
    else:
        vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/lista.html', {
        'vehiculos': vehiculos,
        'busqueda': busqueda
    })

def nuevo_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo registrado correctamente.')
            return redirect('lista_vehiculos')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculos/form.html', {
        'form': form,
        'titulo': 'Nuevo Vehículo'
    })

def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('lista_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculos/form.html', {
        'form': form,
        'titulo': 'Editar Vehículo'
    })

def eliminar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado correctamente.')
        return redirect('lista_vehiculos')
    return render(request, 'vehiculos/confirmar_eliminar.html', {
        'vehiculo': vehiculo
    })