from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from sigma.models import Inventario
from sigma.serializer import *

class InventarioViewset(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=["POST"])
    def consulta_articulos(self, request):
        try:
            data = Inventario.objects.filter(articulo__nombre = request.data['nombre_articulo'])
            serializer = InventarioSerializer(data, many=True)
            response = {'data' : serializer.data}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'message': 'Not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)