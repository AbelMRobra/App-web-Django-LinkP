from compras.models import AvisoOrdenesCompras
from rrhh.models import datosusuario
import datetime as dt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import requests
from agenda import settings

def mandarEmail(comparativa, mensaje):

    if mensaje == 1:
        encabezado = "Todo listo! La O.C para {} esta autorizada!".format(comparativa.proveedor.name)
        mensaje = """
        
                    
Buenas!,

La O.C numero {} fue autorizada!

Te recordamos que para que no tengas problemas con el pago debes cumplir los siguientes pasos:

* Entrega una copia fisica en la oficina en Lamadrid 377 4B, San Miguel del Tucuman, Tucuman
* Firma la copia fisica en el espacio correspondiente
* En caso de observaciones, comunicate con el que corresponda para aclararlas

Esperamos que termine bien tu dia!

Saludos desde el equipo de Link-P

                    """.format(comparativa.o_c)

    if mensaje == 2:
        encabezado = "Atención! La OC para {} fue rechazada!".format(comparativa.proveedor.name)
        mensaje = """
                    
Buenas!,

La orden de compra {} fue rechaza!

Por favor ingresa a www.linkp.online por si hay mensajes y/o comunicate con el responsable.

Que tengas un buen dia!

Saludos desde el equipo de Link-P
                    """.format(comparativa.o_c)

    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Construimos el mensaje simple
    
    mensaje = MIMEText(mensaje)

    mensaje['From']=settings.EMAIL_HOST_USER
    mensaje['To']=datosusuario.objects.get(identificacion = comparativa.creador).email
    mensaje['Subject']=encabezado


    # Envio del mensaje

    mailServer.sendmail(settings.EMAIL_HOST_USER,
                    datosusuario.objects.get(identificacion = comparativa.creador).email,
                    mensaje.as_string())

def mensajeCierreOc():
    
    fc = AvisoOrdenesCompras.objects.get(id=1).fecha_carga

    fecha_hoy=dt.date.today()
  
    # CALCULAR SI ESTAMOS EN SEMANA DE COMPRAS
    
    weekd=fc.weekday()

    fecha_i = fc - dt.timedelta(weekd)
    fecha_f = fc  + dt.timedelta(4-weekd)
    
    if fecha_hoy <= fecha_f and fecha_hoy >= fecha_i:
        
        semana_compra = "Estamos en semana de compras"
        
        if (fecha_f - fecha_hoy).days == 0:

            semana_compra = "Hoy cierra el tiempo para recibir OC"
            
    else:
        semana_compra = "No es semana de compras"

    return [semana_compra, fc]
       