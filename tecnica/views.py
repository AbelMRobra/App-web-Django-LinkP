from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from proyectos.models import Proyectos
from compras.models import Comparativas
from .models import Etapas, ItemEtapa, TecnicaMensaje, SubItem, SubSubItem, Lp, RegistroDesvios, GerenPlanificacion
from presupuestos.models import Capitulos
from rrhh.models import datosusuario
import datetime
from datetime import date, timedelta
import pandas as pd
import numpy as np

# Create your views here.

def gerenciamientopanel(request):

    today = datetime.date.today()

    first_date = datetime.date(today.year, today.month, 1)

    list_dates = []

    aux_date = first_date

    for date in range(24):

        list_dates.append(aux_date)

        if aux_date.month != 12:

            aux_date = datetime.date(aux_date.year, aux_date.month +1, 1)
        else:
            aux_date = datetime.date(aux_date.year + 1, 1, 1)

    proyectos = Proyectos.objects.filter(fecha_f__gte = first_date, fecha_i__lte = aux_date)

    return render(request, 'geren_panel.html', {'list_dates':list_dates, 'proyectos':proyectos})

def gerenciamientoproyecto(request, id_proyecto):

    proyecto = Proyectos.objects.get(id = int(id_proyecto))

    if request.method == 'POST':

        try:
            archivo_pandas = pd.read_excel(request.FILES['archivo'])
            list_capitulos = Capitulos.objects.all()
            months = {"enero":1, "febrero":2, "marzo":3, "abril":4, "mayo":5, "junio":6, "julio":7, "agosto":8, "septiembre":9, "octubre":10, "noviembre":11, "diciembre":12, "January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
            for cap in list_capitulos:
                row_aux = archivo_pandas[archivo_pandas['Nombre'] == cap.nombre]
                if row_aux.shape[0] > 0:
                    if row_aux['Comienzo'].unique()[0].split():
                        fecha_i_aux = row_aux['Comienzo'].unique()[0].split()
                    elif row_aux['Start'].unique()[0].split():
                        fecha_i_aux = row_aux['Start'].unique()[0].split()
                    if row_aux['Fin'].unique()[0].split():
                        fecha_f_aux = row_aux['Fin'].unique()[0].split()
                    elif row_aux['Finish'].unique()[0].split():
                        fecha_f_aux = row_aux['Finish'].unique()[0].split()
                    fecha_i = datetime.date(int(fecha_i_aux[2]), int(months[fecha_i_aux[1]]), int(fecha_i_aux[0]))
                    fecha_f = datetime.date(int(fecha_f_aux[2]), int(months[fecha_f_aux[1]]), int(fecha_f_aux[0]))
                    data_aux = GerenPlanificacion.objects.filter(proyecto = proyecto, capitulo = cap)
                    if len(data_aux) == 0:
                        b = GerenPlanificacion(
                            proyecto = proyecto,
                            capitulo = cap,
                            fecha_i = fecha_i,
                            fecha_f = fecha_f
                        )

                        b.save()

                    else:
                        data_aux[0].fecha_i = fecha_i
                        data_aux[0].fecha_f = fecha_f
                        data_aux[0].save()
            

        except:
            pass
        try:
            data_aux = GerenPlanificacion.objects.filter(proyecto = proyecto, capitulo__id = int(request.POST['cap']))
            if len(data_aux) == 0:
                b = GerenPlanificacion(
                    proyecto = proyecto,
                    capitulo = Capitulos.objects.get(id = int(request.POST['cap'])),
                    fecha_i = request.POST['fecha_i']
                )

                b.save()

            else:
                data_aux[0].fecha_i = request.POST['fecha_i']
                data_aux[0].save()
        except:
            pass
        try:
            data_aux = GerenPlanificacion.objects.filter(proyecto = proyecto, capitulo__id = int(request.POST['cap']))
            if len(data_aux) == 0:
                b = GerenPlanificacion(
                    proyecto = proyecto,
                    capitulo = Capitulos.objects.get(id = int(request.POST['cap'])),
                    fecha_i = request.POST['fecha_f']
                )

                b.save()

            else:
                data_aux[0].fecha_f = request.POST['fecha_f']
                data_aux[0].save()
        except:
            pass

    capitulo = Capitulos.objects.all()

    data_cap = []

    for cap in capitulo:

        data = GerenPlanificacion.objects.filter(proyecto = proyecto, capitulo = cap)

        if len(data) == 0:
            data_cap.append((cap, 0 ,0))

        else:
            data_cap.append((cap, data[0].fecha_i, data[0].fecha_f))

    today = datetime.date.today()

    first_date = datetime.date(today.year, today.month, 1)

    list_dates = []

    aux_date = first_date

    for date in range(24):

        list_dates.append(aux_date)

        if aux_date.month != 12:

            aux_date = datetime.date(aux_date.year, aux_date.month +1, 1)
        else:
            aux_date = datetime.date(aux_date.year + 1, 1, 1)

    # --> Esta es la parte de las OC

    nombre_proyecto = str(proyecto.nombre)
    nombre_proyecto = nombre_proyecto.replace("TORRE", "").replace(" ", "").replace("-", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("INFRA", "")

    comparativas = Comparativas.objects.filter(proyecto__icontains = nombre_proyecto).exclude(estado = "AUTORIZADA").order_by("-fecha_c")

    return render(request, 'gerem_proyecto.html', {'list_dates':list_dates, 'proyecto':proyecto, 'data_cap':data_cap, 'comparativas':comparativas})

def registrodesvios(request):

    if request.method == 'POST':

        user = datosusuario.objects.get(identificacion = request.user.username)
        proyecto = Proyectos.objects.get(id = request.POST['proyecto'])

        b = RegistroDesvios(
            fecha = request.POST['fecha'],
            proyecto = proyecto,
            creador = user,
            nombre = request.POST['nombre'],
            descrip = request.POST['descrip'],
            dias = request.POST['dias'],

        )

        b.save()

    data = RegistroDesvios.objects.all().order_by('fecha')

    proyectos = Proyectos.objects.all()

    return render(request, 'registros_panel.html', {'data':data, 'proyectos':proyectos})

def registrodesviosid(request, id_registro):

    return render(request, 'registro_id.html')

def principaltecnica(request):

    return render(request, 'tecnica_principal.html')

def bbddgroup(request):

    etapas = Etapas.objects.values_list('nombre', flat = True).order_by('nombre')

    etapas = list(set(etapas))

    datos = []

    for e in etapas:

        items = ItemEtapa.objects.filter(etapa__nombre = e).values_list('nombre', flat = True).order_by('nombre')

        items = list(set(items))
        
        list_subitems = []
        
        for i in items:

            subitems = SubItem.objects.filter(item__nombre = i).values_list('nombre', flat = True).order_by('nombre')

            subitems = list(set(subitems))
            list_subsubitems = []
      
            for s in subitems:

                subsubitems = SubSubItem.objects.filter(subitem__nombre = s).values_list('nombre', flat = True).order_by('nombre')

                subsubitems = list(set(subsubitems))
                list_subsubitems.append((s, subsubitems))

            list_subitems.append((i, list_subsubitems))

        datos.append((e, list_subitems))

    return render(request, 'bbdgroup.html', {'datos':datos})

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

        return redirect('Documentacion Amp', id_proyecto = datos.etapa.proyecto.id, id_estado = 0, id_week = 1)

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

        return redirect('Documentacion Amp', id_proyecto = datos.item.etapa.proyecto.id, id_estado = 0, id_week = 1)

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

        orden = len(ItemEtapa.objects.filter(etapa = datos)) +1

        b = ItemEtapa(
            orden = orden,
            nombre = request.POST['nombre'],
            etapa = datos,
        )

        b.save()

        return redirect('Documentacion Amp', id_proyecto = datos.proyecto.id, id_estado = 0, id_week = 1)

    return render(request, "crearitem.html", {"datos":datos})

def editaritem(request, id_item):

    datos = ItemEtapa.objects.get(id = id_item)

    if request.method == 'POST':
        
        datos.nombre = request.POST['nombre']
        datos.estado = request.POST['estado']
        if request.POST['responsable']:
            datos.responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])
        
        if request.POST['fechai']:
            datos.fecha_inicio = request.POST['fechai']

        if request.POST['fechaf']:
            datos.fecha_final = request.POST['fechaf']

        if request.POST['url']:
            datos.url = request.POST['url']

        if request.POST['fecha_estimada_i']:
            datos.fecha_estimada_i = request.POST['fecha_estimada_i']

        if request.POST['fecha_estimada_f']:
            datos.fecha_estimada_f = request.POST['fecha_estimada_f']
   
        try:
            datos.archivo_vigente = request.FILES['adjunto']
            datos.save()

        except:

            datos.save()

        return redirect('Documentacion Amp', id_proyecto = datos.etapa.proyecto.id, id_estado = 0, id_week = 1)

    return render(request, "editaritem.html", {"datos":datos})

