from django import forms
from .models import Articulos, Constantes

class ArticulosForm(forms.ModelForm):

    class Meta:
        model = Articulos
        fields = [
            'codigo',
            'nombre',
            'unidad', 
            'constante',
            'valor', 
            'descrip', 
        ]
        labels = {
            'codigo':'Codigo',
            'nombre':'Nombre del articulo',
            'unidad':'Unidad',  
            'constante':'Constante',
            'valor':'Valor', 
            'descrip':'Descripción', 
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'unidad': forms.TextInput(attrs={'class':'form-control'}), 
            'constante': forms.Select(attrs={'class':'form-control'}),
            'valor': forms.TextInput(attrs={'class':'form-control'}),
            'descrip': forms.TextInput(attrs={'class':'form-control'}), 
        }

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

   