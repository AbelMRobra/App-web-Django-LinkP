from proyectos.models import Proyectos
from django.shortcuts import render , redirect
from curvas.funciones.f_curva import saldo_capitulo , generar_fechas
import datetime as dt
from .models import PartidasCapitulos
from django.db.models import Q

def curvas_principal(request):

    fecha_i = dt.date.today()
    proyectos=Proyectos.objects.all()
    context={'proyectos':proyectos}


    if request.method=='POST':
        datos=request.POST.dict()

        

        fecha_f = datos['fecha_final']

        id_proyecto=int(datos['proyecto'])


        contenedor=PartidasCapitulos.objects.filter(Q(proyecto__id=id_proyecto) & (Q(fecha_final__gt = fecha_i) & Q(fecha_final__lt = fecha_f)) | (Q(fecha_inicial__gt = fecha_i) & Q(fecha_inicial__lt = fecha_f)))
        
        analisis_saldos=[saldo_capitulo(cont,fecha_i,fecha_f) for cont in contenedor]

        
        context['contenedor']=contenedor
        context['analisis_saldos']=analisis_saldos





    template_name='curvas_principal.html'
    
    return render(request , template_name , context)