def editarsubitem(request, id_subitem):

    datos = SubItem.objects.get(id = id_subitem)

    if request.method == 'POST':

        datos.nombre = request.POST['nombre']
        datos.estado = request.POST['estado']

        if request.POST['responsable']:
            datos.responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])
        
        if request.POST['fechai']:
            datos.fecha_inicio = request.POST['fechai']

        if request.POST['fechaf']:
            datos.fecha_final = request.POST['fechaf']

        if request.POST['url']:
            datos.url = request.POST['url']

        if request.POST['fecha_estimada_i']:
            datos.fecha_estimada_i = request.POST['fecha_estimada_i']

        if request.POST['fecha_estimada_f']:
            datos.fecha_estimada_f = request.POST['fecha_estimada_f']
   
        try:
            datos.archivo_vigente = request.FILES['adjunto']
            datos.save()

        except:

            datos.save()

        return redirect('Documentacion Amp', id_proyecto = datos.item.etapa.proyecto.id, id_estado = 0, id_week = 1)

    return render(request, "editarsubitem.html", {"datos":datos})

def editarsubsubitem(request, id_subsubitem):

    datos = SubSubItem.objects.get(id = id_subsubitem)

    if request.method == 'POST':

        datos.nombre = request.POST['nombre']
        datos.estado = request.POST['estado']

        if request.POST['responsable']:
            datos.responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])
        
        if request.POST['fechai']:
            datos.fecha_inicio = request.POST['fechai']

        if request.POST['fechaf']:
            datos.fecha_final = request.POST['fechaf']

        if request.POST['url']:
            datos.url = request.POST['url']

        if request.POST['fecha_estimada_i']:
            datos.fecha_estimada_i = request.POST['fecha_estimada_i']

        if request.POST['fecha_estimada_f']:
            datos.fecha_estimada_f = request.POST['fecha_estimada_f']
   
        try:
            datos.archivo_vigente = request.FILES['adjunto']
            datos.save()

        except:

            datos.save()

        return redirect('Documentacion Amp', id_proyecto = datos.subitem.item.etapa.proyecto.id, id_estado = 0, id_week = 1)

    return render(request, "editarsubsubitem.html", {"datos":datos})

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

        if len(Lp.objects.filter(proyecto = p)) > 0:

            lp = Lp.objects.filter(proyecto = p)[0]

        else:
            lp = 0

        datos.append((p, sub_datos, dias_faltantes, avance_general, dias_faltantes_2, lp))

    return render(request, "documentacion.html", {"datos":datos, "hoy":hoy})

