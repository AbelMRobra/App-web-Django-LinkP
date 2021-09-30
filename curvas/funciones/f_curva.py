from curvas.models import SubPartidasCapitulos,ComposicionesSubpartidas
import numpy as np
import datetime as dt
from presupuestos.models import Modelopresupuesto, CompoAnalisis, Capitulos
from proyectos.models import Proyectos
from compras.models import Compras
from computos.models import Computos
from django.db.models import Q

 


def generar_fechas(fi,ff):

    inicio=dt.date(fi.year , fi.month , 1)

    fechas=[]

    while inicio.year != ff.year and inicio.month != ff.month:
        fechas.append(dt.date(inicio.year , inicio.month ,1))
        inicio=inicio + dt.timedelta(30)

    return fechas




def saldo_capitulo(contenedor,fecha_i,fecha_f):

    # Primero vemos todas las consultas

    proyecto = Proyectos.objects.get(id = contenedor.proyecto.id)
    capitulo = Capitulos.objects.get(id = contenedor.capitulo.id)


    con_modelo = Modelopresupuesto.objects.filter(proyecto = proyecto, capitulo = capitulo)
    con_computos = Computos.objects.filter(proyecto = proyecto)
    con_compoan = CompoAnalisis.objects.all()
    compras = Compras.objects.filter(proyecto = proyecto , capitulo=contenedor.capitulo)

    subpartidas=SubPartidasCapitulos.objects.filter(partida=contenedor)
    # Este bucle determina los analisis y su cantidad dentro de un proyecto

    data_analisis = [
        
        (modelo.analisis, modelo.cantidad) if modelo.cantidad != None 
        
        else 
            (modelo.analisis, sum(np.array(con_computos.filter(tipologia = modelo.vinculacion).values_list("valor_vacio", flat = True)))) if "SOLO MANO DE OBRA" in str(modelo.analisis.nombre) 
            
            else (modelo.analisis, sum(np.array(con_computos.filter(tipologia = modelo.vinculacion).values_list("valor_lleno", flat = True)))) 
        
        for modelo in con_modelo ]

    # Este bucle determina los cantidad de articulos según la cantidad del analisis

    data_articulos = [(componente.articulo, componente.cantidad*data[1]) 
    
        for data in data_analisis

        for componente in con_compoan.filter(analisis = data[0])]

    # Este bucle determina el listado de articulos del proyecto

    articulos_proyecto = list(set([articulo[0] for articulo in data_articulos]))

    # Este bucle determina el listado de articulos del proyecto y su cantidad total

    articulos_cant_proyecto = [(articulo, sum(map(lambda n: n[1], filter(lambda n: n[0] == articulo, data_articulos))))
    
    for articulo in articulos_proyecto]

    # En este bucle determino articulos presentes en el presupuesto, cantidad necesaria, comprado, saldo, saldo en pesos

    explosion_insumos = [

        [data[0],  #ARTICULO 0
        data[1],    #SUMA DE ARTICULOS DEL PRESUPUESTO 1
        sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)), #ARTICULOS COMPRADOS 2
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True))), #CANTIDAD DISPONIBLE EN EL SALDO 3
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)))*data[0].valor] #SALDO
            
        for data in articulos_cant_proyecto]
    
    saldo_total=sum([i[4] for i in explosion_insumos])
    
    

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



    return detalle

def curva_calculo_contenedor(id_proyecto, contenedor):

     # Primero calculo los articulos 
    
    detalle_capitulo = saldo_capitulo(id_proyecto, contenedor)

    detalle_bolsas = curva_calculo_bolsas(contenedor)



def curva_calculo_bolsas(contenedor):

    con_elementos_bolsas = ['Elemento 1', 'Elemento 2']
    con_bolsas = ['Elemento 1', 'Elemento 2']

    for bolsa in con_bolsas:
        elemento_bolsa = bolsa
        costo_volsa = sum(np.array())
