import numpy as np
from presupuestos.models import Modelopresupuesto, CompoAnalisis
from proyectos.models import Proyectos
from compras.models import Compras
from computos.models import Computos

def Creditocapitulo(id_proyecto):

    # Primero vemos todas las consultas

    proyecto = Proyectos.objects.get(id = id_proyecto)
    con_modelo = Modelopresupuesto.objects.filter(proyecto = proyecto)
    con_computos = Computos.objects.filter(proyecto = proyecto)
    con_compoan = CompoAnalisis.objects.all()
    compras = Compras.objects.filter(proyecto = proyecto)

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

        (data[0], 
        data[1], 
        sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)), 
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True))), 
        (data[1] - sum(compras.filter(articulo = data[0]).values_list("cantidad", flat=True)))*data[0].valor)
            
        for data in articulos_cant_proyecto]

    # Esta parte arma los articulos que no estan en el presupuesto

    compras_no_presentes = filter(lambda x: x.articulo not in articulos_proyecto, compras)

    explosion_credito_f = list(set([(compra.articulo, 0, 
    sum(compras.filter(articulo = compra.articulo).values_list("cantidad", flat=True)),
    -sum(compras.filter(articulo = compra.articulo).values_list("cantidad", flat=True)),
    -sum(compras.filter(articulo = compra.articulo).values_list("cantidad", flat=True))*compra.articulo.valor)
    for compra in compras_no_presentes]))
    
    return [explosion_insumos, explosion_credito_f]

