from django.shortcuts import render
from proyectos.models import Proyectos
from .models import Etapas, ItemEtapa, TecnicaMensaje
from rrhh.models import datosusuario
import datetime
from datetime import date, timedelta

# Create your views here.

def documentacion(request):

    datos_proyectos = Etapas.objects.values_list("proyecto")

    proyectos = []

    for d in datos_proyectos:
        proyectos.append(Proyectos.objects.get(id = d[0]))
    
    proyectos = list(set(proyectos))

    datos = []

    for p in proyectos:

        hoy = datetime.date.today()

        dias_faltantes = (p.fecha_f - hoy).days

        datos_etapas = Etapas.objects.filter(proyecto = p)

        sub_datos = []

        avance_general = 0
        cantidad_total = 0
        

        for e in datos_etapas:

            listos = len(ItemEtapa.objects.filter(etapa = e, estado = "LISTO"))

            avance_general = avance_general + listos

            datos_itemetapas = ItemEtapa.objects.filter(etapa = e)

            cantidad = len(ItemEtapa.objects.filter(etapa = e))

            cantidad_total = cantidad_total + cantidad

            avance = 0
            no_avance = 100

            if cantidad > 0:

                avance = round((listos/cantidad)*100, 0)
                no_avance = 100 - avance

            sub_datos.append((e, datos_itemetapas, cantidad, avance, no_avance))

        if cantidad_total != 0:

            avance_general = round((avance_general/cantidad_total)*100, 0)

        else:
            avance_general = 0.0

        datos.append((p, sub_datos, dias_faltantes, avance_general))

    return render(request, "documentacion.html", {"datos":datos})

def ganttet(request, id_proyecto):

    proyecto = Proyectos.objects.get(id = id_proyecto)

    datos_etapas = Etapas.objects.filter(proyecto = proyecto)

    # ------> Fechas

    #Establecemos un rango para hacer el gantt
    
    fecha_inicial_hoy = datetime.date.today()

    fecha_inicial_2 = datetime.date(fecha_inicial_hoy.year, fecha_inicial_hoy.month, 1)

    fechas = []

    contador = 0
    contador_year = 1

    # El cash en template es un rango de 24 meses

    for f in range(8):

        if (fecha_inicial_2.month + contador) == 13:
            
            year = fecha_inicial_2.year + contador_year
            
            fecha_cargar = date(year, 1, 1)

            fechas.append(fecha_cargar)
            
            contador_year += 1

            contador = - (12 - contador)

        else:

            mes = fecha_inicial_2.month + contador

            year = fecha_inicial_2.year + contador_year - 1

            fecha_cargar = date(year, mes, 1)

            fechas.append(fecha_cargar)

        contador += 1

    # ------> Datos a colocar

    datos_etapas = Etapas.objects.filter(proyecto = proyecto)

    datos = []

    for e in datos_etapas:

        items = ItemEtapa.objects.filter(etapa = e, fecha_inicio__lte = fechas[-1], fecha_final__gte = fecha_inicial_hoy)

        datos_items = []
        
        if len(items) > 0:

            fecha_1 = ItemEtapa.objects.filter(etapa = e, fecha_inicio__lte = fechas[-1], fecha_final__gte = fecha_inicial_hoy).order_by("-fecha_inicio").values_list("fecha_inicio")[0][0]
            fecha_2 = ItemEtapa.objects.filter(etapa = e, fecha_inicio__lte = fechas[-1], fecha_final__gte = fecha_inicial_hoy).order_by("-fecha_final").values_list("fecha_final")[0][0]

            for i in items:

                if (i.fecha_inicio - fecha_inicial_hoy).days >= 0 and (fechas[-1] - i.fecha_final) >= 0:

                    datos_items.append((i.nombre, i.fecha_inicio, i.fecha_final))

                elif (i.fecha_inicio -fecha_inicial_hoy).days >= 0:

                    datos_items.append((i.nombre, i.fecha_inicio, fechas[-1]))
                else:
                    datos_items.append((i.nombre, fecha_inicial_hoy, i.fecha_final))
            
            datos.append((e.nombre, datos_items, fecha_1, fecha_2))

    return render(request, "gantt.html", {"fechas":fechas, "proyecto":proyecto, "datos":datos})

def mensajesitem(request, id_item):

    if request.method == 'POST':

        datos_post = request.POST.items()

        for i in datos_post:

            if i[0] == "mensaje" and i[1] != "" :

                b = TecnicaMensaje(
                        usuario = datosusuario.objects.get(identificacion = request.user),
                        item = ItemEtapa.objects.get(id = id_item),
                        mensaje = i[1],

                        )

                b.save()


    datos = ItemEtapa.objects.get(id = id_item)

    mensajes = TecnicaMensaje.objects.filter(item__id = id_item).order_by("-fecha")

    return render(request, 'mensajeitem.html', {'datos':datos, 'mensajes':mensajes})