from django.http import response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ventas.models import ReclamosPostventa
from ventas.serializers.serializers import ReclamosSerializer


class ReclamosViewset(viewsets.ModelViewSet):
    
    queryset = ReclamosPostventa.objects.all()
    serializer_class = ReclamosSerializer
    permission_classes = (AllowAny,)

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