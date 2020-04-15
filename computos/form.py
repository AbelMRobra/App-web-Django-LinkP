from django import forms
from .models import Computos

class ComputosForm(forms.ModelForm):

    class Meta:
        model = Computos
        fields = [
            'proyecto',
            'planta', 
            'rubro', 
            'tipologia', 
            'valor_lleno', 
            'valor_vacio',
            'valor_total', 
            'valor_obra', 

        ]