from django.shortcuts import render, redirect
import requests
import datetime as dt
from rrhh.models import Sugerencia,datosusuario

from users.funciones.mandaremail import mandar_email


def sugerencias(request):
    mensaje=''
    if request.method == 'POST':
        datos=request.POST.dict()
        usuarios = datosusuario.objects.all()
        archivo=request.FILES.get('adjunto',None)

        if 'crear' in datos:

            creador = usuarios.get(identificacion = request.user.username)
            nueva_consulta = Sugerencia(
                usuario = creador,
                nombre = request.POST['nombre'],
                descripcion = request.POST['descripcion'],
                adjunto=archivo,
            )
            nueva_consulta.save()
            
            mensaje = """{} ha cargado una nueva sugerencia: {}  """.format(creador.identificacion, request.POST['nombre'])
            titulo = "Nueva sugerencia Link-P"
            usuarios_it = usuarios.filter(area = "IT")

            for user in usuarios_it:
                mandar_email(mensaje, user.email, titulo)

            return redirect('Sugerencias')


        if 'editar' in datos:
            nombre=datos['nombre']
            descrip=datos['descripcion']

            archivo=request.FILES.get('adjunto',None)
     
            sugerencia_selec = Sugerencia.objects.get(id = int(datos['editar']))
            sugerencia_selec.nombre = nombre
            sugerencia_selec.descripcion = descrip
            if archivo is not None:
                sugerencia_selec.adjunto = archivo
            sugerencia_selec.save()
   
            return redirect('Sugerencias')

        if 'eliminar' in datos:

            sug=Sugerencia.objects.get(pk=int(datos['eliminar']))
            sug.delete()

            return redirect('Sugerencias')


        if 'ENTREGADO' in datos:

            today  = dt.date.today()
            sugerencia = Sugerencia.objects.get(id = int(datos['ENTREGADO']))
            sugerencia.estado = "LISTO"
            sugerencia.fecha_listo = today
            sugerencia.save()

            email = sugerencia.usuario.email
            titulo = """Hola {}!, completamos tu sugerencia!  """.format(sugerencia.usuario.nombre)
            mensaje = "Trabajamos y resolvimos tu sugerencia {}, cuentanos tu experiencia y si es lo que buscabas para seguir mejorando!, te deseamos un gran dia!".format(sugerencia.nombre)
            
            try:
                mandar_email(mensaje, email, titulo)
            except:
                mensaje='Ocurrio un error con el envio del email'

            return redirect('Sugerencias')
        #RESPUESTAS
        if 'respuesta' in datos:
            respuesta=datos['respuesta']
            id_sug=datos['sugerencia']
            
            sugerencia=Sugerencia.objects.get(pk=id_sug)
            respuestas=sugerencia.respuestas

            if respuestas is None:
                sugerencia.respuestas=respuesta
            else:
                sugerencia.respuestas=respuestas + '|' + respuesta
            sugerencia.save()


            titulo='Tienes una respuesta a la sugerencia "{}"'.format(sugerencia.nombre)
            mensaje='Tu sugerencia: {}  . Nueva respuesta : {}'.format(sugerencia.descripcion ,respuesta)

            mandar_email(mensaje, sugerencia.usuario.email, titulo)
            return redirect('Sugerencias')

    sugerencias = Sugerencia.objects.all().order_by("-id")


    data=[]
    for i in sugerencias:
        sug=[]
        resp=i.respuestas
        respuestas=resp.split('|')
        sug.extend([i,respuestas])
        data.append(sug)
    return render (request, 'users/sugerencias.html', {'data':data,'mensaje':mensaje})
