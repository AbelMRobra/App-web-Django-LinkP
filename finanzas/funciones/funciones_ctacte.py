import datetime
import numpy as np
from finanzas.models import CuentaCorriente, Cuota, Pago
from dateutil.relativedelta import relativedelta

def ctacte_revision_cuotas(id_cliente):

    cuotas = Cuota.objects.filter(cuenta_corriente__id = id_cliente).order_by("fecha")

    for cuota in cuotas:

        pago_cuota = sum(np.array(Pago.objects.filter(cuota = cuota).values_list("pago")))
        saldo_cuota = cuota.precio - pago_cuota
        saldo_cuota = cuota.precio - pago_cuota

        if cuota.precio != 0 and cuota.pagada == "NO":
            
            if abs(saldo_cuota*cuota.constante.valor) < 50:
                
                cuota.precio = pago_cuota
                cuota.pagada = "SI"
                cuota.save()
                saldo_cuota = 0

def fechas_flujo_excel(id_proyecto):

    fecha_inicial_flujo = Cuota.objects.filter(cuenta_corriente__venta__proyecto__id = id_proyecto).order_by("fecha")[0].fecha
    fecha_final_flujo = Cuota.objects.filter(cuenta_corriente__venta__proyecto__id = id_proyecto).order_by("-fecha")[0].fecha

    fecha_incial_set = datetime.date(fecha_inicial_flujo.year, fecha_inicial_flujo.month, 1)
    fecha_final_set = datetime.date(fecha_final_flujo.year, fecha_final_flujo.month, 1)


    fechas = []

    fecha_auxiiar = fecha_incial_set

    while fecha_auxiiar <= fecha_final_set:
        fechas.append(fecha_auxiiar)
        fecha_auxiiar = fecha_auxiiar + relativedelta(months=1)

    return fechas


