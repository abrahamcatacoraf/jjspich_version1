from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from taller_jjspich.decoradores import solo_admin
from auditoria.utils import registrar
from .models import Cliente
from .forms import ClienteForm

@login_required
def lista_clientes(request):
    busqueda = request.GET.get('buscar', '')
    if busqueda:
        clientes = Cliente.objects.filter(
            nombre__icontains=busqueda
        ) | Cliente.objects.filter(
            apellido__icontains=busqueda
        ) | Cliente.objects.filter(
            telefono__icontains=busqueda
        )
    else:
        clientes = Cliente.objects.all()
    return render(request, 'clientes/lista.html', {
        'clientes': clientes,
        'busqueda': busqueda
    })

@login_required
def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            registrar(request.user, 'creacion', 'Cliente', cliente.pk, f"Se creó Cliente: {cliente}")
            messages.success(request, 'Cliente registrado correctamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form.html', {
        'form': form,
        'titulo': 'Nuevo Cliente'
    })

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            registrar(request.user, 'edicion', 'Cliente', cliente.pk, f"Se editó Cliente: {cliente}")
            messages.success(request, 'Cliente actualizado correctamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })

@login_required
@solo_admin
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        registrar(request.user, 'eliminacion', 'Cliente', cliente.pk, f"Se eliminó Cliente: {cliente} (CI: {cliente.ci})")
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('lista_clientes')
    return render(request, 'clientes/confirmar_eliminar.html', {
        'cliente': cliente
    })