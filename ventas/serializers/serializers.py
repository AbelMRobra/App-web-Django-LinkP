from rest_framework import serializers
from ventas.models import ReclamosPostventa, FormularioSolucionPostventa, FormularioDetallePostventa, ClasificacionReclamosPostventa

class ReclamosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReclamosPostventa
        fields = ('__all__')


class ClasificacionReclamosPostventaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClasificacionReclamosPostventa
        fields = ('__all__')


class FormularioSolucionPostventaSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormularioSolucionPostventa
        fields = ('__all__')

class FormularioDetallePostventaSerializer(serializers.ModelSerializer):

    class Meta:
        model = FormularioDetallePostventa
        fields = ('__all__')
