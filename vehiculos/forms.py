from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'anio', 'placa', 'color', 'tipo']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'marca':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Toyota'}),
            'modelo':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Corolla'}),
            'anio':    forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2020'}),
            'placa':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234ABC'}),
            'color':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Rojo'}),
            'tipo':    forms.Select(attrs={'class': 'form-select'}),
        }