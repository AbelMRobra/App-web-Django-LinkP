from curvas.models import SubPartidasCapitulos,ComposicionesSubpartidas, PartidasCapitulos
import numpy as np
import datetime as dt
from presupuestos.models import Modelopresupuesto, CompoAnalisis, Capitulos
from proyectos.models import Proyectos
from compras.models import Compras
from computos.models import Computos
from django.db.models import Q

def generar_fechas(fecha_inicial, fecha_final):

    fecha_inicial_reseteada = dt.date(fecha_inicial.year , fecha_inicial.month , 1)
    fecha_final_reseteada = dt.date(int(fecha_final[0:4]), int(fecha_final[5:7]), 1)

    fechas=[]

    while fecha_inicial_reseteada.year != fecha_final_reseteada.year and fecha_inicial_reseteada.month != fecha_final_reseteada.month:
        fechas.append(dt.date(fecha_inicial_reseteada.year , fecha_inicial_reseteada.month ,1))
        fecha_inicial_reseteada = fecha_inicial_reseteada + dt.timedelta(30)

    fechas.append(dt.date(fecha_inicial_reseteada.year , fecha_inicial_reseteada.month ,1))

    return fechas

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

        [data[0],  #ARTICULO 0
        data[1],    #SUMA DE ARTICULOS DEL PRESUPUESTO 1
        sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)), #ARTICULOS COMPRADOS 2
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True))), #CANTIDAD DISPONIBLE EN EL SALDO 3
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)))*data[0].valor] #SALDO
            
        for data in articulos_cant_proyecto]
    
    saldo_total=sum([i[4] for i in explosion_insumos])

    # PASO 3: Calculo el detalle de los sub-contenedores

    sub_contenedores = SubPartidasCapitulos.objects.filter(Q(partida__id=contenedor.id) & (Q(fecha_final__gt = fecha_i) & Q(fecha_final__lt = fecha_f) | (Q(fecha_inicial__gt = fecha_i) & Q(fecha_inicial__lt = fecha_f)) ) )
    
    data_subContenedores_dataResultante = data_sub_contenedores_data_resultante(sub_contenedores, explosion_insumos)
    

    #partidas : contenedores -> subpartidas : bolsas -> composicionesubpartidas : bolsitas 
    #las bolsitas contienen el articulo y la cantidad que necesito

    #obtener las bolsas pertenecientes al contenedor actual y que cumplan el rango de fecha establecido
    subpartidas=SubPartidasCapitulos.objects.filter(Q(partida__id=contenedor.id) & (Q(fecha_final__gt = fecha_i) & Q(fecha_final__lt = fecha_f) | (Q(fecha_inicial__gt = fecha_i) & Q(fecha_inicial__lt = fecha_f)) ) )
    

    #obtener las bolsitas pertenecientes a las bolsas filtradas

    compos_subpartidas=[ComposicionesSubpartidas.objects.filter(subpartida__id=subpartida.id) for subpartida in subpartidas]

    cont=0

    #iteramos sobre la explosion de insumos para encontrar los articulos que solicita cada bolsita 
    for e in explosion_insumos:
        for compo in compos_subpartidas:
            for arti in compo:
                #si el articulo de la explosion de insumos coincide con el de esta bolsita entrar:
                if arti.articulo == e[0]:

                    print(arti.articulo)
                    #cantidad disponible en la explosion
                    cantidad_disponible=e[3]
                    
                    #si la cantidad que solicita la bolsita es menor o igual a la cantidad disponible en la explosion de insumos
                    if arti.cantidad <= cantidad_disponible:
                        print(arti.cantidad)
                        
                        
                        #restamos la cantidad de la bolsita a la cantidad disponible y modificamos en el array
                        print(cont)
                        print(explosion_insumos[cont][3])
                        explosion_insumos[cont][3] = cantidad_disponible - arti.cantidad

                        
                        
                    else:
                        print('no se llego a cubrir la cantidad solicitada')
                    

        cont += 1
    #proceso de asignacion dr articulos


    detalle={
        'explosion_insumos':explosion_insumos,
        'saldo_total':saldo_total,
        'subpartidas':subpartidas,
    }

    flujo_contenedor = 0
    data_sub_contenedores = 0

    
    
    datos_del_contenedor = {
        "contendor": contenedor,
        "saldo_contenedor":saldo_total,
        "flujo_contenedor":flujo_contenedor,
        "detalle_contenedor":explosion_insumos,
        "data_sub_contenedores":data_sub_contenedores,
    }



    return datos_del_contenedor

def data_sub_contenedores_data_resultante():

    return None

# def curva_calculo_contenedor(id_proyecto, contenedor):

#      # Primero calculo los articulos 
    
#     detalle_capitulo = saldo_capitulo(id_proyecto, contenedor)

#     detalle_bolsas = curva_calculo_bolsas(contenedor)



# def curva_calculo_bolsas(contenedor):

#     con_elementos_bolsas = ['Elemento 1', 'Elemento 2']
#     con_bolsas = ['Elemento 1', 'Elemento 2']

#     for bolsa in con_bolsas:
#         elemento_bolsa = bolsa
#         costo_volsa = sum(np.array())
