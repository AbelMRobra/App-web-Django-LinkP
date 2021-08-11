from .functions import proyeccionfuturo, unidadesvendidas,gananciasmensuales,proyeccionfuturo,validacion_datos,get_or_create_datos,generar_periodo
from proyectos.models import ProyeccionesProyectos, Unidades, Proyectos
from django.shortcuts import render,redirect,reverse
from django.db.models import Count
from ventas.models import VentasRealizadas
import datetime


def flujoventas(request):
    lista_proyecciones=ProyeccionesProyectos.objects.all()
    
    try: 
        cambiar_periodo=bool(request.GET.get('cambiar_periodo'))
        
        fi=request.GET.get('nuevo_fi_periodo')
        ff=request.GET.get('nuevo_ff_periodo')
        nuevo_fi_periodo=datetime.datetime.strptime(fi, "%Y-%m-%d").date()
        nuevo_ff_periodo=datetime.datetime.strptime(ff, "%Y-%m-%d").date()
    
    except:
        cambiar_periodo=False

    if request.method=='POST':
        
        datos=request.POST.dict()


        if 'id' in datos:
            proy=lista_proyecciones.get(pk=request.POST['id'])

            if 'fecha_inicial' in datos:
                if request.POST['fecha_inicial'] =='':
                    proy.fecha_inicial=None
                else:
                    proy.fecha_inicial=request.POST['fecha_inicial']
                

            if 'fecha_final' in datos:
                if request.POST['fecha_final'] =='':
                    
                    proy.fecha_final=None
                else:
                    
                    proy.fecha_final=request.POST['fecha_final']

            if 'ritmo_venta' in datos:
                proy.ritmo_venta=request.POST['ritmo_venta']
            proy.save()        
            #actualizar datos
            lista_proyecciones=ProyeccionesProyectos.objects.all()
            
            return redirect('Flujo de ventas')

        if 'fi_periodo' in datos and 'ff_periodo' in datos:
            cambiar_periodo=str(True)
            nuevo_fi_periodo=str(request.POST['fi_periodo'])
            nuevo_ff_periodo=str(request.POST['ff_periodo'])

            
            
            return redirect('/ventas/flujoventas/?cambiar_periodo={}&nuevo_ff_periodo={}&nuevo_fi_periodo={}'.format(cambiar_periodo,nuevo_ff_periodo,nuevo_fi_periodo))
    #obtengo las unidades disponibles
    unidades_disponibles=Unidades.objects.filter(estado='DISPONIBLE')
   
    #obtengo los proyectos con unidades disponibles
    proyectos_con_unidades=unidades_disponibles.values('proyecto__nombre','proyecto__color').annotate(cant=Count('proyecto__nombre'))

    #obtengo los nombres de proyectos con unidades disponibles
    nombres=[ p['proyecto__nombre'] for p in proyectos_con_unidades]

    #guardo los objetos de cada proyecto con unidades disponibles en esta lista
    proyectos=[Proyectos.objects.get(nombre=n) for n in nombres]
  
    if cambiar_periodo:
        meses=generar_periodo(cambiar_periodo,nuevo_fi_periodo,nuevo_ff_periodo)
        fi_periodo=meses[0]
        ff_periodo=meses[-1]
        
    else:
        meses=generar_periodo(cambiar_periodo)
        fi_periodo=meses[0]
        ff_periodo=meses[-1]
        

    get_or_create_datos(unidades_disponibles)

    lista_proyecciones=ProyeccionesProyectos.objects.all()

    aux_proyecciones=validacion_datos(unidades_disponibles,lista_proyecciones,meses)

    

    nombres,datos_grafico,datos_proyecciones=proyeccionfuturo(unidades_disponibles,aux_proyecciones,meses)

    #FALTA REFACTORIZAR
    ventas=VentasRealizadas.objects.all()
    fechas=ventas.values('fecha__month','fecha__year').distinct()
    proyectos=ventas.values_list('proyecto__nombre').distinct()


    fechas_aux=[]
    for f in fechas:
            mes=f['fecha__month']
            año=f['fecha__year']
            fechas_aux.append(datetime.datetime(año,mes,1))
    fechas_ordenadas=sorted(fechas_aux)

    ventas_proyectos,prom_ventas=unidadesvendidas(ventas,proyectos,fechas_ordenadas)

    anticipos_meses=gananciasmensuales(ventas,proyectos,fechas_ordenadas)

    

    context={'datos_proyecciones':datos_proyecciones,'proyectos':lista_proyecciones,
            'fechas':fechas_ordenadas,'ventas_proyectos':ventas_proyectos,
            'anticipos_meses':anticipos_meses,'prom_ventas':round(prom_ventas),
            'meses':meses,'datos_grafico':datos_grafico,'periodo': {'ff_periodo': ff_periodo,'fi_periodo':fi_periodo}}
    #############################################
    


    return render(request,'flujoproyeccionventas.html',context)
