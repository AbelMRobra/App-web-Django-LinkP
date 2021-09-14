from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from compras.models import Compras, Comparativas, Proveedores
from .serializers import Compras_Serializer, Comparativas_Serializer, Proveedores_Serializer

class ComprasViewSet(viewsets.ModelViewSet):

    queryset = Compras.objects.all()
    serializer_class =  Compras_Serializer

class ComparativasViewSet(viewsets.ModelViewSet):

    queryset = Comparativas.objects.all()
    serializer_class =  Comparativas_Serializer


class ProveedoresViewSet(viewsets.ModelViewSet):

    queryset = Proveedores.objects.all()
    serializer_class =  Proveedores_Serializer

    @action(detail=True, methods=['get'])
    
    def comparativas(self, request, pk=None):
        queryset = Comparativas.objects.filter(proveedor__id = pk)
        serializer = Comparativas_Serializer(queryset, many=True)
        return Response(serializer.data)
