import numpy as np
import numpy_financial as npf

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

    datos_coti = [anticipo, anticipo_h, precio_finan, cuota_esp, importe_aporte, cuotas_p, importe_cuota_esp, aporte, importe_cuota_p, importe_cuota_p_h, importe_cuota_esp_h, importe_aporte_h, valor_cuota_espera, valor_cuota_entrega, valor_cuota_pose]
    return datos_coti