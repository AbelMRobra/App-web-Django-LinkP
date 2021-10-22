from django.http.response import HttpResponse, HttpResponseRedirect
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
from django.contrib.auth.models import User,Group
from django.contrib.auth import logout
from funciones_generales.f_mandar_email import mandar_email
from .functions import generar_contraseña,cropping,recizing

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

    usuarios_datos = datosusuario.objects.all()

    usuarios = []

    for u in usuarios_datos:
        lc_recibidas = len(EntregaMoneda.objects.filter(usuario_recibe = u))
        usuarios.append([u, lc_recibidas])

    usuarios_totales = len(datosusuario.objects.all())
    usuarios_activos = len(datosusuario.objects.filter(estado = "ACTIVO"))
    datos = [usuarios_totales, usuarios_activos]

    return render(request, 'personal_principal.html', {'usuarios':usuarios, 'datos':datos})

def personal_perfil(request, id_persona):

    context={}
    usuario = datosusuario.objects.get(id = id_persona)
    grupos= Group.objects.all().order_by('name')
    
    
    if request.method == 'POST':

        datos=request.POST.dict()
    

        if 'actualizar-usuario' in datos:

            try:

                usuario.nombre = datos.get('nombre')
                usuario.area = datos.get('area')
                usuario.cargo = datos.get('cargo')
                usuario.email = datos.get('email')
                usuario.Telefono = datos.get('telefono')
                usuario.Comentarios = datos.get('comentarios')
      
                usuario.fecha_ingreso=datos.get('fecha_ingreso',None)
                usuario.fecha_nacimiento=datos.get('fecha_nacimiento',None)

                grupo = Group.objects.get(name='RRHH NIVEL 1') 
                grupo.user_set.add(User.objects.get(username='FM'))
                grupo.save()


                usuario.save()

                context['codigo']=1            
            except:
                context['codigo']=0      
            

        if 'baja-alta' in datos:
            try:
                id_usuario=datos['baja-alta']
                usuario=datosusuario.objects.get(pk=id_usuario)
                user=User.objects.get(username=usuario.identificacion)

                
                
                if usuario.estado == "ACTIVO":
                    usuario.estado="NO ACTIVO"
                    user.is_active=False

                    context['codigo']=2      

                elif usuario.estado=="NO ACTIVO":
                    usuario.estado="ACTIVO"
                    user.is_active=True

                    context['codigo']=3

                if user.username==request.user.username:
                    logout(request)

                usuario.save()
                user.save()
        
                      
            except:
                context['codigo']=0     


        if 'gestionar-permisos' in datos:

            try:
                identificacion=datos['gestionar-permisos']

                user=User.objects.get(username=identificacion)
                
                permisos_usuario=user.groups.all().values_list('name',flat=True)

            
                #permisos que vienen desde el template (vienen solo lo que estan chequeados)
                permisos_template=[perm for perm in datos if 'NIVEL' in perm]

                permisos=Group.objects.all()

                for perm in permisos:
                    permiso=perm.name

                    if permiso in permisos_template:

                        if not permiso in permisos_usuario:
                        
                            grupo=Group.objects.get(name=permiso)
                            grupo.user_set.add(user)

                    else:
                        if  permiso in permisos_usuario:
                        
                            grupo=Group.objects.get(name=permiso)
                            grupo.user_set.remove(user)

                user.save()

                du=datosusuario.objects.get(identificacion=identificacion)


                context['codigo']=4            
            except:
                context['codigo']=0   

        
    

    
    context['data']=datosusuario.objects.get(id = id_persona)
    context['permisos']=grupos
    
    return render(request, 'personal_perfil.html',context)

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



    

def crear_usuarios(request):        

    if request.method == 'POST':
        datos=request.POST.dict()
        
        

        if 'crear-usuario' in datos: 

            identificacion=datos['identificacion']

            user=User.objects.filter(username=identificacion)

            if user.count()==0:

            #VERIFICAR QUE NO EXISTA OTRO USUARIO 
                email=datos['email']
                archivos=request.FILES
                imagen=archivos.get('imagen')
                
                user=User.objects.create(username=identificacion,email=email,password=datos['password'],is_active=True)

                # print(imagen)
                # modificada=cropping(imagen)
                # print(modificada)

                usuario=datosusuario(
                    user=user,
                    identificacion=identificacion,
                    nombre=datos['nombre'] + datos['apellido'],
                    area=datos['area'],
                    email=email,
                    Telefono=datos['telefono'],
                    fecha_ingreso=datos['fecha_ingreso'],
                    fecha_nacimiento=datos['fecha_nacimiento'],
                    cargo=datos['cargo'],
                    imagen=imagen,
                    imagenlogo=imagen,
                    )

                
                usuario.save()

                if usuario:
                    
                    path=f'{settings.MEDIA_ROOT}/{imagen}'
                    
                    recizing(path)
                    cropping(path,usuario)


                return redirect('Datos personal')
            else:
                
                mensaje='Ya existe un usuario con el identificador {}'.format(user[0].username)
                print(mensaje)
                
                return render(request,'users/crear_usuarios.html',{'mensaje':mensaje})


    return render(request,'users/crear_usuarios.html',{})


def resetear_contraseña(request):

    if request.method=='POST':
        datos=request.POST.dict()

        if 'resetear-contraseña' in datos:

            email=datos.get('email')
            identificacion=datos.get('identificacion')
          

            usuario=datosusuario.objects.filter(identificacion=identificacion,email=email)
      
            user=User.objects.filter(username=identificacion,email=email)
         
            
            if usuario.count() > 0 and user.count() > 0:
                
                nueva_contraseña=generar_contraseña()

                usuario=user[0]
                usuario.set_password(nueva_contraseña)
                usuario.save()
                mensaje='Hola {}! Tu nueva contraseña es {}. Una vez logueado en el sistema , podras cambiar la contraseña actual por una propia . Saludos'.format(usuario.username,nueva_contraseña)
                
                titulo='Reseteo de contraseña'
                mens=MIMEText("""{}""".format(mensaje))
                mandar_email(mens,usuario.email,titulo)

                mensaje='Tu nueva contraseña fue enviada al email corportativo asociado a tu usuario'

                return redirect('Login')
            else:
                mensaje='No encontramos un usuario con los datos ingresados !'
                return render(request , 'resetear_contraseña.html' , {'mensaje':mensaje})
            
    
    return render(request , 'resetear_contraseña.html' , {})


def informacion_permisos(request):

    return render(request , 'permisos_personal.html',{})