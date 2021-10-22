from django.shortcuts import render
from ventas.models import VentasRealizadas
import datetime
from proyectos.models import Unidades, Proyectos
from ..funciones.f_pricing import *
from ..funciones.f_atributos import *
from users.funciones import f_generales
from users.models import ActividadesUsuarios

def pricing_visor(request, id_proyecto):

    context = {}
    context['alertas'] = []
    proyecto = Proyectos.objects.get(id = id_proyecto)

    if request.method == 'POST':

        context["mensaje"] = pricing_editar_unidad(request.POST["editar"], request.POST["numero"],  request.POST["piso"], request.POST["nombre"], request.POST["tipologia"], request.POST["superficie"])

    if request.method == 'GET':

        datos_recibidos_get = request.GET.items()

        for dato in datos_recibidos_get:

            pricing_modificar_precio_desde(id_proyecto, dato[1])

            categoria = "pricing"
            accion = f"Modifico base de {proyecto.nombre}"

            f_generales.generales_registro_actividad(request.user.username, categoria, accion)
    
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
        try:
            precio_financiado = unidades_calculo_financiacion(unidad, meses, calculo_precios[0], m2_resultante)
            precio_financiado_m2 = precio_financiado/m2_resultante
            precio_anticipo = precio_financiado*0.4
            precio_cuotas = (precio_financiado - anticipo)/meses
        except:
            context["mensaje"] = "El proyecto no tiene los parametros para el analisis financiero"
            precio_financiado = 0
            precio_financiado_m2 = 0
            precio_anticipo = 0
            precio_cuotas = 0
        
        ventas = VentasRealizadas.objects.filter(unidad = unidad).exclude(estado = "BAJA")

        datos_unidades.append((unidad, m2_resultante, precio_final_m2, precio_final, precio_financiado_m2, precio_financiado, precio_anticipo, precio_cuotas, ventas))

        # -> Calculamos algunos datos generales

        m2_totales += m2_resultante
        precio_final_proyecto += precio_final

        ventas_actualizar_datos(unidad)

    context["proyecto"] = proyecto
    context["datos"] = unidades
    context["datos_unidades"] = datos_unidades
    context["actividades"] = ActividadesUsuarios.objects.filter(categoria = "pricing").order_by("-momento")
    context["anticipo"] = anticipo
    context['m2_totales'] = m2_totales
    context['precio_final_proyecto'] = precio_final_proyecto

    return render(request, 'pricing/pricing_visor.html', context)


