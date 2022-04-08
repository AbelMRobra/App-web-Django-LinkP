
import datetime
from dateutil.relativedelta import *
from presupuestos.models import Constantes
import pandas as pd
import numpy as np
from django.core.files.base import ContentFile
from datetime import date
from .models import Almacenero, CuentaCorriente, Cuota, Pago, RegistroAlmacenero, ArchivosAdmFin, Arqueo, RetirodeSocios, MovimientoAdmin, Honorarios, RegistroEmail
from proyectos.models import Unidades, Proyectos
from ventas.models import FeaturesUni
from rrhh.models import datosusuario


def validacion_cuotas_pagadas(id_cta_cte):
    ctacte = CuentaCorriente.objects.get(id = id_cta_cte)
    cuotas = Cuota.objects.filter(cuenta_corriente = ctacte)
    pagos = Pago.objects.filter(cuota__cuenta_corriente = ctacte)

    for cuota in cuotas:
        valor_cuota = cuota.precio*cuota.constante.valor
        pagado = sum(pagos.filter(cuota = cuota).values_list('pago', flat=True)*pagos.filter(cuota = cuota).values_list('pago__cuota__constante__valor', flat=True))
        saldo = valor_cuota - pagado

        if  saldo < 5:
            cuota.pagada = 'SI'

        else:
             cuota.pagada = 'NO'   
                
        cuota.save()

def fechas_cc(id):

    proyecto = Proyectos.objects.get(id = id)
    hoy = date.today()

    # Supongamos que existen pagos

    try:
        inicio_pagos = Pago.objects.filter(cuota__cuenta_corriente__venta__proyecto = proyecto).order_by("fecha").values_list("fecha", flat = True)[0]
        inicio_pagos = datetime.date(inicio_pagos.year, inicio_pagos.month, 1)

    except:

        inicio_pagos = date(hoy.year, hoy.month, 1)

    ultima_fecha = Cuota.objects.filter(cuenta_corriente__venta__proyecto = proyecto).order_by("-fecha")[0].fecha
    fecha_auxiliar = inicio_pagos
    
    fechas = []
    
    while fecha_auxiliar < ultima_fecha :
        fechas.append(fecha_auxiliar)
        fecha_auxiliar += relativedelta(months=+1)
    fechas.append(fecha_auxiliar)

    return fechas

