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


class notas_serialzier(serializers.ListField):
    nota=serializers.CharField(required=True)

class prueba_serializer(serializers.Serializer):
    nombre=serializers.CharField(required=True)
    apellido=serializers.CharField(required=True)
    notas=notas_serialzier()

