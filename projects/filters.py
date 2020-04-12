import django_filters
from django_filters import CharFilter
from .models import Certificados

class CertificadoFilter(django_filters.FilterSet):

    descrip = CharFilter(field_name='descrip', lookup_expr='icontains', label="Buscar por descripción ")

    class Meta:
        model = Certificados
        
        fields = [

            'obra' ,
            'nombre' ,
            
         ]
        labels = {

            'obra':'Buscar por obra' ,
            'nombre':'Buscar por nombre' ,
            
        }
    
       