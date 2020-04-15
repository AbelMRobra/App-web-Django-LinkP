import django_filters
from django_filters import CharFilter
from .models import Articulos

class ArticulosFilter(django_filters.FilterSet):

    codigo = CharFilter(field_name='codigo', lookup_expr='icontains', label='Buscar por codigo ')
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains', label='Buscar por nombre ')

    class Meta:
        model = Articulos
        fields = [
         
        ]