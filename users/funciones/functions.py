from compras.models import Comparativas

import datetime as dt

from rrhh.models import datosusuario

from django.contrib.auth.models import User


# Función de cajas derivadas

def saludo():
    hora_actual = dt.datetime.now()
    
    if hora_actual.hour >= 20:
        mensaje_bievenida = "¡Buenas noches {}!"

    elif hora_actual.hour >= 13:
        mensaje_bievenida = "¡Buenas tardes {}!"

    else:
        mensaje_bievenida = "¡Buen dia {}!"

    return mensaje_bievenida


def Avisos(usuario,aviso):
    nt=False
    nc=False

    fecha_hoy=dt.date.today()
    
    fc=aviso.fecha_carga
    


    dias_faltantes=(fc-fecha_hoy).days

    #CALCULAR SI ESTAMOS EN SEMANA DE COMPRAS
    weekd=fc.weekday()
    
    fecha_i = fc - dt.timedelta(weekd)
    fecha_f = fc  + dt.timedelta(4-weekd)
    
   
    if fecha_hoy <= fecha_f and fecha_hoy >= fecha_i:
        semana_compra=1
        

        if (fecha_f - fecha_hoy).days==0:
            semana_compra=2
            
    else:
        semana_compra=0
       

    if (fecha_f-fecha_hoy).days<0:
        aviso.fecha_carga=fc + dt.timedelta(14)
        aviso.save()
   
   
    
    no_autorizadas=Comparativas.objects.filter(estado="NO AUTORIZADA",creador=usuario)
    no_conformes=Comparativas.objects.filter(visto="VISTO NO CONFORME",creador=usuario)

    if no_autorizadas.exists():
        nt=[no_autorizadas,len(no_autorizadas)]
    if no_conformes.exists():
        nc=[no_conformes,len(no_conformes)]
        
    avisos_comparativas={
        'no_autorizadas':nt,
        'no_conformes':nc,
        'semana_compras':semana_compra,

    }
    return avisos_comparativas


def actualizar_usuarios():

    usuarios=datosusuario.objects.all()

    for usuario in usuarios:
        user=User.objects.filter(username=usuario.identificacion)

        if user.count() >0 :
            usuario.user=user[0]
            usuario.save()


