from proyectos.models import ProyectosTerceros
from django.shortcuts import render , redirect
from curvas.funciones.f_curva import saldo_capitulo
import datetime as dt
from .models import PartidasCapitulos
from django.db.models import Q

def curvas_principal(request):

    fecha_i = dt.date.today()
    fecha_f = dt.date(2022,9,28)

    id_proyecto=1


    contenedor=PartidasCapitulos.objects.filter(Q(proyecto__id=id_proyecto) & (Q(fecha_final__gt = fecha_i) & Q(fecha_final__lt = fecha_f)) | (Q(fecha_inicial__gt = fecha_i) & Q(fecha_inicial__lt = fecha_f)))
    
    analisis_saldos=[saldo_capitulo(cont,fecha_i,fecha_f) for cont in contenedor]





    template_name='curvas_principal.html'
    context={'partidas':contenedor,
             'analisis_saldos':analisis_saldos}
    return render(request , template_name , context)