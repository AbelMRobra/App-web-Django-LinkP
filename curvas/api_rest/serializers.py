from rest_framework import serializers
from presupuestos.models import Articulos


class ArticuloSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Articulos
        fields='__all__'


class explosion_serializer(serializers.Serializer):
    articulo=ArticuloSerialzer()
    suma=serializers.FloatField()
    comprados=serializers.FloatField()
    dispo=serializers.FloatField()
    saldo=serializers.FloatField()


