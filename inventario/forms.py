from django import forms
from .models import Insumo

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'categoria', 'descripcion', 'cantidad',
                  'unidad', 'precio_unitario', 'stock_minimo']
        widgets = {
            'nombre':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del insumo'}),
            'categoria':       forms.Select(attrs={'class': 'form-select'}),
            'descripcion':     forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unidad':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'litro, kilo, unidad...'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_minimo':    forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class AjusteStockForm(forms.Form):
    TIPOS = [
        ('entrada', 'Entrada de stock'),
        ('salida',  'Salida de stock'),
    ]
    tipo     = forms.ChoiceField(choices=TIPOS, widget=forms.Select(attrs={'class': 'form-select'}))
    cantidad = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'})
    )
    motivo   = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del ajuste'})
    )