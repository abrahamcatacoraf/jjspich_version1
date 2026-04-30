from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            'cliente', 'categoria', 'tipo_vehiculo', 'tipo_moto',
            'marca', 'modelo', 'anio', 'placa', 'color',
            'kilometraje', 'gasolina'
        ]
        widgets = {
            'cliente':       forms.Select(attrs={'class': 'form-select'}),
            'categoria':     forms.Select(attrs={'class': 'form-select', 'id': 'id_categoria'}),
            'tipo_vehiculo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_vehiculo'}),
            'tipo_moto':     forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_moto'}),
            'marca':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Toyota'}),
            'modelo':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Corolla'}),
            'anio':          forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2020'}),
            'placa':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234ABC', 'style': 'text-transform:uppercase'}),
            'color':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Rojo'}),
            'kilometraje':   forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 50000', 'step': '0.01'}),
            'gasolina':      forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100', 'min': '0', 'max': '100', 'step': '0.01'}),
        }