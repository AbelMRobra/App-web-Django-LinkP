import numpy as np
import numpy_financial as npf
from proyectos.models import Proyectos
from django.db.models import Avg, Max, Min,Sum,Q,Count
from finanzas.models import CuentaCorriente,Cuota
import datetime as dt
import math
from proyectos.models import Unidades,Proyectos,ProyeccionesProyectos




def unidadesvendidas(ventas,proyectos,fechas_ordenadas):
    ventas_proyectos=[]
    
    cant_ventas=0
    for p in proyectos:
        proy=Proyectos.objects.get(nombre=p[0])
        mes_proyecto=[]
        for f in fechas_ordenadas:

            monto=ventas.aggregate(suma=Sum('precio_venta' , filter=Q(proyecto__nombre=p[0] ,fecha__month=f.month,fecha__year=f.year)))
            
            cant=ventas.aggregate(cant=Count('unidad', filter=Q(proyecto__nombre=p[0] ,fecha__month=f.month,fecha__year=f.year)))

            anticipos=ventas.aggregate(anticipo=Count('anticipo', filter=Q(proyecto__nombre=p[0] ,fecha__month=f.month,fecha__year=f.year)))

            if monto['suma'] is None:
                monto['suma']=0

            mes_proyecto.append(cant['cant'])
            
            cant_ventas=cant['cant'] + cant_ventas
        ventas_proyectos.append([proy,mes_proyecto])

    promedio_ventas=cant_ventas/len(fechas_ordenadas)

    return ventas_proyectos,promedio_ventas

def get_or_create_datos(unidades_disponibles):

    proyectos_con_unidades=unidades_disponibles.values('proyecto__nombre','proyecto__color').annotate(cant=Count('proyecto__nombre'))
    nombres=[ p['proyecto__nombre'] for p in proyectos_con_unidades]

    #guardo los objetos de cada proyecto con unidades disponibles en esta lista
    proyectos=[Proyectos.objects.get(nombre=n) for n in nombres]


    lista_proyecciones=ProyeccionesProyectos.objects.all()
    
    unidades=[ p['cant'] for p in proyectos_con_unidades]


   
    #aqui se recorren los nombres de los proyectos para obtener o crear instancias del modelo ProyeccionesProyectos
    for n in zip(nombres,unidades):
        nombre=n[0]
        unidades=n[1]

        try:
            proyeccion_proyecto=lista_proyecciones.get(proyecto__nombre=nombre)
        
            
        except:
            pro=Proyectos.objects.get(nombre=nombre)
            unidades=unidades_disponibles.filter(proyecto__nombre=pro.nombre)
            proyeccion_proyecto=ProyeccionesProyectos(
                proyecto=pro,
                cant_unidades=len(unidades),
                ritmo_venta=0,
            )
            proyeccion_proyecto.save()

        #se agrega los datos de cada objeto a un array para poder ser listados en las tabllas

def generar_periodo(*args):

    if  args[0] is False:
        fecha_hoy=dt.date.today()
        fecha_inicio_mes=dt.date(fecha_hoy.year, fecha_hoy.month , 1 )
        fecha_aux=fecha_inicio_mes
        cant_meses=25

    elif args[0] is True:
        fecha_inicial=args[1]
        fecha_final=args[2]
        fecha_inicio_mes=dt.date(fecha_inicial.year,fecha_inicial.month,1)
        #calcular cantidad de meses
        años=fecha_final.year - fecha_inicial.year
        cant_meses=fecha_final.month - fecha_inicial.month + 12*años
        fecha_aux=fecha_inicio_mes


    conj_fechas=[]
    
    for i in range(cant_meses):
        conj_fechas.append(fecha_aux)
        if fecha_aux.month==12:
            fecha_aux=dt.date(fecha_aux.year + 1 , 1 , 1)
        else:
            fecha_aux=dt.date(fecha_aux.year , fecha_aux.month + 1 , 1)
    
    return conj_fechas

