from django.shortcuts import render
from django.shortcuts import redirect
from proyectos.models import Proyectos
from .models import Etapas, ItemEtapa, TecnicaMensaje, SubItem, SubSubItem
from rrhh.models import datosusuario
import datetime
from datetime import date, timedelta

# Create your views here.


def subitem(request, id_item):

    datos_item = ItemEtapa.objects.get(id = id_item)
    datos_sub = SubItem.objects.filter(item = datos_item)

    return render(request, 'subitems.html', {"datos_item":datos_item, "datos_sub":datos_sub})

def agregarsubitem(request, id_item):

    datos = ItemEtapa.objects.get(id = id_item)

    if request.method == 'POST':
        orden = len(SubItem.objects.filter(item = datos)) +1

        b = SubItem(
            orden = orden,
            nombre = request.POST['nombre'],
            item = datos,
        )

        b.save()

        return redirect('Sub item', id_item = id_item)

    return render(request, "crearsubitem.html", {"datos":datos})

def agregarsubsubitem(request, id_subitem):

    datos = SubItem.objects.get(id = id_subitem)

    if request.method == 'POST':

        orden = len(SubSubItem.objects.filter(subitem = datos)) +1

        b = SubSubItem(
            orden = orden,
            nombre = request.POST['nombre'],
            subitem = datos,
        )

        b.save()

        return redirect('Documentacion Amp', id_proyecto = datos.item.etapa.proyecto.id)

    return render(request, "crearsubsubitem.html", {"datos":datos})

def eliminaritem(request, id_item):

    datos = ItemEtapa.objects.get(id = id_item)

    if request.method == 'POST':

        datos.delete()

        return redirect('Documentacion')

    return render(request, "borraritem.html", {"datos":datos})

def agregaritem(request, id_etapa):

    datos = Etapas.objects.get(id = id_etapa)

    if request.method == 'POST':

        b = ItemEtapa(
            orden = request.POST['orden'],
            nombre = request.POST['nombre'],
            etapa = datos,
        )

        b.save()

        return redirect('Documentacion')

    return render(request, "crearitem.html", {"datos":datos})

def editaritem(request, id_item):

    datos = ItemEtapa.objects.get(id = id_item)

    if request.method == 'POST':
        
        datos.nombre = request.POST['nombre']
        datos.responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])
        datos.estado = request.POST['estado']
        datos.fecha_inicio = request.POST['fechai']
        datos.fecha_final = request.POST['fechaf']
        datos.url = request.POST['url']
        
        if request.POST['orden']:
            datos.orden = request.POST['orden']
            
        if request.POST['fecha_estimada_i']:
            datos.fecha_estimada_i = request.POST['fecha_estimada_i']

        if request.POST['fecha_estimada_f']:
            datos.fecha_estimada_f = request.POST['fecha_estimada_f']
   
        try:
            datos.archivo_vigente = request.FILES['adjunto']
            datos.save()

        except:

            datos.save()

        return redirect('Documentacion')

    return render(request, "editaritem.html", {"datos":datos})

