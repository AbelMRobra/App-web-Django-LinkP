from app import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

def mandar_email(mensaje, recibe, subject):

    if mensaje == 1:

        mensaje = mensaje_sp_autorizada()
    
    if mensaje == 2:

        mensaje = mensaje_sp_rechazada()

    if mensaje == 3:
        mensaje = mensaje_sp_observada()

    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Construimos el mensaje simple
    
    mensaje = MIMEText(mensaje)

    mensaje['From']=settings.EMAIL_HOST_USER
    mensaje['To']=recibe
    mensaje['Subject']=subject


    # Envio del mensaje

    mailServer.sendmail(settings.EMAIL_HOST_USER,
                    recibe,
                    mensaje.as_string())


def mensaje_sp_autorizada():

    return """
                    
Buenas!,

Este es un mensaje automatico de Link-P, por favor no conteste.

Tu orden de compra fue autorizada por SP en el dia de la fecha

Para continuar, debes dejar una copia fisica en la oficina cumpliendo los tiempos del circuito

Si este mensaje es un error, por favor comunicate con el equipo de IT

Muchas gracias, saludos!
                    """

def mensaje_sp_rechazada():

    return """
                    
Buenas!,

Este es un mensaje automatico de Link-P, por favor no conteste.

Tu orden de compra fue RECHAZADA por SP en el dia de la fecha

Debes comunicarte con el para responder las dudas que tenga para continuar con el circuito

Si este mensaje es un error, por favor comunicate con el equipo de IT

Muchas gracias, saludos!
                    """


def mensaje_sp_observada():

    return """
                    
Buenas!,

SP tiene dudas sobre tu OC

Por favor comunicate con el para responder sus dudas

Gracias!

Saludos!
                """