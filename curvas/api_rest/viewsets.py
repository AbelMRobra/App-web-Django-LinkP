from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


from curvas.models import *
from curvas.funciones.f_curva import *
from curvas.serializers import *
from curvas.api_rest.serializers import *




class SubPartidasViewSet(viewsets.ModelViewSet):
    pass

class APICurvas(APIView):


    def get(self,request):

        proyecto=request.query_params.get('proyecto',None)

        if proyecto is not None:  #esto quiere decir que no hay recalculo
            response=leer_datos_api(proyecto)
        else:
            response={'error':'Ingrese un proyecto para obtener la informacion'}
        return Response(response)

    def post(self,request):
        #crear flujo con el proyecto y la fecha final
        serializer = CrearFlujoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos=serializer.validated_data
        fecha=datos['fecha_final']
        id_proyecto=datos['proyecto']

        proyecto=Proyectos.objects.filter(pk=id_proyecto)

        if proyecto.count()==0:
            response={'error':'no existe un proyecto con el id ingresado'}
        else:
            datos=calcular_datos_api(id_proyecto,fecha)
            guardar_json(datos,id_proyecto)
            mensaje='se ha calculado el flujo de {}'.format(proyecto[0].nombre)
            response={'status':200,'mensaje':mensaje}

        return Response(response)

