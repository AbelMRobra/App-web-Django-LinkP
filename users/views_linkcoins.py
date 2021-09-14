from django.shortcuts import render, redirect
from rrhh.models import EntregaMoneda, datosusuario, CanjeMonedas, PremiosMonedas, MonedaLink
from statistics import mode
from .functions_linkcoins import estadisticasLinkcoin, email_canje_rrhh, email_canje_usuario,aviso_regalo_link
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
        datos=request.POST.dict()

        if 'ENTREGADO' in datos:
            canje = CanjeMonedas.objects.get(id = int(datos['ENTREGADO']))
            canje.entregado = "SI"
            canje.save()

            return redirect('Canjes realizados')

    
    context['data'] = CanjeMonedas.objects.all().order_by("entregado")



    return render(request, "linkcoins/canjesrealizados.html", context)

def generador_linkcoins(request):

    if request.method == 'POST':
        datos=request.POST.dict()

        if 'generar' in datos:
            cant = int(datos['cantidad']) + 1
            mens = datos['mensaje']
    
            destino = datosusuario.objects.get(id = datos['usuario'])
            for i in range(1,cant):

                nueva_moneda = MonedaLink(
                    nombre = str(date.today()) + "LINK" + str(datosusuario.objects.get(id = datos['usuario']).identificacion) + str(i),
                    usuario_portador = datosusuario.objects.get(identificacion = request.user.username),
                    fecha = date.today(),
                    tipo = "REGALO DE LINK"
                )
                nueva_moneda.save()

                entrega = EntregaMoneda(
                    moneda = nueva_moneda,
                    fecha = date.today(),
                    usuario_recibe = destino,
                    mensaje = mens,

                )
                entrega.save()

            try:
                cant=cant-1
                aviso_regalo_link(destino.email,cant,mens)
            except:
                mensaje='No se pudo enviar el email'
                
            return redirect('Generador')
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
    context['list_usuarios'] = datosusuario.objects.all().order_by("identificacion").exclude(estado = "NO ACTIVO")

    return render(request, "linkcoins/generador_linkcoins.html", context)



def canjemonedas(request):

    context = {}

    canjes=CanjeMonedas.objects.all()
    premios=PremiosMonedas.objects.all()

    usuario = datosusuario.objects.get(identificacion = request.user)

    monedas_recibidas = EntregaMoneda.objects.filter(usuario_recibe = usuario).count()

    monedas_canjear = monedas_recibidas - sum(canjes.filter(usuario = usuario).values_list("monedas", flat=True))

    mensaje = ''
    
    if request.method == 'POST':
        datos=request.POST.dict()
     
        

        today = date.today()

        if 'premio' in datos:
            premio=datos['premio']

            if today.day <= 20:

                premio_solicitado = premios.get(id = int(premio))

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
                    mensaje="No tienes suficientes monedas para canjear el premio seleccionado"
              
  

            else:
                mensaje="Solo puedes canjear hasta el dia 10 de cada mes"
  

        

        if  'id' in datos:
            
            if datos['id'] != "0":
                premio = premios.get(id = int(datos['id']))
                premio.nombre = datos['nombre']
                premio.cantidad = datos['cantidad']
                premio.save()

        

            else:
                b = PremiosMonedas(
                    nombre = datos['nombre'],
                    cantidad = int(datos['cantidad']),
                )

                b.save()

        

        if 'borrar' in datos:
            premio=datos['borrar']

            premio = premios.get(id = int(premio))
            premio.delete()



    premios = premios.order_by("nombre")

    monedas = MonedaLink.objects.filter(usuario_portador = usuario)

    monedas_recibidas = EntregaMoneda.objects.filter(usuario_recibe = usuario).count()

    monedas_canjear = monedas_recibidas - sum(canjes.filter(usuario = usuario).values_list("monedas", flat=True))
    
    
    monedas_disponibles = sum([1 for m in monedas if EntregaMoneda.objects.filter(moneda = m).count() == 0])


    dato_monedas = {'monedas_recibidas':monedas_recibidas, 'monedas_disponibles':monedas_disponibles, 'monedas':monedas, 'monedas_canjear':monedas_canjear}
  
    context['premios'] = premios
    context['dato_monedas'] = dato_monedas
    context['mensaje'] = mensaje

    return render(request, "linkcoins/canjemonedas.html", context)

