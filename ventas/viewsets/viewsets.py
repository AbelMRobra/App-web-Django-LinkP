from django.http import response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ventas.models import FormularioDetallePostventa, ReclamosPostventa, ClasificacionReclamosPostventa, FormularioSolucionPostventa, \
    FormularioDetallePostventa 
from ventas.serializers.serializers import ReclamosSerializer, FormularioSolucionPostventaSerializer, \
    FormularioDetallePostventaSerializer, ClasificacionReclamosPostventaSerializer


class ClasificacionReclamosPostventaViewset(viewsets.ModelViewSet):
    queryset = ClasificacionReclamosPostventa.objects.all()
    serializer_class = ClasificacionReclamosPostventaSerializer
    permission_classes = (AllowAny,)


class FormularioDetallePostventaViewset(viewsets.ModelViewSet):
    queryset = FormularioDetallePostventa.objects.all()
    serializer_class = FormularioDetallePostventaSerializer
    permission_classes = (AllowAny,)

class FormularioSolucionPostventaViewset(viewsets.ModelViewSet):
    
    queryset = FormularioSolucionPostventa.objects.all()
    serializer_class = FormularioSolucionPostventaSerializer
    permission_classes = (AllowAny,)

class ReclamosViewset(viewsets.ModelViewSet):
    
    queryset = ReclamosPostventa.objects.all()
    serializer_class = ReclamosSerializer
    permission_classes = (AllowAny,)

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.clasificacion = ClasificacionReclamosPostventa.objects.get(id = request.data["clasificacion"]).nombre
        instance.save()

        response = {"mensaje": f"Pude modificar a {instance.clasificacion}!"}

        return Response(response, status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=True)

    def estado(self, request, pk):
        try:
            reclamo = ReclamosPostventa.objects.get(id = pk)
            reclamo.estado = request.data["estado"]
            reclamo.save()

            response = {"mensaje": f"Reclamo {reclamo.estado}!"}
            return Response(response, status=status.HTTP_202_ACCEPTED)

        except:

            response = {"mensaje": "Error inesperado"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['POST'], detail=True)

    def cambio_estado(self, request, pk):
        reclamo = ReclamosPostventa.objects.get(id = pk)

        if 'check' in request.data:
            
            if  reclamo.visto == True:
                reclamo.visto = False
                reclamo.save()

                response = {"mensaje": "Pendiente!"}

                return Response(response, status=status.HTTP_202_ACCEPTED)

            else:
                reclamo.visto = True
                reclamo.save()

                response = {"mensaje": "Visto!"}

                return Response(response, status=status.HTTP_202_ACCEPTED)

        else:

            response = {"mensaje": "Error inesperado"}

            return Response(response, status=status.HTTP_400_BAD_REQUEST)