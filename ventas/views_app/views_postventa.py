import numpy as np
import datetime

from django.shortcuts import render, redirect
from ventas.models import ReclamosPostventa, AdjuntosReclamosPostventa, ClasificacionReclamosPostventa, \
    FormularioDetallePostventa, FormularioSolucionPostventa
from users.models import datosusuario

def postventa_panel_principal(request):

    context = {}


    if request.method == 'POST':

        datos_post = request.POST.dict()

        if 'crear_clasificacion' in datos_post:

            try:

                nuevo_reclamo = ClasificacionReclamosPostventa.objects.create(nombre = request.POST["crear_clasificacion"])
                context['mensaje'] = [1, "Creado correctamente!"]
            except:

                context['mensaje'] = [0, "Ya existe el nombre"]

        if 'borrar_clasificacion' in datos_post:

            reclamo = ClasificacionReclamosPostventa.objects.get(nombre = request.POST["borrar_clasificacion"]).delete()
            context['mensaje'] = [1, "Borrado correctamente!"]
        if 'editar_clasificacion' in datos_post:

            reclamo = ClasificacionReclamosPostventa.objects.get(nombre = request.POST["editar_clasificacion"])
            reclamo.nombre =request.POST["nombre_nuevo"]
            reclamo.save()

            context['mensaje'] = [1, "Editado correctamente!"]

        if 'borrar_adjuntos' in datos_post:

            try:

                ids_adjuntos = [id_adjunto for id_adjunto in datos_post if 'adjunto-' in id_adjunto]

                for id in ids_adjuntos:

                    id_adjunto = request.POST[id]
                    adjunto = AdjuntosReclamosPostventa.objects.get(id=int(id_adjunto))
                    adjunto.delete()

                
                context['mensaje'] = [1, "Adjuntos eliminados"]

            except:

                context['mensaje'] = [0, "Error inesperado al tratar de eliminar"]

        if 'borrar_reclamo' in datos_post:
            
            try:

                id_reclamo = int(request.POST['borrar_reclamo'])
                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)
                reclamo.delete()

                context['mensaje'] = [1, "Reclamo eliminado"]

            except:

                context['mensaje'] = [0, "Error inesperado al tratar de eliminar"]

        if 'nuevo_reclamo' in datos_post:

            try:

                usuario = datosusuario.objects.get(identificacion = request.user.username)
                
                reclamo=ReclamosPostventa(
                    numero = request.POST['numero_nuevo'],
                    fecha_reclamo = request.POST['fecha_nuevo'],
                    propietario = request.POST['propietario_nuevo'],
                    usuario = request.POST['usuario_nuevo'],
                    telefono = request.POST['telefono_nuevo'],
                    email = request.POST['email_nuevo'],
                    proyecto = request.POST['proyecto_nuevo'],
                    unidad = request.POST['unidad_nuevo'],
                    clasificacion = request.POST['clasificacion_nuevo'],
                    descripcion = request.POST['descripcion_nuevo'],
                    responsable=usuario,
                )
                
                reclamo.save()

                context['mensaje'] = [1, "Creado exitosamente"]

            except:

                context['mensaje'] = [0, "Error inesperado al tratar de crear el reclamo"]

        if 'editar_reclamo' in datos_post:
        
            try:

                id_reclamo=int(request.POST['editar_reclamo'])
                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)
                reclamo.numero = request.POST['numero_editar']
                reclamo.fecha_reclamo = request.POST['fecha_editar']
                reclamo.propietario = request.POST['propietario_editar']
                reclamo.usuario = request.POST['usuario_editar']
                reclamo.telefono = request.POST['telefono_editar']
                reclamo.email = request.POST['email_editar']
                reclamo.proyecto = request.POST['proyecto_editar']
                reclamo.unidad = request.POST['unidad_editar']
                reclamo.clasificacion = request.POST['clasificacion_editar']
                reclamo.descripcion = request.POST['descripcion_editar']

                reclamo.save()

                     
                try:
                    reclamo.fecha_solucion = request.POST['fecha_solucion_editar']
                    reclamo.save()

                    context['mensaje'] = [1, "Todo listo!, se guardaron los cambios"]

                except:
                    context['mensaje'] = [1, "Reclamo editado correctamente"]

                try:

                    usuario = datosusuario.objects.get(id = int(request.POST['responsable_editar'].split("-")[0]))
                    reclamo.responsable = usuario
                    reclamo.save()
   
                except:
                    context['mensaje'] = [1, "No se encontro el usuario indicado, pero se pudo editar"]

            except:

                context['mensaje'] = [0, "Error inesperado al tratar de editar el reclamo"]


        if 'reclamo_para_adjuntar' in datos_post:

            try:
                reclamo_adjuntar = ReclamosPostventa.objects.get(id = int(request.POST['reclamo_para_adjuntar']))
                nuevo_reclamo = AdjuntosReclamosPostventa(
                    nombre = request.POST['nombre_adjunto'],
                    reclamo = reclamo_adjuntar,
                    archivo = request.FILES['adjunto']
                )

                nuevo_reclamo.save()

                context['mensaje'] = [1, "Adjunto cargado correctamente"]

            except:

                context['mensaje'] = [0, "Error inesperado al tratar de subir el adjunto"]

        if 'cambio_estado' in datos_post:

            try:
                reclamo_visto = ReclamosPostventa.objects.get(id = int(request.POST['cambio_estado']))
                reclamo_visto.visto = True
                reclamo_visto.save()

                context['mensaje'] = [1, "Todo listo!"]

            except:
                
                context['mensaje'] = [0, "No se pudo cambiar el estado"]

    con = ReclamosPostventa.objects.all()

    datos_proyectos = con.values_list("proyecto", flat= True).distinct().order_by("proyecto")

    context['proyectos'] = datos_proyectos

    datos_clasificacion = con.values_list("clasificacion", flat= True).distinct().order_by("clasificacion")

    context['clasificacion'] = datos_clasificacion

    datos_reclamos = con.order_by("-numero")
    context['datos_completos'] = [(dato, AdjuntosReclamosPostventa.objects.filter(reclamo = dato)) for dato in datos_reclamos]

    if request.method == 'POST':

        datos_post = request.POST.dict()

        if 'filtro_proyecto' in datos_post:

            context['filtro_proyecto'] = request.POST['filtro_proyecto']

            datos_reclamos = con.filter(proyecto__icontains = request.POST['filtro_proyecto']).order_by("-numero")

        if 'filtro_clasificacion' in datos_post:

            context['filtro_clasificacion'] = request.POST['filtro_clasificacion']

            datos_reclamos = datos_reclamos.filter(clasificacion__icontains = request.POST['filtro_clasificacion']).order_by("-numero")

    context['datos'] = [(dato, AdjuntosReclamosPostventa.objects.filter(reclamo = dato)) for dato in datos_reclamos]
    context['datos_clasficacion'] = ClasificacionReclamosPostventa.objects.all()
    context['usuarios'] = datosusuario.objects.all().exclude(estado = "BAJA").order_by("nombre")


    return render(request, 'postventa/postventa_principal.html', context)

