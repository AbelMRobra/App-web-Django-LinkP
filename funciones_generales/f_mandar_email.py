import smtplib
from agenda import settings


def mandar_email(msg, email, titulo):

    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    
    mensaje = msg
    mensaje['From'] = settings.EMAIL_HOST_USER
    mensaje['To'] = email
    mensaje['Subject'] = titulo

    # Envio del mensaje

    enviar=mailServer.sendmail(settings.EMAIL_HOST_USER,
                    email,
                    mensaje.as_string())
