from rest_framework import serializers
from compras.serializers.serializers_compras import ArticulosSerializer
from sigma.models import Inventario

class InventarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventario
        fields = ('__all__')


class InventarioFullSerializer(serializers.ModelSerializer):

    articulo = ArticulosSerializer(many = False)

    class Meta:
        model = Inventario
        fields = ('id', 'num_inv', 'articulo', 'amortizacion', 'fecha_compra', 'fecha_amortizacion', 'valor_amortizacion')