def validacion_datos(unidades_disponibles,lista_proyecciones,meses):
   
    #esto lo vi con abel
    #CALCULO DE INICIO Y FIN DE PERIODO
    
    fecha_i=meses[0]
    fecha_f=meses[-1]

    aux_lista=[]

    for i in lista_proyecciones:
        ff=i.fecha_final
        fi=i.fecha_inicial
        rv=i.ritmo_venta
        proyec=i.proyecto
        unidades=len(unidades_disponibles.filter(proyecto=proyec))
        proyeccion=ProyeccionesProyectos.objects.get(pk=i.id)
        #EN EL CASO QUE NO SE INGRESE FECHA FINAL
        if ff is None and fi is not None:
            #SI EL RITMO DE VENTA ES 0 SE AGREGA 2 POR DEFECTO PARA PODER HACER EL CALCULO
            if rv==0:
                rv=2
                proyeccion.ritmo_venta=rv
                proyeccion.save()
            #SI EL RITMO DE VENTA ES DISTINTO DE 0 , ES DECIR QUE SE INGRESO FECHA INICIAL Y RITMO DE VENTA
            meses_consumo=math.ceil(unidades/rv)-1

            #ENTONCES SE CALCULA LA FECHA FINAL
            ff_aux=fi + dt.timedelta(meses_consumo*30)
        
            proyeccion.fecha_final=ff_aux
            proyeccion.save()

            aux_lista.append(proyeccion)
         
        #EN EL CASO QUE NO SE INGRESE FECHA INICIAL
        elif fi is None and ff is not None:
            #SI EL RITMO DE VENTA ES 0 SE AGREGA 2 POR DEFECTO PARA PODER HACER EL CALCULO
            if rv==0:
                rv=2
                proyeccion.ritmo_venta==rv
                proyeccion.save()

            #ENTONCES SE CALCULA LA FECHA INICIAL
            meses_consumo=math.ceil(unidades/rv)-1
            fi_aux=ff - dt.timedelta(meses_consumo*30)
            proyeccion.fecha_inicial=fi_aux
            proyeccion.save()
            aux_lista.append(proyeccion)
        
        #EN EL CASO QUE SOLO SE INGRESE EL RITMO DE VENTA
        elif fi is None and ff is None and rv!=0:
            #ENTONCES SE TOMARA LA FECHA DE HOY COMO INICIAL Y SE CALCULARA LA FECHA FINAL
            fi=dt.date.today()
            proyeccion.fecha_inicial=fi
            meses_consumo=math.ceil(unidades/rv)-1

            #CALCULO DE FECHA FINAL
            ff_aux=fi + dt.timedelta(meses_consumo*30)
            proyeccion.fecha_final=ff_aux
            proyeccion.save()
            aux_lista.append(proyeccion)
        #si se ingresa fecha inicial y final , se calculara el ritmo de venta por mas que se haya ingresado rv tambien
        elif fi is not None and ff is not None:
           
            años=ff.year-fi.year
            if años==0:
                meses=ff.month-fi.month+1
            elif años>=1:
                meses=ff.month-fi.month+1 + (años*12)
            rv=math.ceil(unidades/meses)
            proyeccion.ritmo_venta=rv
            proyeccion.save()
            aux_lista.append(proyeccion)
     
        elif fi is None and ff is None and rv==0:
            pass

    #listar de nuevo los datos actualizados
    lista_proyecciones=ProyeccionesProyectos.objects.all()

    #verificar cual proyecto entra en el rango de fechas propuesto


    aux_proyecciones=[] #esta lista tendra los proyectos que se van a graficar

    if len(aux_lista)!=0:
        for proyeccion in aux_lista:

            if proyeccion.fecha_final > fecha_i and proyeccion.fecha_final < fecha_f:
                aux_proyecciones.append(proyeccion)
            elif proyeccion.fecha_inicial > fecha_i and proyeccion.fecha_inicial < fecha_f:
                aux_proyecciones.append(proyeccion)
            else:
                pass
         

    
    return aux_proyecciones
def proyeccionfuturo(unidades_disponibles,aux_proyecciones,conj_fechas):
    
    proyectos_con_unidades=unidades_disponibles.values('proyecto__nombre','proyecto__color').annotate(cant=Count('proyecto__nombre'))
    nombres=[ p['proyecto__nombre'] for p in proyectos_con_unidades]
    #guardo los objetos de cada proyecto con unidades disponibles en esta lista
    proyectos=[Proyectos.objects.get(nombre=n) for n in nombres]
    #proyectos con unidades disponibles
    unidades=[ p['cant'] for p in proyectos_con_unidades]
    colores=[ p['proyecto__color'] for p in proyectos_con_unidades]
    
    uni_proy=[]
    datos_grafico=[]
    z=0
    


 
    for x in aux_proyecciones:
        proyeccion_aux=ProyeccionesProyectos.objects.get(pk=x.id)
        proyecto=[]
        
        proy=x.proyecto.nombre
        proyecto.extend([proy,colores[z]])
        
        for j in proyectos_con_unidades:
            nombre=j['proyecto__nombre']
            if nombre==proy:
                cant_uni=j['cant']
        fecha_i=x.fecha_inicial
        fecha_f=x.fecha_final



        años=fecha_f.year-fecha_i.year
        if años==0:
            meses=fecha_f.month-fecha_i.month+1
        elif años>=1:
            meses=fecha_f.month-fecha_i.month+1 + (años*12)

        ritmo_venta=math.ceil(cant_uni / meses)
        proyeccion_aux.ritmo_venta=ritmo_venta
        proyeccion_aux.save()

        valores=[]
    
        j=0
        for i in conj_fechas:
       
            fecha_i_aux=dt.date(fecha_i.year,fecha_i.month,1)
            fecha_f_aux=dt.date(fecha_f.year,fecha_f.month,28)
            if i>=fecha_i_aux and i<=fecha_f_aux:
                if cant_uni!=0:
                    
                    resta=cant_uni - ritmo_venta
                
                    if resta>=0:
                        valores.append(ritmo_venta)
                        cant_uni=cant_uni-ritmo_venta
              
                    else:
               
                        valores.append(cant_uni)
                        cant_uni=cant_uni-cant_uni
                    
                else:
                    valores.append(0)
                
            elif i>=fecha_i:
                resta=cant_uni - ritmo_venta
         
                if resta>=0:
                    valores.append(ritmo_venta)
                    cant_uni=cant_uni-ritmo_venta
         
                else:
           
                    valores.append(cant_uni)
                    cant_uni=cant_uni-cant_uni
                 
              
            else:
                valores.append(0)
            
        proyecto.append(valores)
        datos_grafico.append(proyecto)

        z=z+1
   

     
    datos_proyecciones=[]
    fechas_iniciales=[]
    fechas_finales=[]
    ritmos_ventas=[]
    canti_unidades=[]
    #Obtengo los datos finales que seran mostrados en las tablas:
    for obj in ProyeccionesProyectos.objects.all():
        fechas_iniciales.append(obj.fecha_inicial)
      
        fechas_finales.append(obj.fecha_final)

        ritmos_ventas.append(obj.ritmo_venta)

        canti_unidades.append(obj.cant_unidades)

        datos_proyecciones.extend([fechas_iniciales,fechas_finales,ritmos_ventas,canti_unidades])
    return nombres,datos_grafico,datos_proyecciones



