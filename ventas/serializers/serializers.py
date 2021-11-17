from rest_framework import serializers
from ventas.models import ReclamosPostventa

class ReclamosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ReclamosPostventa
        fields = ('__all__')
