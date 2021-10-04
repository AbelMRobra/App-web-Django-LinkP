from rest_framework import serializers
from presupuestos.models import Articulos




class ArticuloSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Articulos
        fields='__all__'

class NecesidadPosibleSerializer(serializers.ListField):
    child=serializers.CharField()

class ListaFlujo(serializers.ListField):
    child=serializers.FloatField()

class PersonalizadoSerializer(serializers.Serializer):
    flujo=ListaFlujo()
    necesidad_posible=NecesidadPosibleSerializer()
    saldo_suncontenedor=serializers.FloatField()


class SubContenedoresSerializer(serializers.DictField):
    child = PersonalizadoSerializer()

class FlujoSerializer(serializers.ListField):
    child = serializers.FloatField()


class ValuesDetallesSerializer(serializers.DictField):
    child=serializers.FloatField()

class DetalleSerializer(serializers.ListField):
    child = ValuesDetallesSerializer()



class InfoCashSerializerDetalle(serializers.Serializer):
    id=serializers.CharField()
    saldo=serializers.FloatField()
    flujo=FlujoSerializer()
    detalle=DetalleSerializer()
    data_sub_contenedores=SubContenedoresSerializer()

class InfoCashSerializer(serializers.ListField):
    child=InfoCashSerializerDetalle()

class ListaFechasSerializer(serializers.ListField):
    child=serializers.DateField()

class JsonFinalSerializer(serializers.Serializer):
    array_fechas=ListaFechasSerializer()
    informacion_cash=InfoCashSerializer()

class CrearFlujoSerializer(serializers.Serializer):
    proyecto=serializers.IntegerField(required=True)
    fecha_final=serializers.CharField(required=True)


class explosion_serializer(serializers.Serializer):
    articulo=ArticuloSerialzer()
    suma=serializers.FloatField()
    comprados=serializers.FloatField()
    dispo=serializers.FloatField()
    saldo=serializers.FloatField()