def gananciasmensuales(ventas,proyectos,fechas_ordenadas):
    anticipos_meses=[]
    for f in fechas_ordenadas:
        
        suma_mes=0
        for p in proyectos:
        
       
            anticipos_proyecto=ventas.aggregate(suma=Sum('anticipo', filter=Q(proyecto__nombre=p[0] ,fecha__month=f.month,fecha__year=f.year)))
            
            if anticipos_proyecto['suma'] is None:
                anticipos_proyecto['suma']=0
            suma_mes=anticipos_proyecto['suma']+suma_mes

            

        anticipos_meses.append(int(round(suma_mes)))
    
    return anticipos_meses


def calculo_cotizacion(unidad, features_unidad, info_coti, valor_hormigon):




    m2 = 0
    if unidad.sup_equiv > 0:
        m2 = unidad.sup_equiv
    else:
        m2 = unidad.sup_propia + unidad.sup_balcon + unidad.sup_comun + unidad.sup_patio
    precio_contado = m2*unidad.proyecto.desde
    for f2 in features_unidad:
        precio_contado = precio_contado*f2.feature.inc
    
    datos_coti = info_coti.split("&")
    precio_contado = precio_contado * (1-float(datos_coti[4]))
    observacion = datos_coti[5]
    anticipo = float(datos_coti[3])
    anticipo_h = anticipo/valor_hormigon.valor
    cuota_esp = datos_coti[0]
    aporte = datos_coti[1]
    cuotas_p = datos_coti[2]
    total_cuotas = float(cuota_esp) + float(cuotas_p)*1.65 + float(aporte)
    cuotas_espera = []
    cuotas_pose = []
    aporte_va = []

    for i in range(1):
        cuotas_espera.append(0)
        cuotas_pose.append(0)
        aporte_va.append(0)

    for i in range(int(cuota_esp)):
        cuotas_espera.append(1)
        cuotas_pose.append(0)
        aporte_va.append(0)

    if int(aporte) > 0:
        aporte_va.pop()
        aporte_va.append(int(aporte))

    for d in range(int(cuotas_p)):
        cuotas_pose.append(1.65)

    valor_auxiliar_espera = npf.npv(rate=(unidad.proyecto.tasa_f/100), values=cuotas_espera)
    valor_auxiliar_pose = npf.npv(rate=(unidad.proyecto.tasa_f/100), values=cuotas_pose)
    valor_auxiliar_aporte = npf.npv(rate=(unidad.proyecto.tasa_f/100), values=aporte_va)
    factor = valor_auxiliar_aporte + valor_auxiliar_espera + valor_auxiliar_pose
    incremento = (total_cuotas/factor) - 1
    precio_finan = ((precio_contado - float(anticipo))*(1 + incremento)) + float(anticipo)

    importe_cuota_esp = (precio_finan-float(anticipo))/total_cuotas
    importe_aporte = importe_cuota_esp*float(aporte)

    if int(cuotas_p) > 0:

        importe_cuota_p = importe_cuota_esp*1.65

    else:

        importe_cuota_p = 0

    importe_cuota_p_h = importe_cuota_p/valor_hormigon.valor
    importe_aporte_h = importe_aporte/valor_hormigon.valor
    importe_cuota_esp_h = importe_cuota_esp/valor_hormigon.valor

    if cuota_esp != 0:
        valor_cuota_espera = importe_cuota_esp/float(cuota_esp)
    else:
        valor_cuota_espera = 0
    if aporte != 0:
        valor_cuota_entrega = importe_aporte/float(aporte)
    else:
        valor_cuota_entrega = 0
    if cuotas_p != 0:
        valor_cuota_pose = importe_cuota_p/float(cuotas_p)
    else:
        valor_cuota_pose = 0

    datos_coti = [anticipo, anticipo_h, precio_finan, cuota_esp, importe_aporte, cuotas_p, importe_cuota_esp, aporte, importe_cuota_p, importe_cuota_p_h, importe_cuota_esp_h, importe_aporte_h, valor_cuota_espera, valor_cuota_entrega, valor_cuota_pose, observacion]
    return datos_coti