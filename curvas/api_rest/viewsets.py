from rest_framework.views import APIView
from rest_framework.response import Response
from curvas.funciones.f_curva import *
from curvas.models import *
from django.db.models import Q
import datetime as dt

class curva_inversion(APIView):

    def get(self, request):

        #-> PREVIO: Datos que tendre

        fecha_inicial_enviada = dt.date.today()

        fecha_final_enviada = "2022-01-12"

        id_proyecto_enviado = 1

        #-> PASO 1: Hacer array de fechas

        array_fechas = generar_fechas(fecha_inicial_enviada, fecha_final_enviada)

        #-> PASO 2: Toda la información del cash

        informacion_cash = curvas_informacion_cash(id_proyecto_enviado, fecha_inicial_enviada, fecha_final_enviada)

        json_final = {
            "array_fechas": array_fechas,
            "informacion_cash": informacion_cash,
        }


        return Response(json_final)

