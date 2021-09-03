from rrhh.models import EntregaMoneda, datosusuario, CanjeMonedas
from statistics import mode

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from agenda import settings

def estadisticasLinkcoin():

    con_principal = EntregaMoneda.objects.all()
    

    resultados = {}

    list_mensaje = list(con_principal.values_list("mensaje", flat=True))
    list_mensaje.sort(key = len)
    resultados['mensajeMasCorto'] = (list_mensaje[0], len(list_mensaje[0]), datosusuario.objects.get(identificacion = con_principal.filter(mensaje = list_mensaje[0]).values_list("usuario_recibe__identificacion", flat=True)[0]))
    
    list_mensaje.sort(key = len, reverse=True)
    resultados["mensaje_largo"] = (list_mensaje[0], len(list_mensaje[0]), datosusuario.objects.get(identificacion = con_principal.filter(mensaje = list_mensaje[0]).values_list("usuario_recibe__identificacion", flat=True)[0]))

    list_entregas = list(con_principal.values_list("usuario_recibe__identificacion", flat=True))
    resultados["usuario_mas_recibio"] = (datosusuario.objects.get(identificacion = mode(list_entregas)), list_entregas.count(mode(list_entregas)))

    list_entregas_areas = list(EntregaMoneda.objects.all().values_list("usuario_recibe__area", flat=True))
    resultados["area_querida"] = (mode(list_entregas_areas), list_entregas_areas.count(mode(list_entregas_areas)))

    return resultados


def mandar_email(mensaje, cabeza, recibe):

    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Construimos el mensaje simple
    
    mensaje = mensaje

    mensaje['From']=settings.EMAIL_HOST_USER
    mensaje['To']= recibe
    mensaje['Subject']=cabeza


    # Envio del mensaje

    mailServer.sendmail(settings.EMAIL_HOST_USER,
                    recibe,
                    mensaje.as_string())


def email_canje_rrhh(usuario, premio, monedas):

    rrhh = "am@linkinversiones.com.ar"

    #rrhh = "abel.robra.93@gmail.com"

    cabeza = "{} realizo un canje".format(usuario)

    mensaje = MIMEText("""
                
Hola!,

{} acaba de canjear Linkcoins, el premio es {} que costó {} monedas.

Podrás visualizarlo en el panel de seguimiento. Cualquier duda, comunicate con el equipo de IT.

Saludos!

-- Link-Help 


                    
                    """.format(usuario, premio, monedas))

    mandar_email(mensaje, cabeza, rrhh)

def email_canje_usuario(email, usuario, premio, monedas):

    rrhh = email

    cabeza = "Realizaste un canje de Linkcoins".format(usuario)

    mensaje = MIMEText("""
                    
¡Hola!,

Acabas canjear {}  Linkcoins por el siguiente premio: {}.

El equipo de RRHH te notificará cuando el mismo esté disponible para retirarlo (esta gestión puede tomar hasta 10 días hábiles posteriores a la fecha límite de canje).

Si hubiera algún problema del sistema, comunicate con el equipo de IT para solucionarlo.

Saludos,

-- Link-Help 

                
                    """.format(monedas, premio))

    mandar_email(mensaje, cabeza, rrhh)
