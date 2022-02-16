from django.shortcuts import render
from django.shortcuts import redirect
from .models import NotaDePedido, datosusuario, ComentariosCorrespondencia, EntregaMoneda, ArchivosGenerales
from proyectos.models import Proyectos
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from agenda import settings

def apprrhh(request):

    return render(request, 'apprrhh_principal.html')

def archivosrrhh(request):

    data = ArchivosGenerales.objects.all()

    if request.method == 'POST':

        try:
            new_r = ArchivosGenerales(
                nombre = request.POST['nombre'],
                descrip = request.POST['descrip'],
                adjunto = request.FILES['adjunto'],
            )
            new_r.save()

        except:
            delete_archivo = ArchivosGenerales.objects.get(id = request.POST["delete"])
            delete_archivo.delete()

    return render(request, 'archivos_rrh/archivos_principal.html', {'data':data})

def personal_principal(request):

    usuarios_datos = datosusuario.objects.all().order_by('identificacion')

    usuarios = []

    for u in usuarios_datos:
        lc_recibidas = len(EntregaMoneda.objects.filter(usuario_recibe = u))
        usuarios.append([u, lc_recibidas])

    usuarios_totales = len(datosusuario.objects.all())
    usuarios_activos = len(datosusuario.objects.filter(estado = "ACTIVO"))
    datos = [usuarios_totales, usuarios_activos]

    return render(request, 'personal_principal.html', {'usuarios':usuarios, 'datos':datos})

def personal_perfil(request, id_persona):

    data = datosusuario.objects.get(id = id_persona)

    if request.method == 'POST':

        data.nombre = request.POST['nombre']
        data.area = request.POST['area']
        data.cargo = request.POST['cargo']
        data.email = request.POST['email']
        data.Telefono = request.POST['telefono']
        data.Comentarios = request.POST['comentarios']
        data.estado = request.POST['estado']
        try:
            data.fecha_nacimiento = request.POST['fecha_nacimiento']

        except:
            pass
        try:
            data.fecha_ingreso = request.POST['fecha_ingreso']
        except:
            pass
        data.save()

        return redirect('Perfil personal', id_persona = data.id)

    return render(request, 'personal_perfil.html', {'data':data})

def editarcorrespondencia(request, id_nota):

    proyectos = Proyectos.objects.all()

    datos = NotaDePedido.objects.get(id = id_nota)

    if request.method == 'POST':

        datos.proyecto = Proyectos.objects.get(nombre = request.POST['proyecto'])
        datos.titulo = request.POST['titulo']
        datos.destinatario = request.POST['desti']
        datos.fecha_requerida = request.POST['fechareq']
        datos.copia = request.POST['copia']
        datos.envio_documentacion = request.POST['envdoc']
        datos.cambio_proyecto = request.POST['camproy']
        datos.comunicacion_general = request.POST['comugral']
        datos.descripcion = request.POST['descripcion']
        datos.save()

        try:
            datos.adjuntos = request.FILES['archivo']
            datos.save()
        except:
            pass

        return redirect('Nota de pedido', id_nota = datos.id)
                
    return render(request, 'editarcorres.html', {"datos":datos, "proyectos":proyectos})



def crearcorrespondencia(request):

    proyectos = Proyectos.objects.all()

    if request.method == 'POST':

        numero = len(NotaDePedido.objects.filter(tipo = request.POST['corres']))+1

        try:

            b = NotaDePedido(

                proyecto = Proyectos.objects.get(nombre = request.POST['proyecto']),
                numero = numero,
                titulo = request.POST['titulo'],
                creador = str(request.user.username),
                destinatario = request.POST['desti'],
                fecha_requerida = request.POST['fechareq'],
                copia = request.POST['copia'],
                adjuntos = request.FILES['archivo'],
                envio_documentacion = request.POST['envdoc'],
                cambio_proyecto = request.POST['camproy'],
                comunicacion_general = request.POST['comugral'],
                descripcion = request.POST['descripcion'],
                tipo = request.POST['corres'],
            )

            b.save()

        except:

            b = NotaDePedido(

                proyecto = Proyectos.objects.get(nombre = request.POST['proyecto']),
                numero = numero,
                titulo = request.POST['titulo'],
                creador = str(request.user.username),
                destinatario = request.POST['desti'],
                fecha_requerida = request.POST['fechareq'],
                copia = request.POST['copia'],
                envio_documentacion = request.POST['envdoc'],
                cambio_proyecto = request.POST['camproy'],
                comunicacion_general = request.POST['comugral'],
                descripcion = request.POST['descripcion'],
                tipo = request.POST['corres'],
            )

            b.save()

        return redirect('Notas de pedido', id_proyecto = 0, tipo = 0)

    return render(request, 'nuevacorres.html', {'proyectos':proyectos})

