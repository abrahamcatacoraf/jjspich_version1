from django import forms
from .models import Cotizacion


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            'fecha', 'plazo', 'tecnico', 'cliente_nombre',
            'vehiculo_marca', 'vehiculo_modelo', 'vehiculo_placa',
            'vehiculo_color', 'vehiculo_anio', 'diagnostico',
            'costo_estimado', 'notas',
        ]
        widgets = {
            'fecha':            forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'plazo':            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 15 días'}),
            'tecnico':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del técnico'}),
            'cliente_nombre':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del cliente'}),
            'vehiculo_marca':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Toyota'}),
            'vehiculo_modelo':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Corolla'}),
            'vehiculo_placa':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1234ABC', 'style': 'text-transform:uppercase'}),
            'vehiculo_color':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Rojo'}),
            'vehiculo_anio':    forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2020'}),
            'diagnostico':      forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del diagnóstico técnico'}),
            'costo_estimado':   forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'notas':            forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Términos, condiciones, garantía...'}),
        }
