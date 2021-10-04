from curvas.api_rest.serializers import JsonFinalSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from curvas.models import *
from django.db.models import Q
import datetime as dt
from curvas.funciones.f_curva import *
from curvas.serializers import *
import json
from curvas.api_rest.serializers import *



def calcular_datos_api(id_proyecto_enviado,fecha_final_enviada):
    #-> PREVIO: Datos que tendre

        fecha_inicial_enviada = dt.date.today()

        #fecha_final_enviada = "2022-01-12"

        #id_proyecto_enviado = 1

        #-> PASO 1: Hacer array de fechas
       
        array_fechas = generar_fechas(fecha_inicial_enviada, fecha_final_enviada)

        
        #-> PASO 2: Toda la información del cash

        informacion_cash = curvas_informacion_cash(id_proyecto_enviado, fecha_inicial_enviada, fecha_final_enviada)
        
        json_final = {
            "array_fechas": array_fechas,
            "informacion_cash": informacion_cash,
        }

        return json_final
        # serializer=JsonFinalSerializer(json_final)

        # datos_serializados=serializer.data

        
        # datos_json=guardar_json(datos_serializados)

        # datos_python=json.loads(datos_json)

        # datos_response=serializer=JsonFinalSerializer(datos_python).data

def leer_datos_api(proyecto):

    path='curvas/datos_json/flujo_{}.json'.format(proyecto)

    try:
    
        with open(path) as file:
            datos_json=file.read()
            

    except FileNotFoundError:
        mensaje='No existe el archivo del proyecto!'

    datos_python=json.loads(datos_json)

    datos_response=JsonFinalSerializer(datos_python).data

    return datos_response

    


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

        datos=calcular_datos_api(id_proyecto,fecha)
        guardar_json(datos,id_proyecto)

        return Response({'status':200})





#SERIA OPTIMO USAR UN JSON POR PROYECTO

#SIEMPRE SE DEBE ENVIAR EL PROYECTO

#SI NO SE ENVIA LA FECHA FINAL NO HABRA QUE RECALCULAR
    

