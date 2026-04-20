from django import forms
from .models import Orden

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            'cliente', 'vehiculo', 'descripcion', 'diagnostico',
            'estado', 'fecha_entrega', 'costo_estimado', 'tecnico', 'observaciones'
        ]
        widgets = {
            'cliente':        forms.Select(attrs={'class': 'form-select'}),
            'vehiculo':       forms.Select(attrs={'class': 'form-select'}),
            'descripcion':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe el trabajo a realizar'}),
            'diagnostico':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diagnóstico técnico'}),
            'estado':         forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrega':  forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'costo_estimado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'tecnico':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del técnico asignado'}),
            'observaciones':  forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observaciones adicionales'}),
        }