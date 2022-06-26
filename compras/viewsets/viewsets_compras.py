import numpy as np
import datetime
from django.http import response
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from compras.models import Compras, Proveedores, Comparativas
from presupuestos.models import Articulos, Capitulos, CompoAnalisis, Modelopresupuesto
from proyectos.models import Proyectos
from compras.serializers.serializers_compras import ComprasSerializer, ComprasFullSerializer
from compras.functions_comparativas import mensajeCierreOc, mandarEmail
from users.models import VariablesGenerales

class ComparativasViewset(viewsets.GenericViewSet):

    @transaction.atomic
    def upload_monto_minimo(self, request):
        try:
            monto_minimo = VariablesGenerales.objects.get(id = 1)
            monto_minimo.monto_minimo = request.data['monto_minimo']
            monto_minimo.save()
            response = {'message' : 'Success'}
            return Response(response, status=status.HTTP_200_OK)

        except:
            response = {'message' : 'Error'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def change_status(self, request):
        try:

            response = {}
            comparativa = Comparativas.objects.get(id = request.data['id'])
            if comparativa.autoriza == request.data['username'] or comparativa.gerente_autoriza.identificacion == request.data['username']:
                comparativa.estado = request.data['estado']
                comparativa.save()
                
                if comparativa.estado == "AUTORIZADA":
                    if comparativa.publica == "NO":
                        comparativa.visto = "VISTO"

                    if comparativa.autoriza == "SP":
                        comparativa.visto = "VISTO"

                    date = datetime.datetime.now() - datetime.timedelta(hours=3)
                    comparativa.quien_autorizo = request.data['username']
                    comparativa.fecha_autorizacion = date

                    response['action'] = "Compra autorizada"

                elif comparativa.estado == "NO AUTORIZADA":
                    response['action'] = "Compra rechazada"

                else:
                    response['action'] = "Adjunto chequeado"

                comparativa.save()
            response['messege'] = 'Success'
            response['id'] = comparativa.id
            return Response(response, status=status.HTTP_201_CREATED)

        except:
            response = {'mensaje': 'Error de carga'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


class ComprasViewset(viewsets.ModelViewSet):
    queryset = Compras.objects.all()
    serializer_class = ComprasSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:

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

        except:

            response = {'mensaje': 'Error de carga'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


    @action(detail=False, methods=["POST"])
    def consulta_compras(self, request):
        compras = Compras.objects.filter(proyecto = request.data['proyecto'], proveedor__name = request.data['proveedor'], documento = request.data['documento']).order_by("articulo__nombre")
        serializer_proyectos = ComprasFullSerializer(compras, many=True)

        response = {'data' : serializer_proyectos.data}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def consulta_compras_completa(self, request):
        proyectos_seleccionados = request.data['proyectos_seleccionados']
        articulos_seleccionados = request.data['articulos_seleccionados']
        proveedores_seleccionados = request.data['proveedores_seleccionados']

        if len(request.data['proyectos_seleccionados']) != 0:
            compras = Compras.objects.filter(proyecto__nombre__in = proyectos_seleccionados)
        else:
            compras = Compras.objects.all()
        
        print(len(request.data['articulos_seleccionados']))
        if len(request.data['articulos_seleccionados']) != 0:
            compras = Compras.objects.filter(articulo__nombre__in = articulos_seleccionados)

        if len(request.data['proveedores_seleccionados']) != 0:
            compras = Compras.objects.filter(proveedor__name__in = proveedores_seleccionados)

        serializer = ComprasFullSerializer(compras, many=True)
        response = {'data' : serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def modificar_precio_articulo(self, request):
        articulo = Articulos.objects.get(id = request.data['id'])
        articulo.valor = request.data['valor']
        articulo.save()
        response = {'mensaje': 'Success'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def asignar_capitulo(self, request):
        # try:
            capitulo = request.data.pop('capitulo')
            capitulo = Capitulos.objects.get(id = int(capitulo))
            filter = request.data
            compras = Compras.objects.filter(**filter)
            
            for compra in compras:
                compra.capitulo = capitulo
                compra.save()

            response = {'mensaje': 'Success'}
            return Response(response, status=status.HTTP_200_OK)

        # except:

        #     response = {'mensaje': 'Server problem'}
        #     return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["POST"])
    def consulta_articulo(self, request):

        try:

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

            response = {'id': articulo.id,'cantidad' : round(cantidad_presupuesto, 2), 
            'comprado': round(comprado, 2), 'precio': round(articulo.valor, 2), 'partida': round(partida, 2), 'unidad': articulo.unidad}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'messege' : 'Not found'}

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

