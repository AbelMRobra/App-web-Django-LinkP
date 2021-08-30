from django.shortcuts import render, redirect
from rrhh.models import EntregaMoneda, datosusuario, CanjeMonedas
from statistics import mode
from .functions_linkcoins import estadisticasLinkcoin

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

    mensaje = ""

    usuario = datosusuario.objects.get(identificacion = request.user)

    monedas_recibidas = len(EntregaMoneda.objects.filter(usuario_recibe = usuario))

    monedas_canjear = monedas_recibidas - sum(CanjeMonedas.objects.filter(usuario = usuario).values_list("monedas", flat=True))

    if request.method == 'POST':

        try:

            today = date.today()

            if today.day <= 10:

                rrhh = "am@linkinversiones.com.ar"

                premio_solicitado = PremiosMonedas.objects.get(id = int(request.POST['premio']))

                if monedas_canjear >= premio_solicitado.cantidad:

                    canje = CanjeMonedas(
                        usuario = usuario,
                        fecha = datetime.date.today(),
                        premio = str(premio_solicitado.nombre),
                        monedas = int(premio_solicitado.cantidad),
                    )

                    canje.save()

                    # Establecemos conexion con el servidor smtp de gmail
                    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.ehlo()
                    mailServer.starttls()
                    mailServer.ehlo()
                    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                    # Construimos el mensaje simple
                    
                    mensaje = MIMEText("""
                
Hola!,

{} acaba de canjear Linkcoins, el premio es {} que costó {} monedas.

Podrás visualizarlo en el panel de seguimiento. Cualquier duda, comunicate con el equipo de IT.

Saludos!

-- Link-Help 


                    
                    """.format(usuario, canje.premio, canje.monedas))
                    mensaje['From']=settings.EMAIL_HOST_USER
                    mensaje['To']= rrhh
                    mensaje['Subject']="{} realizo un canje".format(usuario)


                    # Envio del mensaje

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                    rrhh,
                                    mensaje.as_string())

                    # Establecemos conexion con el servidor smtp de gmail
                    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                    mailServer.ehlo()
                    mailServer.starttls()
                    mailServer.ehlo()
                    mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                    # Construimos el mensaje simple
                    
                    mensaje = MIMEText("""
                    
¡Hola!,

Acabas canjear {}  Linkcoins por el siguiente premio: {}.

El equipo de RRHH te notificará cuando el mismo esté disponible para retirarlo (esta gestión puede tomar hasta 10 días hábiles posteriores a la fecha límite de canje).

Si hubiera algún problema del sistema, comunicate con el equipo de IT para solucionarlo.

Saludos,

-- Link-Help 

                
                    """.format(canje.monedas, canje.premio))
                    mensaje['From']=settings.EMAIL_HOST_USER
                    mensaje['To']= usuario.email
                    mensaje['Subject']="Realizaste un canje de Linkcoins".format(usuario)


                    # Envio del mensaje

                    mailServer.sendmail(settings.EMAIL_HOST_USER,
                                    usuario.email,
                                    mensaje.as_string())


                    return redirect('Canje de monedas')

                else:
                    mensaje = "No tienes suficientes monedas para canjear el premio seleccionado"

            else:

                mensaje = "Solo puedes canjear hasta el dia 10 de cada mes"

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
  
    return render(request, "users/canjemonedas.html", {'mensaje':mensaje, "premios":premios, 'dato_monedas':dato_monedas})

