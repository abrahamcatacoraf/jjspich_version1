from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    tipo_pago = forms.ChoiceField(
        choices=[('', 'Seleccione el tipo de pago'), ('final', 'Pago final'), ('adelanto', 'Adelanto')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de pago',
    )

    class Meta:
        model = Pago
        fields = ['orden', 'monto', 'metodo', 'observacion']
        widgets = {
            'orden':       forms.Select(attrs={'class': 'form-select'}),
            'monto':       forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'metodo':      forms.Select(attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observaciones del pago'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tipo_pago'].initial = 'adelanto' if self.instance.es_adelanto else 'final'

    def save(self, commit=True):
        self.instance.es_adelanto = self.cleaned_data.get('tipo_pago') == 'adelanto'
        return super().save(commit=commit)