def editarsubitem(request, id_subitem):

    datos = SubItem.objects.get(id = id_subitem)

    if request.method == 'POST':

        datos.nombre = request.POST['nombre']
        datos.responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])
        datos.estado = request.POST['estado']
        datos.fecha_inicio = request.POST['fechai']
        datos.fecha_final = request.POST['fechaf']
        datos.url = request.POST['url']

        if request.POST['orden']:
            datos.orden = request.POST['orden']
            
        if request.POST['fecha_estimada_i']:
            datos.fecha_estimada_i = request.POST['fecha_estimada_i']

        if request.POST['fecha_estimada_f']:
            datos.fecha_estimada_f = request.POST['fecha_estimada_f']
   
        try:
            datos.archivo_vigente = request.FILES['adjunto']
            datos.save()

        except:

            datos.save()

        return redirect('Sub item', id_item = datos.item.id)

    return render(request, "editarsubitem.html", {"datos":datos})

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

        try:

            dias_faltantes_2 = (p.fecha_i - hoy).days

        except:

            dias_faltantes_2 = "NO DEFINIDO"

        datos_etapas = Etapas.objects.filter(proyecto = p)

        sub_datos = []

        avance_general = 0
        cantidad_total = 0
        

        for e in datos_etapas:

            listos = len(ItemEtapa.objects.filter(etapa = e, estado = "LISTO"))

            avance_general = avance_general + listos

            datos_itemetapas = ItemEtapa.objects.filter(etapa = e).order_by("orden")

            datos_subitem = []

            for d in datos_itemetapas:
                
                item_cantidad = len(SubItem.objects.filter(item = d))
                datos_subitem.append((d, item_cantidad))

                if len(SubItem.objects.filter(item = d)) > 0:

                    if len(SubItem.objects.filter(item = d, estado = "PROBLEMAS")) > 0:
                        if d.estado != "PROBLEMAS":
                            d.estado = "PROBLEMAS"
                            d.save()
                    elif len(SubItem.objects.filter(item = d, estado = "TRABAJANDO")) > 0 or (len(SubItem.objects.filter(item = d, estado = "ESPERA"))/len(SubItem.objects.filter(item = d))) != 1:
                        if d.estado != "TRABAJANDO":
                            d.estado = "TRABAJANDO"
                            d.save()
                    elif (len(SubItem.objects.filter(item = d, estado = "LISTO"))/len(SubItem.objects.filter(item = d))) == 1:
                        if d.estado != "LISTO":
                            d.estado = "LISTO"
                            d.save()
                    else:
                        if d.estado != "ESPERA":
                            d.estado = "ESPERA"
                            d.save()

                    fecha_iniciales = SubItem.objects.values_list("fecha_inicio").filter(item = d).exclude(fecha_inicio = None).order_by("fecha_inicio")
                    if len(fecha_iniciales) > 0:
                        d.fecha_inicio = fecha_iniciales[0][0]
                        d.save()

                    fecha_finales = SubItem.objects.values_list("fecha_final").filter(item = d).exclude(fecha_final = None).order_by("-fecha_inicio")
                    if len(fecha_finales) > 0:
                        d.fecha_final = fecha_finales[0][0]
                        d.save()


            cantidad = len(ItemEtapa.objects.filter(etapa = e))

            cantidad_total = cantidad_total + cantidad

            avance = 0
            no_avance = 100

            if cantidad > 0:

                avance = round((listos/cantidad)*100, 0)
                no_avance = 100 - avance

            sub_datos.append((e, datos_subitem, cantidad, avance, no_avance))

        if cantidad_total != 0:

            avance_general = round((avance_general/cantidad_total)*100, 0)

        else:
            avance_general = 0.0

        datos.append((p, sub_datos, dias_faltantes, avance_general, dias_faltantes_2))

    return render(request, "documentacion.html", {"datos":datos, "hoy":hoy})

