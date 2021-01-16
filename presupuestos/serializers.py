from rest_framework import serializers
from .models import Articulos

class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulos
        fields = ('__all__')