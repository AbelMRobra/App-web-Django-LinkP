from django.shortcuts import render, redirect
import requests

from rrhh.models import Sugerencia,datosusuario

from users.funciones.mandaremail import mandar_email


def sugerencias(request):

    if request.method == 'POST':
        try:

            sugerencia_selec = Sugerencia.objects.get(id = int(request.POST['id']))
            sugerencia_selec.nombre = request.POST['nombre']
            sugerencia_selec.descripcion = request.POST['descripcion']

            try:
                sugerencia_selec.adjunto = request.FILES['adjunto']
                sugerencia_selec.save()
            except:
                sugerencia_selec.save()
           
        except:
            pass

        try:

            creador = datosusuario.objects.get(identificacion = request.user.username)
            nueva_consulta = Sugerencia(
                usuario = creador,
                nombre = request.POST['nombre'],
                descripcion = request.POST['descripcion'],
            )
            nueva_consulta.save()

            try:
                nueva_consulta.adjunto = request.FILES['adjunto']
            except:
                pass

            mensaje = """{} ha cargado una nueva sugerencia: {}  """.format(creador.identificacion, request.POST['nombre'])
            titulo = "Nueva sugerencia Link-P"
            usuarios_it = datosusuario.objects.filter(area = "IT")

            for user in usuarios_it:
                email = user.email
                mandar_email(mensaje, email, titulo)


        except:
            pass
        try:
            today  = date.today()
            sugerencia = Sugerencia.objects.get(id = int(request.POST['ENTREGADO']))
            sugerencia.estado = "LISTO"
            sugerencia.fecha_listo = today
            sugerencia.save()

            email = sugerencia.usuario.email
            titulo = """Hola {}!, completamos tu sugerencia!  """.format(sugerencia.usuario.nombre)
            mensaje = "Trabajamos y resolvimos tu sugerencia {}, cuentanos tu experiencia y si es lo que buscabas para seguir mejorando!, te deseamos un gran dia!".format(sugerencia.nombre)
            mandar_email(mensaje, email, titulo)

        except:
            pass
        if 'respuesta' in request.POST.dict():
            respuesta=request.POST.dict()['respuesta']
            id_sug=request.POST.dict()['sugerencia']
            
            sugerencia=Sugerencia.objects.get(pk=id_sug)
            respuestas=sugerencia.respuestas
            if respuestas is None:
                sugerencia.respuestas=respuesta
            else:
                sugerencia.respuestas=respuestas + '|' + respuesta
            sugerencia.save()

            return redirect('Sugerencias')

    sugerencias = Sugerencia.objects.all().order_by("-id")

    data=[]
    for i in sugerencias:
        sug=[]
        resp=i.respuestas
        respuestas=resp.split('|')
        sug.extend([i,respuestas])
        data.append(sug)
    return render (request, 'users/sugerencias.html', {'data':data})
