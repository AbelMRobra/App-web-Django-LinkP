from rest_framework import serializers
from compras.models import Compras
from presupuestos.models import Articulos

class ArticulosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articulos
        fields = ('codigo', 'nombre', 'unidad')

class ComprasFullSerializer(serializers.ModelSerializer):

    articulo = ArticulosSerializer(many = False)
    
    class Meta:
        model = Compras
        fields = ('id', 'proyecto', 'articulo', 'cantidad', 'precio', 'fecha_c')

class ComprasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Compras
        fields = ('__all__')
