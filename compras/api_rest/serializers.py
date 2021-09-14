from rest_framework import serializers
from compras.models import Compras, Comparativas, Proveedores

class Compras_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Compras
        fields=('__all__')

class Comparativas_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Comparativas
        fields=('proveedor', 'proyecto', 'estado', 'numero')

class Proveedores_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Proveedores
        fields=('__all__')