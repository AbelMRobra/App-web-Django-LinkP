import numpy as np
import numpy_financial as npf

from finanzas.models import Almacenero
from ventas.models import FeaturesProjects, FeaturesUni, VentasRealizadas
from proyectos.models import Unidades

def atributo_agregar(proyecto, nombre, inc):

    try:

        nuevo_atributo = FeaturesProjects(
            proyecto = proyecto,
            nombre = nombre,
            inc = inc
        )

        nuevo_atributo.save()

        return [1, "Atributo creado correctamente!"]

    except:

        return [0, "Ocurrio un error inesperado"]

def atributo_editar(id_atributo, nombre, inc):

    try:

        atributo_a_editar = FeaturesProjects.objects.get(id = int(id_atributo))
        atributo_a_editar.nombre = nombre
        atributo_a_editar.inc = inc
        atributo_a_editar.save()

        return [1, "Atributo editado correctamente!"]

    except:

        return [0, "Ocurrio un error inesperado"]

def atributo_borrar(id_atributo):

    try:

        atributo_a_borrar = FeaturesProjects.objects.get(id = int(id_atributo))
        atributo_a_borrar.delete()

        return [1, "Atributo borrado correctamente!"]

    except:

        return [0, "Ocurrio un error inesperado"]

def atributo_asignar_unidad(info_template):

    nombre_unidad = info_template[0].split(sep='&')
    nombre = nombre_unidad[0]
    id_unidad = nombre_unidad[1]

    if len(FeaturesUni.objects.filter(feature__nombre = nombre, unidad = int(id_unidad))) == 0 and info_template[1] == "on":
                    
        unidad = Unidades.objects.get(id = int(id_unidad))
        atributo = FeaturesProjects.objects.get(proyecto = unidad.proyecto, nombre = nombre)
    
        nueva_asignacion_atributo_a_unidad = FeaturesUni(
            
            feature = atributo,
            unidad = unidad)
        
        nueva_asignacion_atributo_a_unidad.save()


    if len(FeaturesUni.objects.filter(feature__nombre = nombre, unidad = int(id_unidad))) > 0 and info_template[1] == "off":
        
        asignacion_existente = FeaturesUni.objects.filter(feature__nombre = nombre, unidad = int(id_unidad))

        for asignacion in asignacion_existente:

            asignacion.delete()

def unidades_calculo_m2(id_unidad):

    unidad = Unidades.objects.get(id = id_unidad)

    if unidad.sup_equiv > 0:

        m2_resultante = round(unidad.sup_equiv, 2)

    else:

        m2_resultante = round((unidad.sup_propia + unidad.sup_balcon + unidad.sup_comun + unidad.sup_patio), 2)

    return m2_resultante

def unidades_calculo_precio_final(id_unidad):

    unidad = Unidades.objects.get(id = id_unidad)

    m2_resultante = unidades_calculo_m2(id_unidad)

    atributos_unidad = FeaturesUni.objects.filter(unidad = unidad)

    if unidad.proyecto.desde:
        precio_base = m2_resultante*unidad.proyecto.desde
    
    else:
        precio_base = m2_resultante
    
    precio_final = precio_base

    for atributo in atributos_unidad:

        precio_final = precio_final*atributo.feature.inc

    unidad.contado = precio_final
    unidad.save()

    return [precio_base, precio_final]

def pricing_editar_unidad(id_unidad, numero, piso, nombre, tipologia, superficie):
    try:

        unidad_a_editar = Unidades.objects.get(id = id_unidad)
        unidad_a_editar.orden = numero
        unidad_a_editar.piso_unidad = piso
        unidad_a_editar.nombre_unidad = nombre
        unidad_a_editar.tipologia = tipologia
        unidad_a_editar.sup_equiv = superficie
        unidad_a_editar.save()

        return [1, "Unidad editada correctamente correctamente!"]

    except:

        return [0, "Ocurrio un error inesperado"]

def pricing_actualizar_almacenero(proyecto, ingreso_ventas, unidades_socios, comision):

    almacenero = Almacenero.objects.get(proyecto = proyecto)
    almacenero.ingreso_ventas = ingreso_ventas - ingreso_ventas*0.00
    almacenero.unidades_socios = unidades_socios - unidades_socios*0.00
    almacenero.pendiente_comision = comision
    almacenero.save()

def unidades_calculo_financiacion(unidad, meses, contado, m2_resultante):

    #Aqui calculamos el contado/financiado
        
    values = [0]

    for m in range((meses)):
        values.append(1)

    anticipo = 0.4

    valor_auxiliar = npf.npv(rate=(unidad.proyecto.tasa_f/100), values=values)

    incremento = (meses/(1-anticipo)/(((anticipo/(1-anticipo))*meses)+valor_auxiliar))

    financiado = contado*incremento

    return financiado

def ventas_actualizar_datos(unidad):

    m2_totales = round((unidad.sup_propia + unidad.sup_balcon + unidad.sup_comun + unidad.sup_patio), 2)

    ventas_a_actualizar = VentasRealizadas.objects.filter(unidad = unidad.id)

    for venta in ventas_a_actualizar:

        venta.m2 = m2_totales

        venta.asignacion = unidad.asig

        venta.save()



