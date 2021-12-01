import numpy as np
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from presupuestos.models import Articulos
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
            serializer = InventarioFullSerializer(data, many=True)
            response = {'data' : serializer.data}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'message': 'Not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["GET"])
    def consulta_valor_inventario(self, request):
        try:
            inventarios = Inventario.objects.all()
            amort_values = [ amort.valor_amortizacion() for amort in inventarios ]
            amort_value = sum(amort_values)

            response = {'data' : amort_value}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'message': 'Not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=["GET"])
    def consulta_resumen_articulos(self, request):
        try:
            
            inventarios = Inventario.objects.all().values_list("articulo", flat=True).distinct()
            data = []
            for inventario in inventarios:
                dic_data = {}
                dic_data['id_articulo'] = Articulos.objects.get(codigo = inventario).codigo
                dic_data['articulo'] = Articulos.objects.get(codigo = inventario).nombre
                dic_data['cantidad'] = len(Inventario.objects.filter(articulo = inventario))
                data.append(dic_data)

            response = {'data' : data}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'message': 'Not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)