def postventa_reporte(request):

    list_category = ReclamosPostventa.objects.all().values_list('clasificacion')
    list_category = list(set(list_category))

    list_project = ReclamosPostventa.objects.all().values_list('proyecto')
    list_project = list(set(list_project))

    category_data = []

    for l in list_category:
        porcentual_l = len(ReclamosPostventa.objects.filter(clasificacion = l[0]))/len(ReclamosPostventa.objects.all())*100

        category_data.append((l[0], porcentual_l))

    status_data = []

    for p in list_project:
        listos = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "LISTO"))
        trabajando = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "TRABAJANDO"))
        problemas = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "PROBLEMAS"))
        espera = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "ESPERA"))
        status_data.append((listos, trabajando, problemas, espera))

    category_data = sorted(category_data, key=lambda x: x[1], reverse=True)

    listos = len(ReclamosPostventa.objects.filter(estado = "LISTO"))
    trabajando = len(ReclamosPostventa.objects.filter(estado = "TRABAJANDO"))
    problemas = len(ReclamosPostventa.objects.filter(estado = "PROBLEMAS"))
    todos = len(ReclamosPostventa.objects.all())
    general_data = [listos, trabajando, problemas, todos]

    days = []

    data_list = ReclamosPostventa.objects.filter(estado = "LISTO")

    for i in data_list:
        if i.fecha_solucion:
            inicio = i.fecha_reclamo
            final = i.fecha_solucion
            dias = (final - inicio).days
            days.append(dias)

    days = np.array(days)
    promedio = np.mean(days)
    maximo = np.max(days)
    minimo = np.min(days)
    

    return render(request, 'postventa/postventa_reporte.html', {'minimo':minimo, 'maximo':maximo,'promedio':promedio,'general_data':general_data, 'satus_data':status_data, 'category_data':category_data, 'list_project':list_project})

