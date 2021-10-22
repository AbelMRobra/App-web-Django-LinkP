from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from rrhh.models import datosusuario, EntregaMoneda
from email.mime.text import MIMEText
from django.contrib.auth.models import User,Group
from django.contrib.auth import logout
from funciones_generales.f_mandar_email import mandar_email
from ..funciones.f_usuarios import generar_contraseña, cropping


def perfil_usuario_principal(request):

    usuarios_datos = datosusuario.objects.all()

    usuarios = []

    for u in usuarios_datos:
        lc_recibidas = len(EntregaMoneda.objects.filter(usuario_recibe = u))
        usuarios.append([u, lc_recibidas])

    usuarios_totales = len(datosusuario.objects.all())
    usuarios_activos = len(datosusuario.objects.filter(estado = "ACTIVO"))
    datos = [usuarios_totales, usuarios_activos]

    return render(request, 'perfil_usuario/perfil_usuario_principal.html', {'usuarios':usuarios, 'datos':datos})

def perfil_usuario_perfil(request, id_persona):

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
    
    return render(request, 'perfil_usuario/perfil_usuario_perfil.html',context)

def perfil_usuario_resetear_password(request):

    if request.method=='POST':
        datos=request.POST.dict()

        if 'resetear-contraseña' in datos:

            email=datos.get('email')
            identificacion=datos.get('identificacion')
          

            usuario=datosusuario.objects.filter(identificacion=identificacion, email=email)
      
            user=User.objects.filter(username=identificacion)
         
            
            if usuario.count() > 0 and user.count() > 0:
                
                nueva_contraseña=generar_contraseña()

                usuario=user[0]
                usuario.set_password(nueva_contraseña)
                usuario.save()
                mensaje='Hola {}! Tu nueva contraseña es {}. Una vez logueado en el sistema , podras cambiar la contraseña actual por una propia . Saludos'.format(usuario.username,nueva_contraseña)
                
                titulo='Reseteo de contraseña'
                mens=MIMEText("""{}""".format(mensaje))
                mandar_email(mens,usuario.email,titulo)

                mensaje_success='Tu nueva contraseña fue enviada al email corportativo asociado a tu usuario'
                return render(request , 'perfil_usuario/perfil_usuario_recuperar_password.html' , {'mensaje_success':mensaje_success})

            else:
                mensaje='No encontramos un usuario con los datos ingresados !'
                return render(request , 'perfil_usuario/perfil_usuario_recuperar_password.html' , {'mensaje':mensaje})
            
    
    return render(request , 'perfil_usuario/perfil_usuario_recuperar_password.html' , {})

def informacion_permisos(request):

    return render(request , 'permisos_personal.html',{})

def users_crear(request):        

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
                    cropping(path)


                return redirect('Datos personal')
            else:
                mensaje='Ya existe un usuario con el identificador {}'.format(user[0].username)
                
                return render(request,'perfil_usuario/perfil_usuario_crear.html',{'mensaje':mensaje})


    return render(request,'perfil_usuario/perfil_usuario_crear.html',{})