def documentacionamp(request, id_proyecto, id_estado, id_week):
    week = int(id_week)

    hoy = date.today()
    fecha_esta_semana = hoy - timedelta(hoy.weekday())
    fecha_otra_semana = fecha_esta_semana + timedelta(7)

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

        # ------------> Borrar lo que sea

        try:
            item = ItemEtapa.objects.get(id= int(request.POST['borraritem']))
            item.delete()
        except:
            pass
        try:
            item = SubItem.objects.get(id= int(request.POST['borraritem']))
            item.delete()
        except:
            pass
        try:
            item = SubSubItem.objects.get(id= int(request.POST['borraritem']))
            item.delete()
        except:
            pass

        # ------------> Editar lo que sea

        try:
            item = ItemEtapa.objects.get(id= int(request.POST['editaritem']))
            item.nombre = request.POST['nombre']
            item.estado = request.POST['estado']
            if request.POST['fecha_estimada_i']:
                item.fecha_estimada_i = request.POST['fecha_estimada_i']
            if request.POST['fecha_estimada_f']:
                item.fecha_estimada_f = request.POST['fecha_estimada_f']
            if request.POST['fechai']:
                item.fecha_inicio = request.POST['fechai']
            if request.POST['fechaf']:
                item.fecha_final = request.POST['fechaf']
            item.url =  request.POST['url']
            try:
                item.archivo_vigente = request.FILES['adjunto']
                item.save()
            except:
                item.save()
        except:
            pass

        try:
            item = SubItem.objects.get(id= int(request.POST['editarsubitem']))
            item.nombre = request.POST['nombre']
            item.estado = request.POST['estado']
            if request.POST['fecha_estimada_i']:
                item.fecha_estimada_i = request.POST['fecha_estimada_i']
            if request.POST['fecha_estimada_f']:
                item.fecha_estimada_f = request.POST['fecha_estimada_f']
            if request.POST['fechai']:
                item.fecha_inicio = request.POST['fechai']
            if request.POST['fechaf']:
                item.fecha_final = request.POST['fechaf']
            item.url =  request.POST['url']
            try:
                item.archivo_vigente = request.FILES['adjunto']
                item.save()
            except:
                item.save()
        except:
            pass

        try:
            item = SubSubItem.objects.get(id= int(request.POST['editarsubsubitem']))
            item.nombre = request.POST['nombre']
            item.estado = request.POST['estado']
            if request.POST['fecha_estimada_i']:
                item.fecha_estimada_i = request.POST['fecha_estimada_i']
            if request.POST['fecha_estimada_f']:
                item.fecha_estimada_f = request.POST['fecha_estimada_f']
            if request.POST['fechai']:
                item.fecha_inicio = request.POST['fechai']
            if request.POST['fechaf']:
                item.fecha_final = request.POST['fechaf']
            item.url =  request.POST['url']
            try:
                item.archivo_vigente = request.FILES['adjunto']
                item.save()
            except:
                item.save()
        except:
            pass

        # ------------> Crear lo que sea

        try:
            item = Etapas.objects.get(id= int(request.POST['crearitem']))

            b = ItemEtapa(
                nombre = request.POST['nombre'],
                etapa_id = item.id,
                estado = "ESPERA"

            )

            b.save()

        except:
            pass

        try:
            item = ItemEtapa.objects.get(id= int(request.POST['crearsubitem']))

            b = SubItem(
                nombre = request.POST['nombre'],
                item_id = item.id,
                estado = "ESPERA"

            )

            b.save()

        except:
            pass


        try:
            item = SubItem.objects.get(id= int(request.POST['crearsubsubitem']))

            b = SubSubItem(
                nombre = request.POST['nombre'],
                subitem_id = item.id,
                estado = "ESPERA"

            )

            b.save()

        except:
            pass

        # ------------> Editar fecha de inicio



        for d in request.POST.items():


            

            if "fecha_final_item" in d[0]:
                id_item = d[0].split('-')
                b = ItemEtapa.objects.get(id= int(id_item[0]))
                b.fecha_final = d[1]
                b.save()

            if "fecha_inicio_item" in d[0]:
                id_item = d[0].split('-')
                b = ItemEtapa.objects.get(id= int(id_item[0]))
                b.fecha_inicio = d[1]
                b.save()

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

            if week: 

                datos_itemetapas = ItemEtapa.objects.filter(etapa = e).order_by("orden")

            else:

                datos_itemetapas = ItemEtapa.objects.filter(etapa = e, fecha_inicio__lte = fecha_otra_semana, fecha_final__gte = fecha_esta_semana).order_by("orden")

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

                if week:
            
                    item_cantidad = SubItem.objects.filter(item = d).order_by("orden")

                else:

                    item_cantidad = SubItem.objects.filter(item = d, fecha_inicio__lte = fecha_otra_semana, fecha_final__gte = fecha_esta_semana).order_by("orden")

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

                    if week:

                        subsubitems = SubSubItem.objects.filter(subitem = j).order_by("orden")
                    else:
                        subsubitems = SubSubItem.objects.filter(subitem = j, fecha_inicio__lte = fecha_otra_semana, fecha_final__gte = fecha_esta_semana).order_by("orden")
                
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


    if request.is_ajax():
        data = [{"datos":datos, "hoy":hoy, "fechas_semana":fechas_semana, "fecha_semana_actual":fecha_semana_actual, "mensaje":mensaje, "week":week}]
        return JsonResponse({'Informacion':data})
    else:
        return render(request, "documentacionamp.html", {"datos":datos, "hoy":hoy, "fechas_semana":fechas_semana, "fecha_semana_actual":fecha_semana_actual, "mensaje":mensaje, "week":week})

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