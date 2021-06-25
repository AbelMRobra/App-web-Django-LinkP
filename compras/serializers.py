from rest_framework import serializers


from presupuestos.models import Articulos



class articulos_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Articulos
        fields=('__all__')