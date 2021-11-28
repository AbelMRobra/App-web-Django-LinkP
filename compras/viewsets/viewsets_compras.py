import numpy as np
from django.http import response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from compras.models import Compras, Proveedores
from presupuestos.models import Articulos, CompoAnalisis, Modelopresupuesto
from proyectos.models import Proyectos
from compras.serializers.serializers_compras import ComprasSerializer, ComprasFullSerializer


class ComprasViewset(viewsets.ModelViewSet):
    queryset = Compras.objects.all()
    serializer_class = ComprasSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # try:

            articulo = Articulos.objects.get(nombre = request.data['articulo'])
            proyecto = Proyectos.objects.get(id = int(request.data['proyecto']))
            proveedor = Proveedores.objects.get(name = request.data['proveedor'])


            if float(request.data['cantidad_presupuesto']) <= 0 or float(request.data["partida"]) <= 0:
                imprevisto = "IMPREVISTO"
            else:
                imprevisto = "PREVISTO"

            nueva_compra = Compras(
                proyecto = proyecto,
                proveedor = proveedor,
                nombre = request.data['documento'],
                documento = request.data['documento'],
                articulo = articulo,
                tipo = 'NORMAL',
                cantidad = request.data["cantidad"],
                precio = request.data["precio"],
                precio_presup = request.data["precio_presup"],
                fecha_c = request.data["fecha_c"],
                partida = request.data["partida"],
                imprevisto = imprevisto,
            )

            nueva_compra.save()

            response = {'mensaje': 'Success'}
            return Response(response, status=status.HTTP_201_CREATED)

        # except:

        #     response = {'mensaje': 'Error de carga'}
        #     return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


    @action(detail=False, methods=["POST"])
    def consulta_compras(self, request):
        compras = Compras.objects.filter(proyecto = request.data['proyecto'], proveedor__name = request.data['proveedor'], documento = request.data['documento']).order_by("articulo__nombre")
        serializer_proyectos = ComprasFullSerializer(compras, many=True)

        response = {'data' : serializer_proyectos.data}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def consulta_articulo(self, request):

        articulo = Articulos.objects.get(nombre = request.data['articulo'])
        composicion_analisis = CompoAnalisis.objects.filter(articulo = articulo)
        cantidad_presupuesto = 0
        for composicion in composicion_analisis:
            modelos = Modelopresupuesto.objects.filter(proyecto = request.data['proyecto'], analisis = composicion.analisis)
            if len(modelos) > 0:
                for modelo in modelos:
                    if modelo.cantidad and composicion.cantidad:
                        cantidad_presupuesto += (modelo.cantidad * composicion.cantidad)

        comprado = sum(np.array(Compras.objects.filter(proyecto = request.data['proyecto'], articulo = articulo).values_list("cantidad", flat=True)))
        partida = (cantidad_presupuesto - comprado)*articulo.valor

        response = {'cantidad' : round(cantidad_presupuesto, 2), 
        'comprado': round(comprado, 2), 'precio': round(articulo.valor, 2), 'partida': round(partida, 2), 'unidad': articulo.unidad}

        return Response(response, status=status.HTTP_200_OK)