def documentacionamp(request, id_proyecto, id_estado):

    if id_estado == "0": 
            
        mensaje = "Todo"

    elif id_estado == "1":

        mensaje = "Listo"

    elif id_estado == "2":
        mensaje = "Trabajando"

    elif id_estado == "3":
        mensaje = "Problemas"

    else:
        mensaje = "Espera"

    if request.method == 'POST':

        for d in request.POST.items():

            if "fecha_final_subitem" in d[0]:
                id_subitem = d[0].split('-')
                b = SubItem.objects.get(id= int(id_subitem[0]))
                b.fecha_final = d[1]
                b.save()

            if "fecha_inicio_subitem" in d[0]:
                id_subitem = d[0].split('-')
                b = SubItem.objects.get(id= int(id_subitem[0]))
                b.fecha_inicio = d[1]
                b.save()

            if "estado_subitem" in d[0]:
                id_subitem = d[0].split('-')
                b = SubItem.objects.get(id= int(id_subitem[0]))
                b.estado = d[1]
                b.save()

            if "fecha_inicio_subsubitem" in d[0]:
                id_subsubitem = d[0].split('-')
                b = SubSubItem.objects.get(id= int(id_subsubitem[0]))
                b.fecha_inicio = d[1]
                b.save()

            if "fecha_final_subsubitem" in d[0]:
                id_subsubitem = d[0].split('-')
                b = SubSubItem.objects.get(id= int(id_subsubitem[0]))
                b.fecha_final = d[1]
                b.save()

            if "estado_subsubitem" in d[0]:
                id_subsubitem = d[0].split('-')
                b = SubSubItem.objects.get(id= int(id_subsubitem[0]))
                b.estado = d[1]
                b.save()

            if "subir_subitem" in d[0]:
                
                subitem = SubItem.objects.get(id = d[1])               
                if subitem.orden != 1:
                    orden_nuevo = subitem.orden -1
                    resto_subitems = SubItem.objects.filter(orden = orden_nuevo, item = subitem.item)

                    for r in resto_subitems:
                        r.orden = r.orden + 1
                        r.save()
                    subitem.orden = subitem.orden - 1
                    subitem.save()

            if "bajar_subitem" in d[0]:
                
                subitem = SubItem.objects.get(id = d[1])               
                if subitem.orden != len(SubItem.objects.filter(item = subitem.item)):
                    orden_nuevo = subitem.orden + 1
                    resto_subitems = SubItem.objects.filter(orden = orden_nuevo, item = subitem.item)

                    for r in resto_subitems:
                        r.orden = r.orden - 1
                        r.save()
                    subitem.orden = subitem.orden + 1
                    subitem.save()

            if "subir_subsubitem" in d[0]:
                
                subsubitem = SubSubItem.objects.get(id = d[1])               
                if subsubitem.orden != 1:
                    orden_nuevo = subsubitem.orden -1
                    resto_subsubitems = SubSubItem.objects.filter(orden = orden_nuevo, subitem = subsubitem.subitem)

                    for r in resto_subsubitems:
                        r.orden = r.orden + 1
                        r.save()
                    subsubitem.orden = subsubitem.orden - 1
                    subsubitem.save()

            if "bajar_subsubitem" in d[0]:
                
                subsubitem = SubSubItem.objects.get(id = d[1])               
                if subsubitem.orden != len(SubSubItem.objects.filter(subitem = subsubitem.subitem)):
                    orden_nuevo = subsubitem.orden + 1
                    resto_subsubitems = SubSubItem.objects.filter(orden = orden_nuevo, subitem = subsubitem.subitem)

                    for r in resto_subsubitems:
                        r.orden = r.orden - 1
                        r.save()
                    subsubitem.orden = subsubitem.orden + 1
                    subsubitem.save()

            if "subir_item" in d[0]:
                
                item = ItemEtapa.objects.get(id = d[1])               
                if item.orden != 1:
                    orden_nuevo = item.orden -1
                    resto_items = ItemEtapa.objects.filter(orden = orden_nuevo, etapa = item.etapa)

                    for r in resto_items:
                        r.orden = r.orden + 1
                        r.save()
                    item.orden = item.orden - 1
                    item.save()

            if "bajar_item" in d[0]:
                
                item = ItemEtapa.objects.get(id = d[1])               
                if item.orden != len(ItemEtapa.objects.filter(etapa = item.etapa)):
                    orden_nuevo = item.orden + 1
                    resto_items = ItemEtapa.objects.filter(orden = orden_nuevo, etapa = item.etapa)

                    for r in resto_items:
                        r.orden = r.orden - 1
                        r.save()
                    item.orden = item.orden + 1
                    item.save()


    p = Proyectos.objects.get(id = id_proyecto)
       
    hoy = datetime.date.today()

    dias_faltantes = (p.fecha_f - hoy).days

    fecha_semana_actual = hoy - datetime.timedelta(hoy.weekday())
    
    fechas_semana = []

    fecha_nueva = fecha_semana_actual - datetime.timedelta(7)
    
    for f in range(50):

        fecha_nueva = fecha_nueva + datetime.timedelta(7)

        fechas_semana.append(fecha_nueva)

    try:

        dias_faltantes_2 = (p.fecha_i - hoy).days

    except:

        dias_faltantes_2 = "NO DEFINIDO"

    datos_etapas = Etapas.objects.filter(proyecto = p)

    sub_datos = []

    avance_general = 0
    cantidad_total = 0
        
    for e in datos_etapas:

        listos = len(ItemEtapa.objects.filter(etapa = e, estado = "LISTO"))

        avance_general = avance_general + listos

        if id_estado == "0": 

            datos_itemetapas = ItemEtapa.objects.filter(etapa = e).order_by("orden")

        elif id_estado == "1":

            datos_itemetapas = ItemEtapa.objects.filter(etapa = e, estado = "LISTO").order_by("orden")

        elif id_estado == "2":
            datos_itemetapas = ItemEtapa.objects.filter(etapa = e, estado = "TRABAJANDO").order_by("orden")

        elif id_estado == "3":
            datos_itemetapas = ItemEtapa.objects.filter(etapa = e, estado = "PROBLEMAS").order_by("orden")

        else:
            datos_itemetapas = ItemEtapa.objects.filter(etapa = e, estado = "ESPERA").order_by("orden")


        datos_subitem = []

        for d in datos_itemetapas:

            if id_estado == "0": 
            
                item_cantidad = SubItem.objects.filter(item = d).order_by("orden")

            elif id_estado == "1":

                item_cantidad = SubItem.objects.filter(item = d, estado = 'LISTO').order_by("orden")

            elif id_estado == "2":
                item_cantidad = SubItem.objects.filter(item = d, estado = 'TRABAJANDO').order_by("orden")

            elif id_estado == "3":
                item_cantidad = SubItem.objects.filter(item = d, estado = 'PROBLEMAS').order_by("orden")

            else:
                item_cantidad = SubItem.objects.filter(item = d, estado = 'ESPERA').order_by("orden")
            
            datos_subsubitem = []

            for j in item_cantidad:
                if id_estado == "0": 

                    subsubitems = SubSubItem.objects.filter(subitem = j).order_by("orden")
                elif id_estado == "1":

                    subsubitems = SubSubItem.objects.filter(subitem = j, estado = 'LISTO').order_by("orden")

                elif id_estado == "2":
                    subsubitems = SubSubItem.objects.filter(subitem = j, estado = 'TRABAJANDO').order_by("orden")

                elif id_estado == "3":
                    subsubitems = SubSubItem.objects.filter(subitem = j, estado = 'PROBLEMAS').order_by("orden")

                else:
                    subsubitems = SubSubItem.objects.filter(subitem = j, estado = 'ESPERA').order_by("orden")

                if len(SubSubItem.objects.filter(subitem = j)) > 0:

                    if len(SubSubItem.objects.filter(subitem = j, estado = "PROBLEMAS")) > 0:
                        if j.estado != "PROBLEMAS":
                            j.estado = "PROBLEMAS"
                            j.save()
                    elif len(SubSubItem.objects.filter(subitem = j, estado = "TRABAJANDO")) > 0:
                        if j.estado != "TRABAJANDO":
                            j.estado = "TRABAJANDO"
                            j.save()
                    elif (len(SubSubItem.objects.filter(subitem = j, estado = "LISTO"))/len(SubSubItem.objects.filter(subitem = j))) == 1:
                        if j.estado != "LISTO":
                            j.estado = "LISTO"
                            j.save()
                    else:
                        if j.estado != "ESPERA":
                            j.estado = "ESPERA"
                            j.save()

                    fecha_iniciales = SubSubItem.objects.values_list("fecha_inicio").filter(subitem = j).exclude(fecha_inicio = None).order_by("fecha_inicio")
                    if len(fecha_iniciales) > 0:
                        j.fecha_inicio = fecha_iniciales[0][0]
                        j.save()

                    fecha_finales = SubSubItem.objects.values_list("fecha_final").filter(subitem = j).exclude(fecha_final = None).order_by("-fecha_inicio")
                    if len(fecha_finales) > 0:
                        j.fecha_final = fecha_finales[0][0]
                        j.save()

                datos_subsubitem.append((j, subsubitems))

            if len(SubItem.objects.filter(item = d)) > 0:

                if len(SubItem.objects.filter(item = d, estado = "PROBLEMAS")) > 0:
                    if d.estado != "PROBLEMAS":
                        d.estado = "PROBLEMAS"
                        d.save()
                elif len(SubItem.objects.filter(item = d, estado = "TRABAJANDO")) > 0:
                    if d.estado != "TRABAJANDO":
                        d.estado = "TRABAJANDO"
                        d.save()
                elif (len(SubItem.objects.filter(item = d, estado = "LISTO"))/len(SubItem.objects.filter(item = d))) == 1:
                    if d.estado != "LISTO":
                        d.estado = "LISTO"
                        d.save()
                else:
                    if d.estado != "ESPERA":
                        d.estado = "ESPERA"
                        d.save()

                fecha_iniciales = SubItem.objects.values_list("fecha_inicio").filter(item = d).exclude(fecha_inicio = None).order_by("fecha_inicio")
                if len(fecha_iniciales) > 0:
                    d.fecha_inicio = fecha_iniciales[0][0]
                    d.save()

                fecha_finales = SubItem.objects.values_list("fecha_final").filter(item = d).exclude(fecha_final = None).order_by("-fecha_inicio")
                if len(fecha_finales) > 0:
                    d.fecha_final = fecha_finales[0][0]
                    d.save()

            datos_subitem.append((d, datos_subsubitem))
           
        cantidad = len(ItemEtapa.objects.filter(etapa = e))

        cantidad_total = cantidad_total + cantidad

        avance = 0
        no_avance = 100

        if cantidad > 0:

            avance = round((listos/cantidad)*100, 0)
            no_avance = 100 - avance

        sub_datos.append((e, datos_subitem, cantidad, avance, no_avance))
       
    if cantidad_total != 0:

        avance_general = round((avance_general/cantidad_total)*100, 0)

    else:
        avance_general = 0.0

    datos = [p, sub_datos, dias_faltantes, avance_general, dias_faltantes_2]

    
    return render(request, "documentacionamp.html", {"datos":datos, "hoy":hoy, "fechas_semana":fechas_semana, "fecha_semana_actual":fecha_semana_actual, "mensaje":mensaje})

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

            fecha_1 = ItemEtapa.objects.filter(etapa = e, fecha_inicio__lte = fechas[-1], fecha_final__gte = fecha_inicial_hoy).order_by("fecha_inicio").values_list("fecha_inicio")[0][0]
            fecha_2 = ItemEtapa.objects.filter(etapa = e, fecha_inicio__lte = fechas[-1], fecha_final__gte = fecha_inicial_hoy).order_by("-fecha_final").values_list("fecha_final")[0][0]

            if (fecha_inicial_hoy - fecha_1).days > 0:
                fecha_1 = fecha_inicial_hoy
            else:
                fecha_1 = fecha_1

            if (fechas[-1] - fecha_2).days < 0:
                fecha_2 = fechas[-1]
            else:
                fecha_2 = fecha_2


            for i in items:

                if (i.fecha_inicio - fecha_inicial_hoy).days >= 0 and (fechas[-1] - i.fecha_final).days >= 0:

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