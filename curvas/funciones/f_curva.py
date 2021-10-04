from curvas.models import SubPartidasCapitulos,ComposicionesSubpartidas, PartidasCapitulos
import numpy as np
import pandas as pd
import datetime as dt
from presupuestos.models import Modelopresupuesto, CompoAnalisis, Capitulos
from proyectos.models import Proyectos
from compras.models import Compras
from computos.models import Computos
from django.db.models import Q

import json

def generar_fechas(fecha_inicial, fecha_final):

    fecha_inicial_reseteada = dt.date(fecha_inicial.year , fecha_inicial.month , 1)
    
    fecha_final_reseteada = dt.date(int(fecha_final[0:4]), int(fecha_final[5:7]), 1)

    fechas=[]

    while fecha_inicial_reseteada.year != fecha_final_reseteada.year and fecha_inicial_reseteada.month != fecha_final_reseteada.month:
        fechas.append(dt.date(fecha_inicial_reseteada.year , fecha_inicial_reseteada.month ,1))
        fecha_inicial_reseteada = fecha_inicial_reseteada + dt.timedelta(32)

    fechas.append(dt.date(fecha_inicial_reseteada.year , fecha_inicial_reseteada.month ,1))
    
    return fechas

def armar_flujo(fecha_inicial, fecha_final, saldo, fechas):

    meses_cuota = (fecha_final.year -  fecha_inicial.year) * 12 + (fecha_final.month -  fecha_inicial.month) +1  
    valor_cuota = saldo/meses_cuota
    
    flujo=[]

    for fecha in fechas:
        if fecha.month == fecha_inicial.month and fecha.year == fecha_inicial.year:
            flujo.append(valor_cuota)
            
        elif fecha.month == fecha_final.month and fecha.year == fecha_final.year:
            flujo.append(valor_cuota)
            
        elif fecha > fecha_inicial and fecha < fecha_final:
            flujo.append(valor_cuota)
            
        else:
            flujo.append(0)
            
    return flujo

def curvas_informacion_cash(id_proyecto, fecha_inicial, fecha_final):

    contenedores = PartidasCapitulos.objects.filter(Q(proyecto__id=id_proyecto) & (Q(fecha_final__gt = fecha_inicial) & Q(fecha_final__lt = fecha_final)) | (Q(fecha_inicial__gt = fecha_inicial) & Q(fecha_inicial__lt = fecha_final)))

    data_cash = []

    for contenedor in contenedores:

        data_contenedor = datos_del_contenedor(contenedor, fecha_inicial, fecha_final)

        data_cash.append(data_contenedor)

    return data_cash

def datos_del_contenedor(contenedor,fecha_i,fecha_f):

    # PASO 1: Consultas necesarias

    proyecto = Proyectos.objects.get(id = contenedor.proyecto.id)
    capitulo = Capitulos.objects.get(id = contenedor.capitulo.id)


    con_modelo = Modelopresupuesto.objects.filter(proyecto = proyecto, capitulo = capitulo)
    con_computos = Computos.objects.filter(proyecto = proyecto)
    con_compoan = CompoAnalisis.objects.all()
    compras = Compras.objects.filter(proyecto = proyecto , capitulo=contenedor.capitulo)

    subpartidas=SubPartidasCapitulos.objects.filter(partida=contenedor)
    
    # PASO 2: Determino la explosión de insumos del contenedor

    data_analisis = [
        
        (modelo.analisis, modelo.cantidad) if modelo.cantidad != None 
        
        else 
            (modelo.analisis, sum(np.array(con_computos.filter(tipologia = modelo.vinculacion).values_list("valor_vacio", flat = True)))) if "SOLO MANO DE OBRA" in str(modelo.analisis.nombre) 
            
            else (modelo.analisis, sum(np.array(con_computos.filter(tipologia = modelo.vinculacion).values_list("valor_lleno", flat = True)))) 
        
        for modelo in con_modelo ]

    data_articulos = [(componente.articulo, componente.cantidad*data[1]) 
    
        for data in data_analisis

        for componente in con_compoan.filter(analisis = data[0])]

    articulos_proyecto = list(set([articulo[0] for articulo in data_articulos]))

    articulos_cant_proyecto = [(articulo, sum(map(lambda n: n[1], filter(lambda n: n[0] == articulo, data_articulos))))
    
    for articulo in articulos_proyecto]

    explosion_insumos = [

        [data[0].codigo,  #ARTICULO 0
        data[1],    #SUMA DE ARTICULOS DEL PRESUPUESTO 1
        sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)), #ARTICULOS COMPRADOS 2
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True))), #CANTIDAD DISPONIBLE EN EL SALDO 3
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)))*data[0].valor] #SALDO
            
        for data in articulos_cant_proyecto]
    
    saldo_total=sum([i[4] for i in explosion_insumos])

    # PASO 3: Calculo el detalle de los sub-contenedores

    sub_contenedores = SubPartidasCapitulos.objects.filter(Q(partida__id=contenedor.id) & (Q(fecha_final__gt = fecha_i) & Q(fecha_final__lt = fecha_f) | (Q(fecha_inicial__gt = fecha_i) & Q(fecha_inicial__lt = fecha_f)) ) )
    
    fechas=generar_fechas(fecha_i,fecha_f)

    data_subContenedores_dataResultante = data_sub_contenedores_data_resultante(sub_contenedores, explosion_insumos, fecha_i,fecha_f, fechas)

    saldo = sum(np.array(data_subContenedores_dataResultante["detalle_contenedor"]["Saldo"]))
    flujo = armar_flujo(contenedor.fecha_i_aplicacion, contenedor.fecha_f_aplicacion, saldo_total, fechas)
    detalle = data_subContenedores_dataResultante["detalle_contenedor"]
    data_sub_contenedores = data_subContenedores_dataResultante["destalles_subcontenedores"]

    detalle=detalle.to_dict('records')

    data_completa = {
        "id":f'{contenedor.proyecto.id}-{contenedor.capitulo.id}',
        "saldo":saldo,
        "flujo":flujo,
        "detalle":detalle,
        "data_sub_contenedores":data_sub_contenedores,
    }

    
    
    return data_completa