def postventa_reclamo_detalle(request, id_reclamo):

    if request.method == 'POST':

        datos = request.POST.items()

        for i in datos:

            if i[0] == "LISTO":

                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)
                reclamo.fecha_solucion = datetime.date.today()
                reclamo.estado = "LISTO"
                reclamo.save()

            if i[0] == "TRABAJANDO":

                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)

                reclamo.estado = "TRABAJANDO"
                reclamo.fecha_solucion = None
                reclamo.save()

            if i[0] == "PROBLEMAS":

                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)

                reclamo.estado = "PROBLEMAS"
                reclamo.fecha_solucion = None
                reclamo.save()

    datos = ReclamosPostventa.objects.get(id = id_reclamo)

    

    return render(request, 'postventa/postventa_reclamo_detalle.html', {'datos':datos})

def postventa_formulario_1(request, id_reclamo):

    context = {}
    
    context["datos_reclamo"] = ReclamosPostventa.objects.get(id = id_reclamo)

    if request.method == 'POST':

        nuevo = FormularioSolucionPostventa.objects.create(

            reclamo = context["datos_reclamo"],
            fecha = datetime.date.today(),
            responsable = request.POST["responsable"],
            metodo_pago = request.POST["metodo_pago"],
            costo_mo = float(request.POST["costo_mo"]),
            costo_mat = float(request.POST["costo_mat"]),
            descripcion = request.POST["descripcion"],
            observacion = request.POST["observacion"],
        )

    if len(FormularioSolucionPostventa.objects.filter(reclamo = context["datos_reclamo"])) > 0:
        context["datos_formulario"] = FormularioSolucionPostventa.objects.filter(reclamo = context["datos_reclamo"]).order_by("-id")

    else:

        context["datos_formulario"] = False

    return render(request, 'postventa/postventa_formulario_1.html', context)

def postventa_formulario_2(request, id_reclamo):

    context = {}
    context["datos_reclamo"] = ReclamosPostventa.objects.get(id = id_reclamo)

    if request.method == 'POST':

        nuevo = FormularioDetallePostventa.objects.create(
            reclamo = context["datos_reclamo"],
            fecha_incio = request.POST["fecha_inicio"],
            fecha_final = request.POST["fecha_final"],
            descripcion = request.POST["descripcion"],

        )

    if len(FormularioDetallePostventa.objects.filter(reclamo = context["datos_reclamo"])) > 0:
        context["datos_formulario"] = FormularioDetallePostventa.objects.filter(reclamo = context["datos_reclamo"]).order_by("-id")

    else:

        context["datos_formulario"] = False

    return render(request, 'postventa/postventa_formulario_2.html', context)

def crearreclamo(request):

    proyectos = list(set(ReclamosPostventa.objects.values_list('proyecto')))
    clasificacion = list(set(ReclamosPostventa.objects.values_list('clasificacion')))

    if request.method == 'POST':

        b = ReclamosPostventa(
                numero = request.POST['numero'],
                fecha_reclamo = request.POST['fecha'],
                propietario = request.POST['propietario'],
                usuario = request.POST['usuario'],
                telefono = request.POST['telefono'],
                email = request.POST['email'],
                proyecto = request.POST['proyecto'],
                unidad = request.POST['unidad'],
                estado = "ESPERA",
                clasificacion = request.POST['clasificacion'],
                descripcion = request.POST['descripcion'],
                )

        b.save()

        return redirect('Reclamos Postventa')

    return render(request, 'postventa/agregarreclamo.html', {'proyectos':proyectos, 'clasificacion':clasificacion})

def editarreclamo(request, id_reclamo):

    datos = ReclamosPostventa.objects.get(id = id_reclamo)

    proyectos = list(set(ReclamosPostventa.objects.values_list('proyecto')))
    clasificacion = list(set(ReclamosPostventa.objects.values_list('clasificacion')))
    responsable = datosusuario.objects.values_list('identificacion')

    if request.method == 'POST':
        reclamo = ReclamosPostventa.objects.get(id = id_reclamo)
        reclamo.numero = request.POST['numero']
        reclamo.fecha_reclamo = request.POST['fecha']
        reclamo.propietario = request.POST['propietario']
        reclamo.usuario = request.POST['usuario']
        reclamo.telefono = request.POST['telefono']
        reclamo.email = request.POST['email']
        reclamo.proyecto = request.POST['proyecto']
        reclamo.unidad = request.POST['unidad']
        reclamo.clasificacion = request.POST['clasificacion']
        reclamo.descripcion = request.POST['descripcion']
        if request.POST['fecha_solucion']:
            reclamo.fecha_solucion = request.POST['fecha_solucion']
        try:
            usuario = datosusuario.objects.get(identificacion = request.POST['responsable'])
            reclamo.responsable = usuario
            reclamo.save()
        except:
            reclamo.save()

        return redirect('Reclamo', id_reclamo = datos.id)

    return render(request, 'postventa/editar_reclamo.html', {'responsable':responsable, 'datos':datos, 'proyectos':proyectos, 'clasificacion':clasificacion})


