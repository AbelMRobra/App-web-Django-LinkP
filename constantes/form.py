from django import forms
from.models import Constantes

class ConsForm(forms.ModelForm):
    class Meta:
        model = Constantes

        fields = [
            'nombre',
            'valor',
            'descrip',
        ]

        labels = {
            'nombre':'Nombre de la constante',
            'valor':'Valor',
            'descrip':'Descripción',          
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'valor': forms.TextInput(attrs={'class':'form-control'}),
            'descrip': forms.TextInput(attrs={'class':'form-control'}),
        }