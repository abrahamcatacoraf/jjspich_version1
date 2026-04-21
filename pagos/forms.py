from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['orden', 'monto', 'metodo', 'es_adelanto', 'observacion']
        widgets = {
            'orden':       forms.Select(attrs={'class': 'form-select'}),
            'monto':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'metodo':      forms.Select(attrs={'class': 'form-select'}),
            'es_adelanto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observaciones del pago'}),
        }