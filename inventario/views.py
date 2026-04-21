from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Insumo
from .forms import InsumoForm, AjusteStockForm

@login_required
def lista_inventario(request):
    categoria = request.GET.get('categoria', '')
    busqueda  = request.GET.get('buscar', '')
    insumos   = Insumo.objects.all()
    if categoria:
        insumos = insumos.filter(categoria=categoria)
    if busqueda:
        insumos = insumos.filter(nombre__icontains=busqueda)
    return render(request, 'inventario/lista.html', {
        'insumos':   insumos,
        'categoria': categoria,
        'busqueda':  busqueda,
    })

@login_required
def nuevo_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo registrado correctamente.')
            return redirect('lista_inventario')
    else:
        form = InsumoForm()
    return render(request, 'inventario/form.html', {
        'form': form, 'titulo': 'Nuevo Insumo'
    })

@login_required
def editar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Insumo actualizado correctamente.')
            return redirect('lista_inventario')
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'inventario/form.html', {
        'form': form, 'titulo': f'Editar {insumo.nombre}'
    })

@login_required
def ajustar_stock(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        form = AjusteStockForm(request.POST)
        if form.is_valid():
            tipo     = form.cleaned_data['tipo']
            cantidad = form.cleaned_data['cantidad']
            if tipo == 'entrada':
                insumo.cantidad += cantidad
                messages.success(request, f'Se agregaron {cantidad} {insumo.unidad} de {insumo.nombre}.')
            else:
                if cantidad > insumo.cantidad:
                    messages.error(request, 'No hay suficiente stock para realizar la salida.')
                    return redirect('ajustar_stock', pk=pk)
                insumo.cantidad -= cantidad
                messages.warning(request, f'Se retiraron {cantidad} {insumo.unidad} de {insumo.nombre}.')
            insumo.save()
            return redirect('lista_inventario')
    else:
        form = AjusteStockForm()
    return render(request, 'inventario/ajustar_stock.html', {
        'form': form, 'insumo': insumo
    })

@login_required
def eliminar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        insumo.delete()
        messages.success(request, 'Insumo eliminado correctamente.')
        return redirect('lista_inventario')
    return render(request, 'inventario/confirmar_eliminar.html', {'insumo': insumo})