def data_sub_contenedores_data_resultante(sub_contenedores, explosion_insumos,fecha_i,fecha_f, fechas):

    explosion_principal = pd.DataFrame(explosion_insumos, columns=['Art', 'Soli', 'Buy', 'Pend', 'Saldo'],)

    destalles_subcontenedores={}

    for sub_contenedor in sub_contenedores:

        necesidad_contenedor = ComposicionesSubpartidas.objects.filter(subpartida = sub_contenedor)

        necesidad_posible = []

        saldo_total = 0
     
        for necesidad in necesidad_contenedor:


            mask = necesidad.articulo.codigo

            df_filtrado_mask = explosion_principal[explosion_principal["Art"] == mask]


            df_filtrado_mask = df_filtrado_mask.reset_index()

            print(df_filtrado_mask ,len(df_filtrado_mask))
        
            saldo_actual=df_filtrado_mask.loc[0,'Saldo']
            #asignar todo lo que necesita la bolsita
            if df_filtrado_mask.loc[0, "Pend"] > necesidad.cantidad:
                              
                gasto=necesidad.cantidad * necesidad.articulo.valor

                saldo_nuevo=saldo_actual - gasto
                
                necesidad_posible.extend([necesidad.articulo, necesidad.cantidad, 0 , saldo_nuevo])

                valor = df_filtrado_mask.loc[0, "Pend"]

                resultado = valor - necesidad.cantidad

                explosion_principal.loc[explosion_principal["Art"] == mask, "Pend"] = resultado

                explosion_principal.loc[explosion_principal["Saldo"] == saldo_actual, "Saldo"] = saldo_nuevo


            #asignar lo que puedo
            elif df_filtrado_mask.loc[0, "Pend"] > 0:

                disponible=df_filtrado_mask.loc[0, "Pend"]

                asignar=disponible

                no_asignado=necesidad.cantidad - asignar

                gasto=asignar * necesidad.articulo.valor
                saldo_nuevo=saldo_actual - gasto

                necesidad_posible.extend([necesidad.articulo, asignar, no_asignado,saldo_nuevo])

                explosion_principal.loc[explosion_principal["Art"] == mask, "Pend"] = 0

                explosion_principal.loc[explosion_principal["Saldo"] == saldo_actual, "Saldo"] = saldo_nuevo

            else:
                necesidad_posible.extend([necesidad.articulo, 0, necesidad.articulo, 0])
                saldo_nuevo=df_filtrado_mask[0,'Saldo']
                explosion_principal.loc[explosion_principal["Saldo"] == saldo_actual, "Saldo"] = saldo_nuevo

            saldo_total += saldo_nuevo
            
        flujo = armar_flujo(sub_contenedor.fecha_inicial, sub_contenedor.fecha_final, saldo_total,fechas)

        data_subcontenedor = {
            "flujo":flujo,
            "necesidad_posible":necesidad_posible,
            "saldo_suncontenedor":saldo_total
        }

        destalles_subcontenedores[f'{sub_contenedor.id}'] = data_subcontenedor

    
    
    
    data_completa = {
        "detalle_contenedor": explosion_principal,
        "destalles_subcontenedores":destalles_subcontenedores,
     
    }

    return data_completa
    


    




    # obtener las bolsitas pertenecientes a las bolsas filtradas

    # compos_subpartidas=[ComposicionesSubpartidas.objects.filter(subpartida__id=subpartida.id) for subpartida in subpartidas]

    # cont=0

    # #iteramos sobre la explosion de insumos para encontrar los articulos que solicita cada bolsita 
    # for e in explosion_insumos:
    #     for compo in compos_subpartidas:
    #         for arti in compo:
    #             #si el articulo de la explosion de insumos coincide con el de esta bolsita entrar:
    #             if arti.articulo == e[0]:

    #                 print(arti.articulo)
    #                 #cantidad disponible en la explosion
    #                 cantidad_disponible=e[3]
                    
    #                 #si la cantidad que solicita la bolsita es menor o igual a la cantidad disponible en la explosion de insumos
    #                 if arti.cantidad <= cantidad_disponible:
    #                     print(arti.cantidad)
                        
                        
    #                     #restamos la cantidad de la bolsita a la cantidad disponible y modificamos en el array
    #                     print(cont)
    #                     print(explosion_insumos[cont][3])
    #                     explosion_insumos[cont][3] = cantidad_disponible - arti.cantidad

                        
                        
    #                 else:
    #                     print('no se llego a cubrir la cantidad solicitada')
                    

    #     cont += 1
    #proceso de asignacion dr articulos

    return None


def guardar_json(datos,id_proyecto):

    proyecto=Proyectos.objects.get(pk=id_proyecto).nombre

    path='curvas/datos_json/flujo_{}.json'.format(proyecto)



    with open(path,'w+') as file:
        contenido= json.dumps(datos, indent = 4,default=str)
        file.write(contenido)
        file.close()