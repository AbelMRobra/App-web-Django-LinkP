from proyectos.models import Proyectos
from django.shortcuts import render , redirect
from django.http import HttpResponse
from curvas.funciones.f_curva import *
import datetime as dt
from .models import PartidasCapitulos
from django.db.models import Q

def curvas_principal(request):

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

    return HttpResponse(json_final)


    
    
