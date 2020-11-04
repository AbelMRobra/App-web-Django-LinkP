from django import forms
from .models import StockComprasAnticipadas, Comparativas

class StockAntForm(forms.ModelForm):

    class Meta:
        model = StockComprasAnticipadas

        fields = [

            'obra',
            'name',
            'proveedor',
            'articulo',
            'cantidad',
        ]

        labels = {

            'obra':'Obra',
            'name':'Nombre de la compra',
            'proveedor':'Proveedor',
            'articulo':'articulo',
            'cantidad':'cantidad',
        }
