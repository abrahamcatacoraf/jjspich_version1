from django import forms
from django.contrib.auth.models import User
from .models import Orden, HistorialAdelanto

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            'cliente', 'vehiculo', 'descripcion', 'diagnostico',
            'estado', 'fecha_recepcion', 'fecha_entrega',
            'costo_estimado', 'primer_adelanto', 'tecnico', 'observaciones'
        ]
        widgets = {
            'cliente':         forms.Select(attrs={'class': 'form-select'}),
            'vehiculo':        forms.Select(attrs={'class': 'form-select'}),
            'descripcion':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnostico':     forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado':          forms.Select(attrs={'class': 'form-select'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_entrega':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'costo_estimado':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'primer_adelanto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tecnico':         forms.Select(attrs={'class': 'form-select'}),
            'observaciones':   forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar usuarios del grupo Técnico
        self.fields['tecnico'].queryset = User.objects.filter(
            groups__name='Tecnico'
        )
        self.fields['tecnico'].empty_label = '— Sin asignar —'


class AdelantoForm(forms.ModelForm):
    class Meta:
        model = HistorialAdelanto
        fields = ['monto', 'observacion']
        widgets = {
            'monto':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'observacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo o descripción'}),
        }