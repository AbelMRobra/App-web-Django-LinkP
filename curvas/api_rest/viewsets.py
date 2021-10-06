from rest_framework.views import APIView
from rest_framework.response import Response
from curvas.funciones.f_curva2 import saldo_capitulo
from curvas.models import *
from django.db.models import Q
import datetime as dt

class prueba(APIView):


    def get(self,request):


        fecha_i = dt.date.today()

        proyectos=Proyectos.objects.all().values_list()


        context={'proyectos':list(proyectos)}

        fecha_f = dt.date(2023,4,12)

        id_proyecto=1


        contenedor=PartidasCapitulos.objects.filter(Q(proyecto__id=id_proyecto) & (Q(fecha_final__gt = fecha_i) & Q(fecha_final__lt = fecha_f)) | (Q(fecha_inicial__gt = fecha_i) & Q(fecha_inicial__lt = fecha_f)))
        
        analisis_saldos=[saldo_capitulo(cont,fecha_i,fecha_f) for cont in contenedor]


        return Response(analisis_saldos)

