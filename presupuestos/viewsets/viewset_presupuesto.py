from django.http import response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from presupuestos.models import Presupuestos
from proyectos.models import Proyectos
from presupuestos.serializers import PresupuestosSerializer, ProyectosSerializer


class PresupuestosViewset(viewsets.ModelViewSet):
    queryset = Presupuestos.objects.all()
    serializer_class = PresupuestosSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=["GET"])
    def proyectos_bases(self, request):
        proyectos = Proyectos.objects.filter(presupuesto = "BASE")
        serializer_proyectos = ProyectosSerializer(proyectos, many=True)

        response = {'data' : serializer_proyectos.data}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def asignacion_proyectos(self, request, pk=None):

        try:
            presupuestos = Presupuestos.objects.get(id = pk)
            proyecto = Proyectos.objects.get(id = request.data["proyecto_base"])
            presupuestos.proyecto_base = proyecto
            presupuestos.save()

            response = {'message' : 'Success!'}
            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'message' : 'Problem'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


