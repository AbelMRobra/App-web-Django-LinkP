from django.shortcuts import render, redirect
from ventas.models import Pricing, ArchivosAreaVentas, VentasRealizadas, ArchivoFechaEntrega, ArchivoVariacionHormigon, ReclamosPostventa, \
                            ImgEnlacesProyecto, PricingResumen
from datetime import date
import datetime
from proyectos.models import Unidades, Proyectos
from ..funciones.f_pricing import *
from ..funciones.f_atributos import *

def pricing_panel(request):

    context = {}

    context["proyectos"] = Unidades.objects.all().values_list("proyecto__nombre", flat=True).distinct()

    if request.method == 'POST':

        proyecto = Proyectos.objects.get(nombre = request.POST["proyecto"])

        return redirect( 'Pricing', id_proyecto = proyecto.id )


    return render(request, 'pricing/pricing_panel.html', context)

def pricing_visor(request, id_proyecto):

    context = {}
    context['alertas'] = []
    
    #Aqui empieza para cambiar el precio base

    precio_nuevo = 0

    if request.method == 'POST':

        context["mensaje"] = pricing_editar_unidad(request.POST["editar"], request.POST["numero"],  request.POST["piso"], request.POST["nombre"], request.POST["tipologia"], request.POST["superficie"])

        
        
        #pricing_actualizar_almacenero(proyecto, ingreso_ventas, unidades_socios, comision)

    if request.method == 'GET':

        datos_recibidos_get = request.GET.items()

        for dato in datos_recibidos_get:

            pricing_modificar_precio_desde(id_proyecto, dato[1])

    proyecto = Proyectos.objects.get(id = id_proyecto)
    otros_datos = 0
    anticipo = 0.4
    fecha_entrega =  datetime.datetime.strptime(str(proyecto.fecha_f), '%Y-%m-%d')

    ahora = datetime.datetime.utcnow()

    y = fecha_entrega.year - ahora.year
    n = fecha_entrega.month - ahora.month
    meses = y*12 + n

    m2_totales = 0

    datos_unidades = []

    precio_final_proyecto = 0
    m2_totales = 0

    unidades = Unidades.objects.filter(proyecto = proyecto).order_by("orden")

    for unidad in unidades:

        # -> Condiciones previas para empezar el calculo

        # -> Calculamos los datos del visor

        m2_resultante = unidades_calculo_m2(unidad.id)
        calculo_precios = unidades_calculo_precio_final(unidad.id)
        precio_final = calculo_precios[1]
        precio_final_m2 = round((calculo_precios[1]/m2_resultante), 4)
        precio_financiado = unidades_calculo_financiacion(unidad, meses, calculo_precios[0], m2_resultante)
        precio_financiado_m2 = precio_financiado/m2_resultante
        precio_anticipo = precio_financiado*0.4
        precio_cuotas = (precio_financiado - anticipo)/meses

        ventas = VentasRealizadas.objects.filter(unidad = unidad).exclude(estado = "BAJA")

        datos_unidades.append((unidad, m2_resultante, precio_final_m2, precio_final, precio_financiado_m2, precio_financiado, precio_anticipo, precio_cuotas, ventas))

        # -> Calculamos algunos datos generales

        m2_totales += m2_resultante
        precio_final_proyecto += precio_final

        ventas_actualizar_datos(unidad)
        
    # if request.method == 'GET':

    #     nuevo_precio = request.GET.items()

    #     for precio in nuevo_precio:

    #         precio_nuevo = precio[1]

    #         date = datetime.date.today()

    #         b = PricingResumen(
    #             proyecto = proyecto,
    #             fecha = date,
    #             precio_prom_contado = promedio_contado,
    #             precio_prom_financiado = promedio_financiado,
    #             base_precio = precio_nuevo,
    #             anticipo = 0.4,
    #             cuotas_pend = meses,
    #         )
            
    #         b.save()

    context["proyecto"] = proyecto
    context["datos"] = unidades
    context["datos_unidades"] = datos_unidades
    context["anticipo"] = anticipo
    context['m2_totales'] = m2_totales
    context['precio_final_proyecto'] = precio_final_proyecto

    return render(request, 'pricing/pricing_visor.html', context)