def notasdepedido(request, id_proyecto, tipo):

    proyectos = NotaDePedido.objects.values_list("proyecto")

    proyectos = list(set(proyectos))

    lista_proyectos = []

    for p in proyectos:

        lista_proyectos.append(Proyectos.objects.get(id = p[0]))

    datos = 0

    if id_proyecto == "0":


        if tipo == "0":

            datos = NotaDePedido.objects.all()

        elif tipo == "1":

            datos = NotaDePedido.objects.filter(tipo = "NP")

        elif tipo == "2":

            datos = NotaDePedido.objects.filter(tipo = "OS")

    if id_proyecto != "0":


        if tipo == "0":

            datos = NotaDePedido.objects.filter(proyecto__id = id_proyecto)

        elif tipo == "1":

            datos = NotaDePedido.objects.filter(tipo = "NP", proyecto__id = id_proyecto)

        elif tipo == "2":

            datos = NotaDePedido.objects.filter(tipo = "OS", proyecto__id = id_proyecto)

    if request.method == 'POST':

        datos_viejos = datos

        datos = []   

        palabra_buscar = request.POST["palabra"]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                lista_palabra = palabra.split()

                buscar = (str(i.proyecto)+str(i.titulo)+str(i.tipo)+str(i.numero)+str(i.creador)+str(i.destinatario))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)


    return render(request, 'notasdepedido.html', {'datos':datos, "id_proyecto":id_proyecto, "tipo":tipo, "lista_proyectos":lista_proyectos})

def notadepedido(request, id_nota):

    datos = NotaDePedido.objects.get(id = id_nota)
    comentarios = ComentariosCorrespondencia.objects.filter(correspondencia = datos).order_by("fecha")

    try:
        creador = datosusuario.objects.get(identificacion=datos.creador)

    except:
        creador = 0

    try:
        destino = datosusuario.objects.get(identificacion=datos.destinatario)

    except:
        destino = 0

    if request.method == 'POST':

        datos_post = request.POST.items()

        try:

            if str(datos.visto) == "None":

                datos.visto = str(request.POST["FIRMA"])

            else:

                datos.visto = str(datos.visto) + "-" + str(request.POST["FIRMA"])

            datos.save()

            return redirect('Notas de pedido', id_proyecto = 0, tipo = 0)

        except:
            pass

        try:
        

            date = datetime.datetime.now() - datetime.timedelta(hours=3)

            b = ComentariosCorrespondencia(

                usuario = datosusuario.objects.get(identificacion = request.user.username),
                correspondencia = datos,
                comentario = request.POST["COMENTARIO"],
                fecha = date
            )

            b.save()

            try:

                # Establecemos conexion con el servidor smtp de gmail
                mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                mailServer.ehlo()
                mailServer.starttls()
                mailServer.ehlo()
                mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                # Construimos el mensaje simple
                
                mensaje = MIMEText("""
                
                Buenas!,

                Tu correspondencia de titulo {} a recibido el siguiente comentario de {}!

                El comentario es: "{}"

                Gracias!

                Saludos!
                """.format(datos.titulo, request.user.username, request.POST["COMENTARIO"]))
                mensaje['From']=settings.EMAIL_HOST_USER
                mensaje['To']=datosusuario.objects.get(identificacion = datos.creador).email
                mensaje['Subject']="Tu correspondencia {} tiene un comentario!".format(datos.titulo)


                # Envio del mensaje

                mailServer.sendmail(settings.EMAIL_HOST_USER,
                                datosusuario.objects.get(identificacion = datos.creador).email,
                                mensaje.as_string())

            except:

                pass

            return redirect('Nota de pedido', id_nota = datos.id)

        except:
            pass

    return render(request, 'notadepedido.html', {'datos':datos, 'creador':creador, 'destino':destino, 'comentarios':comentarios})