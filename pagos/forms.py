from django import forms
from django.db.models import Sum
from .models import Pago
from ordenes.models import Orden

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

    def __init__(self, *args, orden_fija=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['orden'].queryset = Orden.objects.exclude(estado='finalizado')
        if orden_fija:
            self.fields['orden'].queryset = Orden.objects.filter(pk=orden_fija)
            self.fields['orden'].initial = orden_fija
            self.fields['orden'].disabled = True
        if self.instance and self.instance.pk:
            self.fields['tipo_pago'].initial = 'adelanto' if self.instance.es_adelanto else 'final'

    def clean(self):
        cleaned_data = super().clean()
        orden = cleaned_data.get('orden')
        monto = cleaned_data.get('monto')
        tipo_pago = cleaned_data.get('tipo_pago')
        if not orden:
            return cleaned_data
        if orden.estado == 'finalizado' or orden.pagos.filter(es_adelanto=False).exists():
            self.add_error('orden', 'Esta orden ya está finalizada, no se pueden registrar más pagos.')
            return cleaned_data
        total_pagado = orden.pagos.aggregate(total=Sum('monto'))['total'] or 0
        saldo = orden.costo_estimado - total_pagado
        if saldo <= 0:
            self.add_error('orden', 'Esta orden ya está totalmente pagada.')
        if monto is not None:
            if monto > saldo:
                self.add_error('monto', f'El monto no puede exceder el saldo pendiente (Bs. {saldo}).')
            elif tipo_pago == 'final' and monto != saldo:
                self.add_error('monto', f'El pago final debe ser exactamente igual al saldo pendiente (Bs. {saldo}).')
        return cleaned_data

    def save(self, commit=True):
        self.instance.es_adelanto = self.cleaned_data.get('tipo_pago') == 'adelanto'
        return super().save(commit=commit)