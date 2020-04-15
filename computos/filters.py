import django_filters
from django_filters import CharFilter
from .models import Computos

class ComputosFilter(django_filters.FilterSet):

    class Meta:
        model = Computos
        fields = [
            'proyecto',
            'planta',
            'rubro',
            'tipologia',
         
        ]