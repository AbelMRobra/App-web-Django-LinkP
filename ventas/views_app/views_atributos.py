from django.shortcuts import render, redirect
from ventas.models import Pricing, ArchivosAreaVentas, VentasRealizadas, ArchivoFechaEntrega, ArchivoVariacionHormigon, ReclamosPostventa, \
                            ImgEnlacesProyecto

from proyectos.models import Unidades, Proyectos
from ..funciones.f_pricing import *
from ..funciones.f_atributos import *



def atributos_proyecto_panel(request, id_proj):

    proyecto = Proyectos.objects.get(id = id_proj)

    context = {}

    if request.method == 'POST':

        try:
            context["mensaje"] = atributo_agregar(proyecto, request.POST['nombre'], request.POST['inc'])

        except:
            pass

        try:
            context["mensaje"] = atributo_editar(request.POST['modificar'], request.POST['nombre_editar'], request.POST['inc'])

        except:
            pass

        try:
            context["mensaje"] = atributo_borrar(request.POST['borrar'])

        except:
            pass

        try:
            data_post = request.POST.items()

            for dato in data_post:

                if '&' in dato[0]:
                    
                    atributo_asignar_unidad(dato)

                    context["mensaje"] = [1, "Atributos modificados correctamente!"]
        
        except:           
            pass

    unidades = Unidades.objects.filter(proyecto__id = id_proj).order_by("orden")
  
    atributos_proyecto = FeaturesProjects.objects.filter(proyecto__id = id_proj)

    informacion_unidades = []

    for unidad in unidades:

        atributo_unidad = []

        for atributo in atributos_proyecto:
            if len(FeaturesUni.objects.filter(feature = atributo, unidad = unidad)) == 1:
                atributo_unidad.append(("SI", atributo))
            if len(FeaturesUni.objects.filter(feature = atributo, unidad = unidad)) == 0:
                atributo_unidad.append(("NO", atributo))

        m2_resultante = unidades_calculo_m2(unidad.id)
        precios = unidades_calculo_precio_final(unidad.id)
        precio_base = precios[0]
        precio_final = precios[1]


        informacion_unidades.append((unidad, atributo_unidad, m2_resultante, precio_base, precio_final))

        context["features"] = atributos_proyecto
        context["data"] = informacion_unidades

    return render(request, 'pricing/pricing_atributos_panel.html', context)
