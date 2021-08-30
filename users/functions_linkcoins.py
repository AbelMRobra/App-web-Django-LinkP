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
    print(resultados["mensaje_largo"])
    list_entregas = list(con_principal.values_list("usuario_recibe__identificacion", flat=True))
    resultados["usuario_mas_recibio"] = (datosusuario.objects.get(identificacion = mode(list_entregas)), list_entregas.count(mode(list_entregas)))

    list_entregas_areas = list(EntregaMoneda.objects.all().values_list("usuario_recibe__area", flat=True))
    resultados["area_querida"] = (mode(list_entregas_areas), list_entregas_areas.count(mode(list_entregas_areas)))

    return resultados