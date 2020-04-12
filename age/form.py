from django import forms
from .models import Agenda

class AgendaForm(forms.ModelForm):

    class Meta:
        model = Agenda
        fields = [
            'codigo',
            'nombre',
            'Unidad', 
            'constante',
            'valor', 
            'descrip', 
        ]
        labels = {
            'codigo':'Codigo',
            'nombre':'Nombre del articulo',
            'Unidad':'Unidad',  
            'constante':'Constante',
            'valor':'Valor', 
            'descrip':'Descripción', 
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'Unidad': forms.TextInput(attrs={'class':'form-control'}), 
            'constante': forms.Select(attrs={'class':'form-control'}),
            'valor': forms.TextInput(attrs={'class':'form-control'}),
            'descrip': forms.TextInput(attrs={'class':'form-control'}), 
        }

   
