from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'ci', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'ci':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678'}),
            'telefono':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 70012345'}),
            'correo':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@email.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dirección'}),
        }