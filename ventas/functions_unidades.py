from .models import Clientescontacto
from presupuestos.models import Constantes
import numpy_financial as npf

def calculo_m2_unidad(unidad):

    if unidad.sup_equiv > 0:

        m2 = unidad.sup_equiv

    else:

        m2 = unidad.sup_propia + unidad.sup_balcon + unidad.sup_comun + unidad.sup_patio

    return m2

def cliente_crm(email, **kwargs):

    if len(Clientescontacto.objects.filter( email = email)) > 0:
        
        cliente = Clientescontacto.objects.get(email = email)
    
    else:
        try:
            cliente = Clientescontacto(

                nombre = kwargs.nombre,
                apellido = kwargs.apellido,
                email = email
            )

            cliente.save()
            
            if kwargs.telefono:
                cliente.telefono = kwargs.telefono
                cliente.save()

        except:

            cliente = 0

    return cliente

def plan_financiacion_cotizador(anticipo, cuota_esp, aporte, cuotas_p, observacion, descuento, precio_contado, unidad):

    cuota_esp = int(cuota_esp)
    cuotas_p = int(cuotas_p)
    aporte = int(aporte)
    descuento = float(descuento)
    anticipo = float(anticipo)
    precio_contado = float(precio_contado)

    # No puede no tener tasa de financiación el proyecto
    # No puede ser el descuento mayor a 1

    hormigon = Constantes.objects.get(id = 7)
    anticipo_h = float(anticipo)/hormigon.valor
    total_cuotas = float(cuota_esp) + float(cuotas_p)*1.65 + float(aporte)

    if anticipo > precio_contado:

        anticipo = precio_contado
        anticipo_h = anticipo/hormigon.valor
        precio_finan = precio_contado
        importe_aporte = 0
        importe_cuota_esp = 0
        importe_cuota_p = 0 
        importe_cuota_p_h = 0 
        importe_cuota_esp_h = 0 
        importe_aporte_h = 0 
        valor_cuota_espera = 0
        valor_cuota_entrega = 0
        valor_cuota_pose = 0
        total_pesos = 0
        total_hormigon = 0


    elif cuota_esp == 0 and aporte == 0 and cuotas_p == 0:
        anticipo = precio_contado
        anticipo_h = anticipo/hormigon.valor
        precio_finan = precio_contado
        importe_aporte = 0
        importe_cuota_esp = 0
        importe_cuota_p = 0 
        importe_cuota_p_h = 0 
        importe_cuota_esp_h = 0 
        importe_aporte_h = 0 
        valor_cuota_espera = 0
        valor_cuota_entrega = 0
        valor_cuota_pose = 0
        total_pesos = 0
        total_hormigon = 0



    else:

        ###### Calculo del valor presente de la parte de espera

        if cuota_esp > 0:

            cuotas_espera = []
            cuotas_espera.append(0)

            for i in range(int(cuota_esp)):                
                    cuotas_espera.append(1)

            valor_presente_espera = npf.npv(rate=(unidad.proyecto.tasa_f/100), values=cuotas_espera)

        else:

            valor_presente_espera = 0

        ###### Calculo del valor presente de la parte de posesión

        if cuotas_p > 0:

            cuotas_pose = []
            cuotas_pose.append(0)

            if cuota_esp > 0:

                for i in range(int(cuota_esp)):                
                    cuotas_pose.append(0)

            for d in range(int(cuotas_p)):
                cuotas_pose.append(1.65)

            valor_presente_posesion = npf.npv(rate=(unidad.proyecto.tasa_f/100), values=cuotas_pose)

        else:
            valor_presente_posesion = 0


        ###### Calculo del valor presente del aporte del dia de la entrega

        if aporte > 0:

            aporte_va = []
            aporte_va.append(0)

            if cuota_esp > 0:

                for i in range(int(cuota_esp)):
                    aporte_va.append(0)

            aporte_va.pop()
            aporte_va.append(int(aporte))

            valor_presente_aporte = npf.npv(rate=(unidad.proyecto.tasa_f/100), values=aporte_va)

        else:

            valor_presente_aporte = 0

        ############ Hasta aqui tengo todos los valores presentes de las 3 secciones de pago

        precio_contado = precio_contado*(1 - descuento)
        
        if valor_presente_espera == 0 and valor_presente_aporte == 0 and valor_presente_posesion == 0:
            incremento = 0
        else:

            factor = valor_presente_aporte + valor_presente_espera + valor_presente_posesion
            incremento = (total_cuotas/factor) - 1


        precio_finan = ((precio_contado - float(anticipo))*(1 + incremento)) + float(anticipo)

        aux_calculo = (precio_finan-float(anticipo))/total_cuotas

        # Calculo del importa de la cuota espera

        if cuota_esp > 0:

            importe_cuota_esp = aux_calculo*cuota_esp

        else:

            importe_cuota_esp = 0

        # Calculo del aporte

        if aporte > 0:

            importe_aporte = aux_calculo*float(aporte)*aporte

        else:

            importe_aporte = 0

        # Calculo del importa de la cuota posesion

        if int(cuotas_p) > 0:

            importe_cuota_p = aux_calculo*1.65*cuotas_p

        else:

            importe_cuota_p = 0

        
        # Pasamos a hormigon los calculos

        importe_cuota_p_h = importe_cuota_p/hormigon.valor
        importe_aporte_h = importe_aporte/hormigon.valor
        importe_cuota_esp_h = importe_cuota_esp/hormigon.valor

        # Calculamos las cuotas

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

        # Hacemos una ultima validación

    total_pesos = importe_aporte + importe_cuota_esp + importe_cuota_p + anticipo
    total_hormigon = importe_aporte_h + importe_cuota_esp_h + importe_cuota_p_h + anticipo_h

    return [anticipo, anticipo_h, precio_finan, cuota_esp, importe_aporte, cuotas_p, importe_cuota_esp,
            aporte, importe_cuota_p, importe_cuota_p_h, importe_cuota_esp_h, importe_aporte_h, valor_cuota_espera,
            valor_cuota_entrega, valor_cuota_pose, observacion, descuento, total_pesos, total_hormigon, precio_contado]


def info_para_cotizador(array):

    return str(array[3])+"&"+str(array[7])+"&"+str(array[5])+"&"+str(array[0])+"&"+str(array[16])+"&"+str(array[15])