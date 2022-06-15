from rest_framework import serializers

class EntregasSerializer(serializers.Serializer):
    cantidad = serializers.SerializerMethodField()
    destino = serializers.SerializerMethodField()
    fecha = serializers.SerializerMethodField()

    def get_cantidad(self, instance):
        return instance.cantidad

    def get_fecha(self, instance):
        return instance.fecha

    def get_destino(self, instance):
        return instance.usuario_recibe.identificacion
