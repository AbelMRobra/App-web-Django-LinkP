from rest_framework import serializers
from compras.models import Proveedores

class ProveedoresSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Proveedores
        fields = ('__all__')
