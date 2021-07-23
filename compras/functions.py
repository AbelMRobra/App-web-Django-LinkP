from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from agenda import settings
import smtplib

import requests

def sendemail(mensaje,asunto,usuario):
   
    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)


    mensaje['From']=settings.EMAIL_HOST_USER
    mensaje['To']=usuario
    mensaje['Subject']=asunto


    # Envio del mensaje

    mailServer.sendmail(settings.EMAIL_HOST_USER,
                    usuario,
                    mensaje.as_string())


def bot(send):
    id = "-585663986"

    token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"
    url = "https://api.telegram.org/bot" + token + "/sendMessage"

    params = {
        'chat_id' : id,
        'text' : send
    }

    requests.post(url, params=params)
