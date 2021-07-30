import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from agenda import settings

def mandar_email(mensaje, email, titulo):

    # Establecemos conexion con el servidor smtp de gmail
    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    mensaje = MIMEText("""{}""".format(mensaje))

    mensaje['From'] = settings.EMAIL_HOST_USER
    mensaje['To'] = email
    mensaje['Subject'] = titulo

    # Envio del mensaje

    mailServer.sendmail(settings.EMAIL_HOST_USER,
                    email,
                    mensaje.as_string())