def flujo_ingreso_proyecto(id, array):

    consulta_principal_cuotas = Cuota.objects.filter(cuenta_corriente__venta__proyecto__id = id).exclude(cuenta_corriente__estado = "baja")
    consulta_principal_pagos = Pago.objects.filter(cuota__cuenta_corriente__venta__proyecto__id = id).exclude(cuota__cuenta_corriente__estado = "baja")
    precio_hormigon = Constantes.objects.get(id = 7).valor
    data_flujo_proyecto = {}

    array.pop()

    for fecha in array:

        fecha_inicial = fecha - datetime.timedelta(days = 1)
        
        if fecha.month == 12:
            fecha_final = date(fecha.year + 1, 1, 1)
        else:
            fecha_final = date(fecha.year, fecha.month + 1, 1)

        consulta_principal_cuotas_fechas = consulta_principal_cuotas.filter(fecha__range = (fecha_inicial, fecha_final))
        consulta_principal_pagos_fechas = consulta_principal_pagos.filter(cuota__fecha__range = (fecha_inicial, fecha_final))

        key = fecha
        data_flujo_proyecto[key] = {}
        data_flujo_proyecto[key]['PLink'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('cuota__constante__valor', flat =True))) + sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('cuota__constante__valor', flat =True)))
        data_flujo_proyecto[key]['PProyecto'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('cuota__constante__valor', flat =True)))
        data_flujo_proyecto[key]['PTotal'] = sum(np.array(consulta_principal_cuotas_fechas.values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.values_list('cuota__constante__valor', flat =True)))
        data_flujo_proyecto[key]['M3ºLink'] = data_flujo_proyecto[key]['PLink']/precio_hormigon
        data_flujo_proyecto[key]['M3ºProyecto'] = data_flujo_proyecto[key]['PProyecto']/precio_hormigon
        data_flujo_proyecto[key]['M3ºTotal'] = data_flujo_proyecto[key]['PTotal']/precio_hormigon
        data_flujo_proyecto[key]['PLinkb'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('cuota__porc_boleto', flat =True))) + sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('cuota__porc_boleto', flat =True)))
        data_flujo_proyecto[key]['PProyectob'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('cuota__porc_boleto', flat =True)))
        data_flujo_proyecto[key]['PTotalb'] = sum(np.array(consulta_principal_cuotas_fechas.values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.values_list('pago', flat =True)) *np.array(consulta_principal_pagos_fechas.values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.values_list('cuota__porc_boleto', flat =True)))
        data_flujo_proyecto[key]['M3ºLinkb'] = data_flujo_proyecto[key]['PLinkb']/precio_hormigon
        data_flujo_proyecto[key]['M3ºProyectob'] = data_flujo_proyecto[key]['PProyectob']/precio_hormigon
        data_flujo_proyecto[key]['M3ºTotalb'] = data_flujo_proyecto[key]['PTotalb']/precio_hormigon


    consulta_principal_cuotas_fechas = consulta_principal_cuotas
    consulta_principal_pagos_fechas = consulta_principal_pagos

    data_flujo_proyecto_total = {}
    data_flujo_proyecto_total['PLink'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('cuota__constante__valor', flat =True))) + sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('cuota__constante__valor', flat =True)))
    data_flujo_proyecto_total['PProyecto'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('cuota__constante__valor', flat =True)))
    data_flujo_proyecto_total['PTotal'] = sum(np.array(consulta_principal_cuotas_fechas.values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.values_list('constante__valor', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.values_list('cuota__constante__valor', flat =True)))
    data_flujo_proyecto_total['M3ºLink'] = data_flujo_proyecto_total['PLink']/precio_hormigon
    data_flujo_proyecto_total['M3ºProyecto'] = data_flujo_proyecto_total['PProyecto']/precio_hormigon
    data_flujo_proyecto_total['M3ºTotal'] = data_flujo_proyecto_total['PTotal']/precio_hormigon
    data_flujo_proyecto_total['PLinkb'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK").values_list('cuota__porc_boleto', flat =True))) + sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO").values_list('cuota__porc_boleto', flat =True)))
    data_flujo_proyecto_total['PProyectob'] = sum(np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('pago', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO").values_list('cuota__porc_boleto', flat =True)))
    data_flujo_proyecto_total['PTotalb'] = sum(np.array(consulta_principal_cuotas_fechas.values_list('precio', flat =True))*np.array(consulta_principal_cuotas_fechas.values_list('constante__valor', flat =True))*np.array(consulta_principal_cuotas_fechas.values_list('porc_boleto', flat =True))) - sum(np.array(consulta_principal_pagos_fechas.values_list('pago', flat =True)) *np.array(consulta_principal_pagos_fechas.values_list('cuota__constante__valor', flat =True))*np.array(consulta_principal_pagos_fechas.values_list('cuota__porc_boleto', flat =True)))
    data_flujo_proyecto_total['M3ºLinkb'] = data_flujo_proyecto_total['PLinkb']/precio_hormigon
    data_flujo_proyecto_total['M3ºProyectob'] = data_flujo_proyecto_total['PProyectob']/precio_hormigon
    data_flujo_proyecto_total['M3ºTotalb'] = data_flujo_proyecto_total['PTotalb']/precio_hormigon

    return [data_flujo_proyecto, data_flujo_proyecto_total]

def flujo_ingreso_proyecto_cliente(id, array, moneda, boleto, historico):

    con_c = Cuota.objects.filter(cuenta_corriente__venta__proyecto__id = id).exclude(cuenta_corriente__estado = "baja")
    con_p = Pago.objects.filter(cuota__cuenta_corriente__venta__proyecto__id = id).exclude(cuota__cuenta_corriente__estado = "baja")
    cuentas_corrientes = CuentaCorriente.objects.filter(venta__proyecto__id = id).exclude(cuota__cuenta_corriente__estado = "baja")
    precio_hormigon = Constantes.objects.get(id = 7).valor

    array.pop()

    ###### Lo pendiente / moroso

    if moneda == "0" and boleto == "0" and historico == "0":

        mensaje = "Tu consulta esta lista!, Pendiente en moneda: ARS - boleto: No activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("constante__valor", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))
            ))) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [((sum(
            np.array(con_c.filter(cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter(cuenta_corriente = cuenta).values_list("constante__valor", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))
            ))) 
            
            for cuenta in cuentas_corrientes]
        
    elif  moneda == "1" and boleto == "0" and historico == "0":

        mensaje = "Tu consulta esta lista!, moneda: Pendiente en Hormigón - boleto: No activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("constante__valor", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True)))
            )/precio_hormigon) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [(
            sum(
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("constante__valor", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True)))
            )/precio_hormigon for cuenta in cuentas_corrientes]

    elif  moneda == "0" and boleto == "1" and historico == "0":

        mensaje = "Tu consulta esta lista!, Pendiente en moneda: ARS - boleto: Activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("constante__valor", flat = True))*
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("porc_boleto", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            )) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [(
            sum(
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("constante__valor", flat = True))*
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("porc_boleto", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            ) for cuenta in cuentas_corrientes]

    elif  moneda == "1" and boleto == "1" and historico == "0":

        mensaje = "Tu consulta esta lista!, Pendiente en moneda: Hormigón - boleto: Activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("constante__valor", flat = True))*
            np.array(con_c.filter(fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuenta_corriente = cuenta).values_list("porc_boleto", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            )/precio_hormigon) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [(
            sum(
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("precio", flat = True))*
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("constante__valor", flat = True))*
            np.array(con_c.filter( cuenta_corriente = cuenta).values_list("porc_boleto", flat = True))
            ) - sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            )/precio_hormigon for cuenta in cuentas_corrientes]

    ###### Lo historico

    elif moneda == "0" and boleto == "0" and historico == "1":

        mensaje = "Tu consulta esta lista!, Historico en moneda: ARS - boleto: No activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago_pesos", flat = True))
            ))) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [((
            sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago_pesos", flat = True))
            ))) 
            
            for cuenta in cuentas_corrientes]
        
    elif  moneda == "1" and boleto == "0" and historico == "1":

        mensaje = "Tu consulta esta lista!, Historico en moneda: Hormigón - boleto: No activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True)))
            )/precio_hormigon) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [(
            sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True)))
            )/precio_hormigon for cuenta in cuentas_corrientes]

    elif  moneda == "0" and boleto == "1" and historico == "1":

        mensaje = "Tu consulta esta lista!, Historico en moneda: ARS - boleto: Activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago_pesos", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            )) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [(
            sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago_pesos", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            ) for cuenta in cuentas_corrientes]

    elif  moneda == "1" and boleto == "1" and historico == "1":

        mensaje = "Tu consulta esta lista!, Historico en moneda: Hormigón - boleto: Activado"

        data_flujo_proyecto = {fecha:  [(cuenta, (
            sum(
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))*
            np.array(con_p.filter(cuota__fecha__range = ((fecha - datetime.timedelta(days = 1)), fecha + relativedelta(months=+1)), cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            )/precio_hormigon) for cuenta in cuentas_corrientes]
        
        for fecha in array}

        flujo_total = [(
            sum(
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("pago", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__constante__valor", flat = True))*
            np.array(con_p.filter(cuota__cuenta_corriente = cuenta).values_list("cuota__porc_boleto", flat = True)))
            )/precio_hormigon for cuenta in cuentas_corrientes]


    return [data_flujo_proyecto, cuentas_corrientes, flujo_total, mensaje]

def flujo_ingreso_cliente(id):

    cuenta_venta = CuentaCorriente.objects.get(id = id)
    proyecto = Proyectos.objects.get(id = cuenta_venta.venta.unidad.proyecto.id)
    fluejo_ingreso = ""
    fluejo_ingreso_m3 = ""
    flujo_ingreso_boleto =""
    fluejo_ingreso_boleto_m3 = ""
    fecha_inicial = 0
    fechas = proyecto.fechas_ctas_ctes.split("&")
    fechas.pop()
    for f in fechas:

        f = datetime.date(int(f[0:4]), int(f[5:7]), int(f[8:10]))

        if fecha_inicial == 0:

            fecha_inicial = f

        else:

            f = f - datetime.timedelta(days=1)

            # Parte pesos -> Abel             
            sum_cuotas_mes = sum(np.array(Cuota.objects.values_list('precio', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta))*np.array(Cuota.objects.values_list('constante__valor', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta)))
            sum_pagos_mes = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))*np.array(Pago.objects.values_list('cuota__constante__valor', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            sum_pagos_nominales = sum(np.array(Pago.objects.values_list('pago_pesos', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            pagado_o_adeudado = sum_pagos_nominales + (sum_cuotas_mes - sum_pagos_mes)
            fluejo_ingreso = fluejo_ingreso + str(pagado_o_adeudado)+"&"

            # Parte M3 -> Abel
            sum_cuotas_mes = sum(np.array(Cuota.objects.values_list('precio', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta)))
            sum_pagos_mes = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            sum_pagos_nominales = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            pagado_o_adeudado = sum_pagos_nominales + (sum_cuotas_mes - sum_pagos_mes)
            fluejo_ingreso_m3 = fluejo_ingreso_m3 + str(pagado_o_adeudado)+"&"

            # Parte de boleto pesos -> Flor

            vector_cuotas_mes=np.array(Cuota.objects.values_list('precio', flat =True).filter(boleto="BOLETO",fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta))
            vector_constantes_mes=np.array(Cuota.objects.values_list('constante__valor', flat =True).filter(boleto="BOLETO",fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta))
            vector_boletos_mes=np.array(Cuota.objects.values_list('porc_boleto', flat =True).filter(boleto="BOLETO",fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta))
            total_cuotas_boletos_mes=sum(vector_cuotas_mes*vector_constantes_mes*vector_boletos_mes)
            vector_pagos_boleto=np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__boleto="BOLETO", cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))
            vector_constante_pagos=np.array(Pago.objects.values_list('cuota__constante__valor', flat =True).filter(cuota__boleto="BOLETO", cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))
            vector_constante_pagos_porc=np.array(Pago.objects.values_list('cuota__porc_boleto', flat =True).filter(cuota__boleto="BOLETO", cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))
            sum_pagos_boleto_mes=sum(vector_pagos_boleto*vector_constante_pagos*vector_constante_pagos_porc)
            sum_pagos_nominales_boletos = sum(np.array(Pago.objects.values_list('pago_pesos', flat =True).filter(cuota__boleto="BOLETO",cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))*np.array(Pago.objects.values_list('cuota__porc_boleto', flat =True).filter(cuota__boleto="BOLETO",cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            pagado_o_adeudado = sum_pagos_nominales_boletos + (total_cuotas_boletos_mes - sum_pagos_boleto_mes)
            flujo_ingreso_boleto = flujo_ingreso_boleto + str(pagado_o_adeudado)+"&"
            
            # Parte de boleto M3 -> Abel
            sum_cuotas_mes = sum(np.array(Cuota.objects.values_list('precio', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta))*np.array(Cuota.objects.values_list('porc_boleto', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta)))
            sum_pagos_mes = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))*np.array(Pago.objects.values_list('cuota__porc_boleto', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            sum_pagos_nominales = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))*np.array(Pago.objects.values_list('cuota__porc_boleto', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            pagado_o_adeudado = sum_pagos_nominales + (sum_cuotas_mes - sum_pagos_mes)
            fluejo_ingreso_boleto_m3 = fluejo_ingreso_boleto_m3 + str(pagado_o_adeudado)+"&"

            f = f + datetime.timedelta(days=1)

            fecha_inicial = f

    cuenta_venta.flujo = fluejo_ingreso
    cuenta_venta.flujo_m3 = fluejo_ingreso_m3
    cuenta_venta.flujo_boleto = flujo_ingreso_boleto
    cuenta_venta.flujo_boleto_m3 = fluejo_ingreso_boleto_m3
    cuenta_venta.save()

def promedio_almacenero(almacenero):
    proyecto = Proyectos.objects.get(id = almacenero.proyecto.id)
    m2_total = 0
    m2_disponible = 0
    precio_m2_disponible = 0
    try:
        unidades = Unidades.objects.filter(proyecto = proyecto)

        for u in unidades:
            m2 = 0
            if u.sup_equiv > 0:
                m2 = round(u.sup_equiv, 2)
            else:
                m2 = round((u.sup_propia + u.sup_balcon + u.sup_comun + u.sup_patio), 2)
            m2_total += m2
            if u.estado == "DISPONIBLE":
                m2_disponible += m2
                try:
                    contado = m2*proyecto.desde
                    features_unidad = FeaturesUni.objects.filter(unidad = u)
                    for f2 in features_unidad:
                        contado = contado*f2.feature.inc
                    precio_m2_disponible += contado
                except:
                    precio_m2_disponible += 0
        porc_dispo = 0

        if m2_disponible != 0:
            precio_m2_disponible = precio_m2_disponible/m2_disponible
        else:
            precio_m2_disponible = 0
    except:
        porc_dispo = 0
        precio_m2_disponible = 0

    data_proyecto = [almacenero, porc_dispo, precio_m2_disponible]
    return data_proyecto

def registroemail(id_cuenta, fecha, usuario, archivo):
    try:
        registro=RegistroEmail(
            usuario=datosusuario.objects.get(identificacion=usuario.username),
            destino=CuentaCorriente.objects.get(pk=id_cuenta),
            fecha=fecha,

        )
        registro.estado_cuenta.save('archivo.pdf', ContentFile(archivo))
        registro.save()
        mensaje='Ok'
        
    except:
        mensaje='error'

def resumen_cuentas(id_proyecto):

    context_data = {}
    context_data["context_data_total"] = {}
    context_data["context_data_proyecto"] = {}
    context_data["context_data_link"] = {}
    context_data["context_data_terreno"] = {}

    context_data["boleto_context_data_total"] = {}
    context_data["boleto_context_data_proyecto"] = {}
    context_data["boleto_context_data_link"] = {}
    context_data["boleto_context_data_terreno"] = {}



    proyecto = Proyectos.objects.get(id = int(id_proyecto))
    precio_hormigon = Constantes.objects.get(id = 7).valor

    hoy = datetime.date.today()

    # ESTAS SON TODAS LAS CONSULTAS NECESARIAS

    cuota_consulta_p = Cuota.objects.filter(fecha__lt = hoy, cuenta_corriente__venta__proyecto = proyecto).exclude(cuenta_corriente__estado = "baja")
    pago_consulta_p = Pago.objects.filter(cuota__fecha__lt = hoy, cuota__cuenta_corriente__venta__proyecto = proyecto).exclude(cuota__cuenta_corriente__estado = "baja")
    cuota_consulta_f = Cuota.objects.filter(fecha__gte = hoy, cuenta_corriente__venta__proyecto = proyecto).exclude(cuenta_corriente__estado = "baja")
    pago_consulta_f = Pago.objects.filter(cuota__fecha__gte = hoy, cuota__cuenta_corriente__venta__proyecto = proyecto).exclude(cuota__cuenta_corriente__estado = "baja")
    pago_p_consulta_p = Pago.objects.filter(cuota__fecha__lt = hoy, cuota__cuenta_corriente__venta__proyecto = proyecto).exclude(cuota__cuenta_corriente__estado = "baja")


    ####### ESTE PUNTO ES TOTAL

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p.values_list('precio', flat=True))*np.array(cuota_consulta_p.values_list('constante__valor', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p.values_list('pago', flat=True))*np.array(pago_consulta_p.values_list('cuota__constante__valor', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p.values_list('pago_pesos', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f.values_list('precio', flat=True))*np.array(cuota_consulta_f.values_list('constante__valor', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f.values_list('pago', flat=True))*np.array(pago_consulta_f.values_list('cuota__constante__valor', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["context_data_total"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["context_data_total"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["context_data_total"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["context_data_total"]["pesos_mora"] = mora
    context_data["context_data_total"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["context_data_total"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["context_data_total"]["pesos_deuda"] = deuda_final
    context_data["context_data_total"]["m3_cobrado"] = (cuotas_hasta_hoy + deuda_final)/precio_hormigon
    context_data["context_data_total"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["context_data_total"]["m3_mora"] = mora/precio_hormigon
    context_data["context_data_total"]["m3_deuda"] = deuda_final/precio_hormigon

    context_data["context_data_total"]["m3_adelantado"] = pagos_desde_hoy/precio_hormigon

    ####### ESTE PUNTO ES PROYECTO

    cuota_consulta_p_proy = cuota_consulta_p.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO")
    pago_consulta_p_proy = pago_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO")
    cuota_consulta_f_proy = cuota_consulta_f.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO")
    pago_consulta_f_proy = pago_consulta_f.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO")
    pago_p_consulta_p_proy = pago_p_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO")

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p_proy.values_list('precio', flat=True))*np.array(cuota_consulta_p_proy.values_list('constante__valor', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p_proy.values_list('pago', flat=True))*np.array(pago_consulta_p_proy.values_list('cuota__constante__valor', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p_proy.values_list('pago_pesos', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f_proy.values_list('precio', flat=True))*np.array(cuota_consulta_f_proy.values_list('constante__valor', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f_proy.values_list('pago', flat=True))*np.array(pago_consulta_f_proy.values_list('cuota__constante__valor', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["context_data_proyecto"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["context_data_proyecto"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["context_data_proyecto"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["context_data_proyecto"]["pesos_mora"] = mora
    context_data["context_data_proyecto"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["context_data_proyecto"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["context_data_proyecto"]["pesos_deuda"] = deuda_final
    context_data["context_data_proyecto"]["m3_cobrado"] = (cuotas_hasta_hoy + deuda_final)/precio_hormigon
    context_data["context_data_proyecto"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["context_data_proyecto"]["m3_mora"] = mora/precio_hormigon
    context_data["context_data_proyecto"]["m3_deuda"] = deuda_final/precio_hormigon

    ####### ESTE PUNTO ES LINK

    cuota_consulta_p_link = cuota_consulta_p.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK")
    pago_consulta_p_link = pago_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK")
    cuota_consulta_f_link = cuota_consulta_f.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK")
    pago_consulta_f_link = pago_consulta_f.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK")
    pago_p_consulta_p_link = pago_p_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK")

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p_link.values_list('precio', flat=True))*np.array(cuota_consulta_p_link.values_list('constante__valor', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p_link.values_list('pago', flat=True))*np.array(pago_consulta_p_link.values_list('cuota__constante__valor', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p_link.values_list('pago_pesos', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f_link.values_list('precio', flat=True))*np.array(cuota_consulta_f_link.values_list('constante__valor', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f_link.values_list('pago', flat=True))*np.array(pago_consulta_f_link.values_list('cuota__constante__valor', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["context_data_link"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["context_data_link"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["context_data_link"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["context_data_link"]["pesos_mora"] = mora
    context_data["context_data_link"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["context_data_link"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["context_data_link"]["pesos_deuda"] = deuda_final
    context_data["context_data_link"]["m3_cobrado"] = (cuotas_hasta_hoy + deuda_final)/precio_hormigon
    context_data["context_data_link"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["context_data_link"]["m3_mora"] = mora/precio_hormigon
    context_data["context_data_link"]["m3_deuda"] = deuda_final/precio_hormigon

    ####### ESTE PUNTO ES TERRENO

    cuota_consulta_p_terreno = cuota_consulta_p.filter(cuenta_corriente__venta__unidad__asig = "TERRENO")
    pago_consulta_p_terreno = pago_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO")
    cuota_consulta_f_terreno = cuota_consulta_f.filter(cuenta_corriente__venta__unidad__asig = "TERRENO")
    pago_consulta_f_terreno = pago_consulta_f.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO")
    pago_p_consulta_p_terreno = pago_p_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO")

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p_terreno.values_list('precio', flat=True))*np.array(cuota_consulta_p_terreno.values_list('constante__valor', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p_terreno.values_list('pago', flat=True))*np.array(pago_consulta_p_terreno.values_list('cuota__constante__valor', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p_terreno.values_list('pago_pesos', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f_terreno.values_list('precio', flat=True))*np.array(cuota_consulta_f_terreno.values_list('constante__valor', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f_terreno.values_list('pago', flat=True))*np.array(pago_consulta_f_terreno.values_list('cuota__constante__valor', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["context_data_terreno"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["context_data_terreno"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["context_data_terreno"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["context_data_terreno"]["pesos_mora"] = mora
    context_data["context_data_terreno"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["context_data_terreno"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["context_data_terreno"]["pesos_deuda"] = deuda_final
    context_data["context_data_terreno"]["m3_cobrado"] = (cuotas_hasta_hoy + deuda_final)/precio_hormigon
    context_data["context_data_terreno"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["context_data_terreno"]["m3_mora"] = mora/precio_hormigon
    context_data["context_data_terreno"]["m3_deuda"] = deuda_final/precio_hormigon


    ##############
    #  BOLETO
    ##############


    ####### ESTE PUNTO ES TOTAL

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p.values_list('precio', flat=True))*np.array(cuota_consulta_p.values_list('constante__valor', flat=True))*np.array(cuota_consulta_p.values_list('porc_boleto', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p.values_list('pago', flat=True))*np.array(pago_consulta_p.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_p.values_list('cuota__porc_boleto', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p.values_list('pago_pesos', flat=True))*np.array(pago_p_consulta_p.values_list('cuota__porc_boleto', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f.values_list('precio', flat=True))*np.array(cuota_consulta_f.values_list('constante__valor', flat=True))*np.array(cuota_consulta_f.values_list('porc_boleto', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f.values_list('pago', flat=True))*np.array(pago_consulta_f.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_f.values_list('cuota__porc_boleto', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["boleto_context_data_total"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["boleto_context_data_total"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["boleto_context_data_total"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["boleto_context_data_total"]["pesos_mora"] = mora
    context_data["boleto_context_data_total"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["boleto_context_data_total"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["boleto_context_data_total"]["pesos_deuda"] = deuda_final
    context_data["boleto_context_data_total"]["m3_cobrado"] = (cuotas_hasta_hoy + deuda_final)/precio_hormigon
    context_data["boleto_context_data_total"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["boleto_context_data_total"]["m3_mora"] = mora/precio_hormigon
    context_data["boleto_context_data_total"]["m3_deuda"] = deuda_final/precio_hormigon

    ####### ESTE PUNTO ES PROYECTO

    cuota_consulta_p_proy = cuota_consulta_p.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO")
    pago_consulta_p_proy = pago_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO")
    cuota_consulta_f_proy = cuota_consulta_f.filter(cuenta_corriente__venta__unidad__asig = "PROYECTO")
    pago_consulta_f_proy = pago_consulta_f.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO")
    pago_p_consulta_p_proy = pago_p_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "PROYECTO")

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p_proy.values_list('precio', flat=True))*np.array(cuota_consulta_p_proy.values_list('constante__valor', flat=True))*np.array(cuota_consulta_p_proy.values_list('porc_boleto', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p_proy.values_list('pago', flat=True))*np.array(pago_consulta_p_proy.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_p_proy.values_list('cuota__porc_boleto', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p_proy.values_list('pago_pesos', flat=True))*np.array(pago_p_consulta_p_proy.values_list('cuota__porc_boleto', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f_proy.values_list('precio', flat=True))*np.array(cuota_consulta_f_proy.values_list('constante__valor', flat=True))*np.array(cuota_consulta_f_proy.values_list('porc_boleto', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f_proy.values_list('pago', flat=True))*np.array(pago_consulta_f_proy.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_f_proy.values_list('cuota__porc_boleto', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["boleto_context_data_proyecto"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["boleto_context_data_proyecto"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["boleto_context_data_proyecto"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["boleto_context_data_proyecto"]["pesos_mora"] = mora
    context_data["boleto_context_data_proyecto"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["boleto_context_data_proyecto"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["boleto_context_data_proyecto"]["pesos_deuda"] = deuda_final
    context_data["boleto_context_data_proyecto"]["m3_cobrado"] = (cuotas_hasta_hoy + deuda_final)/precio_hormigon
    context_data["boleto_context_data_proyecto"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["boleto_context_data_proyecto"]["m3_mora"] = mora/precio_hormigon
    context_data["boleto_context_data_proyecto"]["m3_deuda"] = deuda_final/precio_hormigon

    ####### ESTE PUNTO ES LINK

    cuota_consulta_p_link = cuota_consulta_p.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK")
    pago_consulta_p_link = pago_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK")
    cuota_consulta_f_link = cuota_consulta_f.filter(cuenta_corriente__venta__unidad__asig = "HON. LINK")
    pago_consulta_f_link = pago_consulta_f.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK")
    pago_p_consulta_p_link = pago_p_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "HON. LINK")

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p_link.values_list('precio', flat=True))*np.array(cuota_consulta_p_link.values_list('constante__valor', flat=True))*np.array(cuota_consulta_p_link.values_list('porc_boleto', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p_link.values_list('pago', flat=True))*np.array(pago_consulta_p_link.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_p_link.values_list('cuota__porc_boleto', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p_link.values_list('pago_pesos', flat=True))*np.array(pago_p_consulta_p_link.values_list('cuota__porc_boleto', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f_link.values_list('precio', flat=True))*np.array(cuota_consulta_f_link.values_list('constante__valor', flat=True))*np.array(cuota_consulta_f_link.values_list('porc_boleto', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f_link.values_list('pago', flat=True))*np.array(pago_consulta_f_link.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_f_link.values_list('cuota__porc_boleto', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["boleto_context_data_link"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["boleto_context_data_link"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["boleto_context_data_link"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["boleto_context_data_link"]["pesos_mora"] = mora
    context_data["boleto_context_data_link"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["boleto_context_data_link"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["boleto_context_data_link"]["pesos_deuda"] = deuda_final
    context_data["boleto_context_data_link"]["m3_cobrado"] = (cuotas_hasta_hoy  + deuda_final)/precio_hormigon
    context_data["boleto_context_data_link"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["boleto_context_data_link"]["m3_mora"] = mora/precio_hormigon
    context_data["boleto_context_data_link"]["m3_deuda"] = deuda_final/precio_hormigon

    ####### ESTE PUNTO ES TERRENO

    cuota_consulta_p_terreno = cuota_consulta_p.filter(cuenta_corriente__venta__unidad__asig = "TERRENO")
    pago_consulta_p_terreno = pago_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO")
    cuota_consulta_f_terreno = cuota_consulta_f.filter(cuenta_corriente__venta__unidad__asig = "TERRENO")
    pago_consulta_f_terreno = pago_consulta_f.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO")
    pago_p_consulta_p_terreno = pago_p_consulta_p.filter(cuota__cuenta_corriente__venta__unidad__asig = "TERRENO")

    cuotas_hasta_hoy = sum(np.array(cuota_consulta_p_terreno.values_list('precio', flat=True))*np.array(cuota_consulta_p_terreno.values_list('constante__valor', flat=True))*np.array(cuota_consulta_p_terreno.values_list('porc_boleto', flat=True)))
    pagos_hasta_hoy = sum(np.array(pago_consulta_p_terreno.values_list('pago', flat=True))*np.array(pago_consulta_p_terreno.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_p_terreno.values_list('cuota__porc_boleto', flat=True)))
    pagos_hasta_hoy_historico = sum(np.array(pago_p_consulta_p_terreno.values_list('pago_pesos', flat=True))*np.array(pago_p_consulta_p_terreno.values_list('cuota__porc_boleto', flat=True)))
    mora = cuotas_hasta_hoy - pagos_hasta_hoy

    # En este punto todo esta en pesos a futuro

    cuotas_desde_hoy = sum(np.array(cuota_consulta_f_terreno.values_list('precio', flat=True))*np.array(cuota_consulta_f_terreno.values_list('constante__valor', flat=True))*np.array(cuota_consulta_f_terreno.values_list('porc_boleto', flat=True)))
    pagos_desde_hoy = sum(np.array(pago_consulta_f_terreno.values_list('pago', flat=True))*np.array(pago_consulta_f_terreno.values_list('cuota__constante__valor', flat=True))*np.array(pago_consulta_f_terreno.values_list('cuota__porc_boleto', flat=True)))
    deuda_final = cuotas_desde_hoy - pagos_desde_hoy
    
    context_data["boleto_context_data_terreno"]["pesos_cobrado"] = (pagos_hasta_hoy_historico + mora + deuda_final)
    context_data["boleto_context_data_terreno"]["pesos_pagado"] = pagos_hasta_hoy
    context_data["boleto_context_data_terreno"]["pesos_pagado_historico"] = pagos_hasta_hoy_historico
    context_data["boleto_context_data_terreno"]["pesos_mora"] = mora
    context_data["boleto_context_data_terreno"]["pesos_pendiente"] = cuotas_desde_hoy
    context_data["boleto_context_data_terreno"]["pesos_adelantado"] = pagos_desde_hoy
    context_data["boleto_context_data_terreno"]["pesos_deuda"] = deuda_final
    context_data["boleto_context_data_terreno"]["m3_cobrado"] = (cuotas_hasta_hoy + deuda_final)/precio_hormigon
    context_data["boleto_context_data_terreno"]["m3_pagado"] = pagos_hasta_hoy/precio_hormigon
    context_data["boleto_context_data_terreno"]["m3_mora"] = mora/precio_hormigon
    context_data["boleto_context_data_terreno"]["m3_deuda"] = deuda_final/precio_hormigon


    ######## BUSCADOR DE CUENTAS INDIVIDUALES

    data = CuentaCorriente.objects.filter(venta__proyecto = proyecto).exclude(estado = "baja")

    fecha_inicial_hoy = datetime.date.today()

    datos = []

    consulta_pagos_pasados = Pago.objects.filter(cuota__fecha__lt = fecha_inicial_hoy, cuota__cuenta_corriente__venta__proyecto = proyecto).exclude(cuota__cuenta_corriente__estado = "baja")
    consulta_cuotas_anteriores = Cuota.objects.filter(fecha__lt = fecha_inicial_hoy, cuenta_corriente__venta__proyecto = proyecto).exclude(cuenta_corriente__estado = "baja")
    consulta_pagos_anteriores = Pago.objects.filter(cuota__fecha__lt = fecha_inicial_hoy, cuota__cuenta_corriente__venta__proyecto = proyecto).exclude(cuota__cuenta_corriente__estado = "baja")
    consulta_cuotas_posteriores = Cuota.objects.filter(fecha__gte = fecha_inicial_hoy, cuenta_corriente__venta__proyecto = proyecto).exclude(cuenta_corriente__estado = "baja")
    consulta_pagos_adelantos = Pago.objects.filter(cuota__fecha__gte = fecha_inicial_hoy, cuota__cuenta_corriente__venta__proyecto = proyecto).exclude(cuota__cuenta_corriente__estado = "baja")

    for c in data:

        pagos = sum(np.array(consulta_pagos_pasados.filter(cuota__cuenta_corriente = c).values_list('pago_pesos', flat=True)))
        
        cuotas_anteriores = sum(np.array(consulta_cuotas_anteriores.filter(cuenta_corriente = c).values_list('precio', flat=True))*np.array(consulta_cuotas_anteriores.filter(cuenta_corriente = c).values_list('constante__valor', flat=True)))
        pagos_anteriores = sum(np.array(consulta_pagos_anteriores.filter(cuota__cuenta_corriente = c).values_list('pago', flat=True))*np.array(consulta_pagos_anteriores.filter(cuota__cuenta_corriente = c).values_list('cuota__constante__valor', flat=True)))
        cuotas_posteriores = sum(np.array(consulta_cuotas_posteriores.filter(cuenta_corriente = c).values_list('precio', flat=True))*np.array(consulta_cuotas_posteriores.filter(cuenta_corriente = c).values_list('constante__valor', flat=True)))
        adelantos = sum(np.array(consulta_pagos_adelantos.filter(cuota__cuenta_corriente = c).values_list('pago', flat=True))*np.array(consulta_pagos_adelantos.filter(cuota__cuenta_corriente = c).values_list('cuota__constante__valor', flat=True)))
        
        pagos_m3 = pagos_anteriores/precio_hormigon
        adeudado = cuotas_anteriores - pagos_anteriores
        pendiente = cuotas_posteriores - adelantos
        
        datos.append((c, pagos, adeudado, pendiente, pagos_m3, adeudado/precio_hormigon, pendiente/precio_hormigon))

    pagos = sum(np.array(consulta_pagos_pasados.values_list('pago_pesos', flat=True)))
        
    cuotas_anteriores = sum(np.array(consulta_cuotas_anteriores.values_list('precio', flat=True))*np.array(consulta_cuotas_anteriores.values_list('constante__valor', flat=True)))
    pagos_anteriores = sum(np.array(consulta_pagos_anteriores.values_list('pago', flat=True))*np.array(consulta_pagos_anteriores.values_list('cuota__constante__valor', flat=True)))
    cuotas_posteriores = sum(np.array(consulta_cuotas_posteriores.values_list('precio', flat=True))*np.array(consulta_cuotas_posteriores.values_list('constante__valor', flat=True)))
    adelantos = sum(np.array(consulta_pagos_adelantos.values_list('pago', flat=True))*np.array(consulta_pagos_adelantos.values_list('cuota__constante__valor', flat=True)))
    
    pagos_m3 = pagos_anteriores/precio_hormigon
    adeudado = cuotas_anteriores - pagos_anteriores
    pendiente = cuotas_posteriores - adelantos
    
    datos_total = (c, pagos, adeudado, pendiente, pagos_m3, adeudado/precio_hormigon, pendiente/precio_hormigon)

    context_data["context_buscador"] = datos
    context_data["context_buscador_total"] = datos_total
    

    return context_data