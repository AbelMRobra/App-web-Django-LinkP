import numpy as np
from presupuestos.models import Prametros, Presupuestos

def presupuestos_precio_desde(id_proyecto):

    parametros = Prametros.objects.get(proyecto__id = id_proyecto)
    presupuesto = Presupuestos.objects.get(proyecto__id = id_proyecto)
                       
    costo = (presupuesto.valor)
    costo_imp = costo*(1 + parametros.imprevitso)
    costo_iva = costo_imp*(1 + parametros.iva)
    costo_soft = costo_iva+(costo * parametros.soft)
    porc_terreno =  parametros.terreno/parametros.proyecto.m2
    porc_hon =  parametros.link/parametros.proyecto.m2
    aumento_tem =  parametros.tem_iibb*parametros.por_temiibb
    aumento_comer =  parametros.comer
    costo_completo = costo_soft/(1-((aumento_tem + aumento_comer)*(1 - porc_terreno - porc_hon))*(1 + parametros.ganancia)/(1 - porc_terreno - porc_hon))
    costo_completo = costo_completo/(1 - porc_terreno - porc_hon)
    costo_depto = costo_completo*parametros.depto/parametros.proyecto.m2

    return costo_depto
