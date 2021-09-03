from django.shortcuts import render, redirect
from rrhh.models import EntregaMoneda, datosusuario, CanjeMonedas, PremiosMonedas, MonedaLink
from statistics import mode
from .functions_linkcoins import estadisticasLinkcoin, email_canje_rrhh, email_canje_usuario
from datetime import date, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from agenda import settings
from .functions import saludo

def canjerealizados(request):

    # Listado de los datos de los premios

    context = {}
    context['mensaje_bievenida'] = saludo().format(request.user.first_name)
    context['data_linkcoins'] = estadisticasLinkcoin()

    if request.method == 'POST':

        try:

            canje = CanjeMonedas.objects.get(id = int(request.POST['ENTREGADO']))
            canje.entregado = "SI"
            canje.save()

        except:

            number = 1

            vueltas = int(request.POST['cantidad'])

            for i in range(vueltas):

                nuevas_monedas = MonedaLink(
                    nombre = str(date.today()) + "LINK" + str(datosusuario.objects.get(id = request.POST['usuario']).identificacion) + str(number),
                    usuario_portador = datosusuario.objects.get(identificacion = request.user.username),
                    fecha = date.today(),
                    tipo = "REGALO DE LINK"
                )

                nuevas_monedas.save()

                number += 1

                entrega = EntregaMoneda(
                    moneda = nuevas_monedas,
                    fecha = date.today(),
                    usuario_recibe = datosusuario.objects.get(id = request.POST['usuario']),
                    mensaje = request.POST['mensaje']

                )

                entrega.save()


    data_generador = []

    usuarios_recibieron_generador = EntregaMoneda.objects.filter(moneda__nombre__icontains = "LINK").values_list("usuario_recibe__identificacion", flat = True).distinct()

    for user in usuarios_recibieron_generador:
        mommentos = EntregaMoneda.objects.filter(moneda__nombre__icontains = "LINK", usuario_recibe__identificacion = user).values_list("mensaje", flat = True).distinct()
        for m in mommentos:
            cantidad = len(EntregaMoneda.objects.filter(moneda__nombre__icontains = "LINK", usuario_recibe__identificacion = user, mensaje = m))
            data_generador.append((datosusuario.objects.get(identificacion = user), cantidad, m))

    
    
    context['data'] = CanjeMonedas.objects.all().order_by("entregado")
    context['list_usuarios'] = datosusuario.objects.all().order_by("identificacion").exclude(estado = "NO ACTIVO")
    context['data_generador'] = data_generador


    return render(request, "linkcoins/canjesrealizados.html", context)

def generador_linkcoins(request):

    data_generador = []

    usuarios_recibieron_generador = EntregaMoneda.objects.filter(moneda__nombre__icontains = "LINK").values_list("usuario_recibe__identificacion", flat = True).distinct()

    for user in usuarios_recibieron_generador:
        mommentos = EntregaMoneda.objects.filter(moneda__nombre__icontains = "LINK", usuario_recibe__identificacion = user).values_list("mensaje", flat = True).distinct()
        for m in mommentos:
            cantidad = len(EntregaMoneda.objects.filter(moneda__nombre__icontains = "LINK", usuario_recibe__identificacion = user, mensaje = m))
            data_generador.append((datosusuario.objects.get(identificacion = user), cantidad, m))

    

    context = {}
    context['data_generador'] = data_generador
    context['mensaje_bievenida'] = saludo().format(request.user.first_name)

    return render(request, "linkcoins/generador_linkcoins.html", context)



def canjemonedas(request):

    context = {}

    usuario = datosusuario.objects.get(identificacion = request.user)

    monedas_recibidas = len(EntregaMoneda.objects.filter(usuario_recibe = usuario))

    monedas_canjear = monedas_recibidas - sum(CanjeMonedas.objects.filter(usuario = usuario).values_list("monedas", flat=True))

    if request.method == 'POST':

        try:

            today = date.today()

            if today.day <= 10:

                premio_solicitado = PremiosMonedas.objects.get(id = int(request.POST['premio']))

                if monedas_canjear >= premio_solicitado.cantidad:

                    canje = CanjeMonedas(
                        usuario = usuario,
                        fecha = date.today(),
                        premio = str(premio_solicitado.nombre),
                        monedas = int(premio_solicitado.cantidad),
                    )

                    canje.save()

                    email_canje_rrhh(usuario, canje.premio, canje.monedas)
                    email_canje_usuario(usuario.email, usuario, canje.premio, canje.monedas)


                    context['canje_realizado'] = True 

                else:
                    context['mensaje'] = "No tienes suficientes monedas para canjear el premio seleccionado"

            else:

                context['mensaje'] = "Solo puedes canjear hasta el dia 10 de cada mes"

        except:

            pass

        try:

            if request.POST['id'] != "0":
                premio = PremiosMonedas.objects.get(id = int(request.POST['id']))
                premio.nombre = request.POST['nombre']
                premio.cantidad = request.POST['cantidad']
                premio.save()

            

            else:
                b = PremiosMonedas(
                    nombre = request.POST['nombre'],
                    cantidad = int(request.POST['cantidad']),
                )

                b.save()

        except:

            pass

        try:

            premio = PremiosMonedas.objects.get(id = int(request.POST['borrar']))
            premio.delete()


        except:

            pass


    premios = PremiosMonedas.objects.all().order_by("nombre")

    monedas = MonedaLink.objects.filter(usuario_portador = usuario)

    monedas_recibidas = len(EntregaMoneda.objects.filter(usuario_recibe = usuario))

    monedas_canjear = monedas_recibidas - sum(CanjeMonedas.objects.filter(usuario = usuario).values_list("monedas", flat=True))

    monedas_disponibles = 0
    
    for m in monedas:

        if len(EntregaMoneda.objects.filter(moneda = m)) == 0:

            monedas_disponibles += 1

    dato_monedas = {'monedas_recibidas':monedas_recibidas, 'monedas_disponibles':monedas_disponibles, 'monedas':monedas, 'monedas_canjear':monedas_canjear}
  
    context['premios'] = premios
    context['dato_monedas'] = dato_monedas

    return render(request, "linkcoins/canjemonedas.html", context)

