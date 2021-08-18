import datetime
from datetime import date
import pandas as pd
import numpy as np
import random


from django.shortcuts import render,redirect
from presupuestos.models import Proyectos, Presupuestos, Constantes, Modelopresupuesto, Registrodeconstantes
from .models import Almacenero, CuentaCorriente, Cuota, Pago, RegistroAlmacenero, ArchivosAdmFin, Arqueo, RetirodeSocios, MovimientoAdmin, Honorarios,PagoRentaAnticipada, RegistroEmail
from proyectos.models import Unidades, Proyectos
from ventas.models import Pricing, VentasRealizadas, FeaturesUni
from rrhh.models import datosusuario
from .functions import fechas_cc, flujo_ingreso_proyecto_cliente, flujo_ingreso_proyecto, promedio_almacenero, registroemail, resumen_cuentas


def cuentacte_resumen(request):


    if len(Cuota.objects.values_list("cuenta_corriente__venta__proyecto__id", flat = True)) > 0:

        list_p = Cuota.objects.values_list("cuenta_corriente__venta__proyecto__id", flat = True)
        list_p = list(set(list_p))

        id_proyecto = random.choice(list_p)

        lista_proyecto = []
        for l in list_p:
            aux = Proyectos.objects.get(id = int(l))
            lista_proyecto.append(aux)

        if request.method == 'POST':

            proyecto_elegido = request.POST["proyecto"].split("-")
            id_proyecto = proyecto_elegido[0]
            
        data_proyecto = resumen_cuentas(id_proyecto)
        context = {}
        context["proyecto"] = Proyectos.objects.get(id = int(id_proyecto))
        context["data_cuadro"] = data_proyecto
        context["lista_proyecto"] = lista_proyecto

    else:
        context = {}
        context["sin_data"] = 1


    return render(request, 'ctacte_resumen.html', context)

def totalcuentacte(request, id_proyecto, cliente, moneda, boleto):

    # Listado de los proyectos que tienen cuenta corrientes

    proyectos = Proyectos.objects.all()

    listado = []

    for proyecto in proyectos:

        if len(Cuota.objects.filter(cuenta_corriente__venta__proyecto = proyecto)) > 0:

            listado.append(proyecto)

    if request.method == 'POST':

            proyecto_elegido = request.POST["proyecto"].split("-")
            id_proyecto = proyecto_elegido[0]

    #### Contenido de los cuadros resumens

    context = {}

    proyecto = proyectos.get(id = id_proyecto)
    context["proyecto"] = proyecto
    data_proyecto = resumen_cuentas(id_proyecto)
    context["data_cuadro"] = data_proyecto
    context["fechas"] = fechas_cc(id_proyecto)
    context["listado"] = listado
    context["informacion_general"] = len(CuentaCorriente.objects.filter(venta__proyecto = proyecto).exclude(estado = "baja"))

    if cliente == "0":

        context["flujo_proyecto"] = flujo_ingreso_proyecto(id_proyecto, context["fechas"])

    else:
        context["flujo_proyecto_cliente"] = flujo_ingreso_proyecto_cliente(id_proyecto, context["fechas"], moneda, boleto)
    
    context["cliente"] = cliente

    return render(request, 'totalcuentas.html', context)
