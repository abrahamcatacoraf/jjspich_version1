from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Orden
from .forms import OrdenForm

@login_required
def lista_ordenes(request):
    estado = request.GET.get('estado', '')
    busqueda = request.GET.get('buscar', '')
    ordenes = Orden.objects.all()
    if estado:
        ordenes = ordenes.filter(estado=estado)
    if busqueda:
        ordenes = ordenes.filter(
            cliente__nombre__icontains=busqueda
        ) | ordenes.filter(
            vehiculo__placa__icontains=busqueda
        )
    return render(request, 'ordenes/lista.html', {
        'ordenes': ordenes,
        'estado': estado,
        'busqueda': busqueda,
    })

@login_required
def nueva_orden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orden de trabajo registrada correctamente.')
            return redirect('lista_ordenes')
    else:
        form = OrdenForm()
    return render(request, 'ordenes/form.html', {
        'form': form,
        'titulo': 'Nueva Orden de Trabajo'
    })

@login_required
def editar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orden actualizada correctamente.')
            return redirect('lista_ordenes')
    else:
        form = OrdenForm(instance=orden)
    return render(request, 'ordenes/form.html', {
        'form': form,
        'titulo': f'Editar Orden #{orden.pk}'
    })

@login_required
def detalle_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    return render(request, 'ordenes/detalle.html', {'orden': orden})

@login_required
def eliminar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        messages.success(request, 'Orden eliminada correctamente.')
        return redirect('lista_ordenes')
    return render(request, 'ordenes/confirmar_eliminar.html', {'orden': orden})