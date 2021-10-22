from django.shortcuts import render
from rrhh.models import datosusuario
from ventas.models import ArchivosComercial
from proyectos.models import Proyectos
from users.models import ActividadesUsuarios
from users.funciones import f_generales
from django.db.models import Q

def archivos_principal(request):

    if request.method == "POST":

        datos_post = request.POST.dict()

        if 'editar_archivo' in datos_post:

            archivo_editar = ArchivosComercial.objects.get(id = int(request.POST['editar_archivo']))

            if request.POST["proyecto"] != "0":
                proyecto = Proyectos.objects.get(id = request.POST["proyecto"])
            else:
                proyecto = None

            archivo_editar.nombre = request.POST['nombre']
            archivo_editar.fecha = request.POST['fecha']
            archivo_editar.proyecto = proyecto

            for post in request.POST.items():

                if "editar_usuarios" in post[0]:

                    usuario = datosusuario.objects.get(identificacion = post[0].split("-")[1])
                    archivo_editar.usuarios_permitidos.add(usuario)


            try:
                archivo_editar.adjunto = request.FILES['adjunto']
                archivo_editar.save()

                if archivo_editar.proyecto:
                    nombre_accion = archivo_editar.nombre + " de " + archivo_editar.proyecto.nombre
                else:
                    nombre_accion = archivo_editar.nombre

                accion = f"Edito * {nombre_accion}"

            except:
                archivo_editar.save()

                if archivo_editar.proyecto:
                    nombre_accion = archivo_editar.nombre + " de " + archivo_editar.proyecto.nombre
                else:
                    nombre_accion = archivo_editar.nombre

                accion = f"Edito {nombre_accion}"

            
            categoria = "archivos_comercial"
            f_generales.generales_registro_actividad(request.user.username, categoria, accion)

        if 'eliminar_archivo' in datos_post:

            archivo_eliminar = ArchivosComercial.objects.get(id = int(request.POST['eliminar_archivo']))
            
            categoria = "archivos_comercial"

            if archivo_eliminar.proyecto:
                nombre_accion = archivo_eliminar.nombre + " de " + archivo_eliminar.proyecto.nombre
            else:
                nombre_accion = archivo_eliminar.nombre

            accion = f"Elimino {nombre_accion}"
            archivo_eliminar.delete()
            f_generales.generales_registro_actividad(request.user.username, categoria, accion)


        if 'guardar_archivo' in datos_post:

            if request.POST["proyecto"] != "0":
                proyecto = Proyectos.objects.get(id = request.POST["proyecto"])
            else:
                proyecto = None

            nuevo_archivo = ArchivosComercial(
                nombre = request.POST["nombre"],
                proyecto = proyecto,
                fecha = request.POST["fecha"],
                adjunto = request.FILES["adjunto"]
            )

            nuevo_archivo.save()

            for post in request.POST.items():

                if "usuario" in post[0]:

                    usuario = datosusuario.objects.get(identificacion = post[0].split("-")[1])
                    nuevo_archivo.usuarios_permitidos.add(usuario)

            categoria = "archivos_comercial"
            if proyecto:
                nombre_accion = nuevo_archivo.nombre + " de " + proyecto.nombre
            else:
                nombre_accion = nuevo_archivo.nombre
            accion = f"Cargo {nombre_accion}"

            f_generales.generales_registro_actividad(request.user.username, categoria, accion)

    con_archivos = ArchivosComercial.objects.all().order_by("-fecha")

    context = {}    
    context['archivos'] = con_archivos
    context['user'] = datosusuario.objects.get(identificacion = request.user.username)
    context['usuarios'] = datosusuario.objects.filter(
        Q(area = "MKT-COMER") | Q(area = "DIRECCION") | Q(area = "IT")
        )
    context['proyectos'] = Proyectos.objects.all()
    context['filtros'] = list(set(con_archivos.values_list("nombre", flat=True)))
    context['filtros_seleccionados'] = context['filtros']
    context["actividades"] = ActividadesUsuarios.objects.filter(categoria = "archivos_comercial").order_by("-momento")[0:20]

    if request.method == "POST":

        datos_post = request.POST.dict()

        if 'filtro' in datos_post:

            filtro_seleccionado = []

            for data in datos_post:

                if data != "filtro" and data != "csrfmiddlewaretoken":
                    filtro_seleccionado.append(data)

            filtros_no_seleccionados = [filtro for filtro in context['filtros'] if filtro not in filtro_seleccionado]

            for filtro in filtros_no_seleccionados:
                context['archivos'] = context['archivos'].exclude(nombre = filtro)


            context['filtros_seleccionados'] = filtro_seleccionado

    return render(request, 'archivos/archivos_principal.html', context)