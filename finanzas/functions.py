import datetime
from datetime import date
import pandas as pd
import numpy as np
from .models import Almacenero, CuentaCorriente, Cuota, Pago, RegistroAlmacenero, ArchivosAdmFin, Arqueo, RetirodeSocios, MovimientoAdmin, Honorarios
from proyectos.models import Unidades, Proyectos
from ventas.models import FeaturesUni


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

    fechas = ""
    contador = 0
    contador_year = 1

    while fecha_auxiliar < ultima_fecha:

        if (inicio_pagos.month + contador) == 13:
            
            year = inicio_pagos.year + contador_year
            
            fecha_auxiliar = date(year, 1, 1)

            fechas += str(fecha_auxiliar)+"&"
            
            contador_year += 1

            contador = - (12 - contador)

        else:

            mes = inicio_pagos.month + contador

            year = inicio_pagos.year + contador_year - 1

            fecha_auxiliar = date(year, mes, 1)

            fechas += str(fecha_auxiliar)+"&"

        contador += 1

    if (inicio_pagos.month + contador) == 13:
            
            year = inicio_pagos.year + contador_year
            
            fecha_auxiliar = date(year, 1, 1)

            fechas += str(fecha_auxiliar)+"&"
            
    else:

        mes = inicio_pagos.month + contador

        year = inicio_pagos.year + contador_year - 1

        fecha_auxiliar = date(year, mes, 1)

        fechas += str(fecha_auxiliar)+"&"

    proyecto.fechas_ctas_ctes = fechas
    proyecto.save()

def flujo_ingreso_proyecto(id):

    proyecto = Proyectos.objects.get(id = id)
    flujo_ingreso = ""
    flujo_ingreso_proyecto = ""
    flujo_ingreso_link = ""
    flujo_ingreso_m3 = ""
    flujo_ingreso_proyecto_m3 = ""
    flujo_ingreso_link_m3 = ""
    fecha_inicial = 0
    fechas = proyecto.fechas_ctas_ctes.split("&")
    fechas.pop()
    for f in fechas:
        f = datetime.date(int(f[0:4]), int(f[5:7]), int(f[8:10]))
        if fecha_inicial == 0:
            fecha_inicial = f
        else:
            f = f - datetime.timedelta(days=1)  

            valor_general = 0
            valor_proyecto = 0
            valor_link= 0
            valor_general_m3 = 0
            valor_proyecto_m3 = 0
            valor_link_m3= 0

            asignaciones = ["PROYECTO", "TERRENO", "HON. LINK", "SOCIOS"]

            for asignacion in asignaciones:
                cuotas_mes = sum(np.array(Cuota.objects.values_list('precio', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente__venta__proyecto = proyecto, cuenta_corriente__venta__unidad__asig = asignacion))*np.array(Cuota.objects.values_list('constante__valor', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente__venta__proyecto = proyecto, cuenta_corriente__venta__unidad__asig = asignacion)))
                pagos_mes = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente__venta__proyecto = proyecto, cuota__cuenta_corriente__venta__unidad__asig = asignacion))*np.array(Pago.objects.values_list('cuota__constante__valor', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente__venta__proyecto = proyecto, cuota__cuenta_corriente__venta__unidad__asig = asignacion)))
                ingreso_mes = cuotas_mes - pagos_mes
                valor_general += ingreso_mes
                if asignacion == "TERRENO" or asignacion == "HON. LINK":
                    valor_link += ingreso_mes
                if asignacion == "PROYECTO":
                    valor_proyecto += ingreso_mes

            flujo_ingreso += str(valor_general) + "&"
            flujo_ingreso_proyecto += str(valor_proyecto) + "&"
            flujo_ingreso_link += str(valor_link) + "&"

            for asignacion in asignaciones:
                cuotas_mes = sum(np.array(Cuota.objects.values_list('precio', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente__venta__proyecto = proyecto, cuenta_corriente__venta__unidad__asig = asignacion)))
                pagos_mes = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente__venta__proyecto = proyecto, cuota__cuenta_corriente__venta__unidad__asig = asignacion)))
                ingreso_mes = cuotas_mes - pagos_mes
                valor_general_m3 += ingreso_mes
                if asignacion == "TERRENO" or asignacion == "HON. LINK":
                    valor_link_m3 += ingreso_mes
                if asignacion == "PROYECTO":
                    valor_proyecto_m3 += ingreso_mes

            flujo_ingreso_m3 = flujo_ingreso_m3 + str(valor_general_m3) + "&"
            flujo_ingreso_proyecto_m3  = flujo_ingreso_proyecto_m3 + str(valor_proyecto_m3) + "&"
            flujo_ingreso_link_m3  = flujo_ingreso_link_m3 + str(valor_link_m3) + "&"
            fecha_inicial = f

    proyecto.flujo_ingreso = flujo_ingreso
    proyecto.flujo_ingreso_link = flujo_ingreso_link
    proyecto.flujo_ingreso_proyecto = flujo_ingreso_proyecto
    proyecto.flujo_ingreso_m3 = flujo_ingreso_m3
    proyecto.flujo_ingreso_link_m3 = flujo_ingreso_link_m3
    proyecto.flujo_ingreso_proyecto_m3 = flujo_ingreso_proyecto_m3
    proyecto.save()

def flujo_ingreso_cliente(id):

    cuenta_venta = CuentaCorriente.objects.get(id = id)
    proyecto = Proyectos.objects.get(id = cuenta_venta.venta.unidad.proyecto.id)
    fluejo_ingreso = ""
    fluejo_ingreso_m3 = ""
    fecha_inicial = 0
    fechas = proyecto.fechas_ctas_ctes.split("&")
    fechas.pop()
    for f in fechas:

        f = datetime.date(int(f[0:4]), int(f[5:7]), int(f[8:10]))

        if fecha_inicial == 0:

            fecha_inicial = f

        else:

            f = f - datetime.timedelta(days=1)             
            sum_cuotas_mes = sum(np.array(Cuota.objects.values_list('precio', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta))*np.array(Cuota.objects.values_list('constante__valor', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta)))
            sum_pagos_mes = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta))*np.array(Pago.objects.values_list('cuota__constante__valor', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            sum_pagos_nominales = sum(np.array(Pago.objects.values_list('pago_pesos', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            pagado_o_adeudado = sum_pagos_nominales + (sum_cuotas_mes - sum_pagos_mes)
            fluejo_ingreso = fluejo_ingreso + str(pagado_o_adeudado)+"&"


            sum_cuotas_mes = sum(np.array(Cuota.objects.values_list('precio', flat =True).filter(fecha__range = (fecha_inicial, f), cuenta_corriente = cuenta_venta)))
            sum_pagos_mes = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            sum_pagos_nominales = sum(np.array(Pago.objects.values_list('pago', flat =True).filter(cuota__fecha__range = (fecha_inicial, f), cuota__cuenta_corriente = cuenta_venta)))
            pagado_o_adeudado = sum_pagos_nominales + (sum_cuotas_mes - sum_pagos_mes)
            fluejo_ingreso_m3 = fluejo_ingreso_m3 + str(pagado_o_adeudado)+"&"

            fecha_inicial = f

    cuenta_venta.flujo = fluejo_ingreso
    cuenta_venta.flujo_m3 = fluejo_ingreso_m3
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
                #try:
                contado = m2*proyecto.desde
                features_unidad = FeaturesUni.objects.filter(unidad = u)
                for f2 in features_unidad:
                    contado = contado*f2.feature.inc
                    precio_m2_disponible += contado

                print(m2)
                print(contado)
                print(contado/m2)
                #except:
                    #precio_m2_disponible += 0
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