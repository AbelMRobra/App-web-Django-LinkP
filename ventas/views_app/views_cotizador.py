import datetime
import os
import smtplib
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse 
from xhtml2pdf import pisa
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.template.loader import get_template
from django.shortcuts import render, redirect
from proyectos.models import Unidades
from presupuestos.models import Constantes
from ventas.models import FeaturesUni, ImgEnlacesProyecto, Clientescontacto
from crm.models import Consulta, Tipologia
from rrhh.models import datosusuario
from ventas.functions_unidades import calculo_m2_unidad, cliente_crm, plan_financiacion_cotizador, info_para_cotizador


def cotizador(request, id_unidad):

    context = {}

    datos = Unidades.objects.get(id = id_unidad)
    today = datetime.date.today()

    m2 = calculo_m2_unidad(datos)

    precio_contado = m2*datos.proyecto.desde

    features_unidad = FeaturesUni.objects.filter(unidad = datos)

    for f2 in features_unidad:

        precio_contado = precio_contado*f2.feature.inc

    desde = round((precio_contado/m2), 4)

    if request.method == 'POST':

        try:
            context["cliente"] = cliente_crm(request.POST['email'], nombre = request.POST['nombre'], apellido = request.POST['apellido'], telefono = request.POST['telefono'])

        except:

            context["cliente"] = cliente_crm(request.POST['email'])

        context["resultados"] = plan_financiacion_cotizador(request.POST["anticipo"], request.POST["cuotas_esp"], request.POST["aporte"], request.POST["cuotas_p"], request.POST['observacion'], request.POST['descuento'], precio_contado, datos)

        context["info_coti_email"] = info_para_cotizador(context["resultados"])

    
    context["imagenes_carru"] = ImgEnlacesProyecto.objects.filter(proyecto = datos.proyecto)
    context["tiempo_restante"] = (datos.proyecto.fecha_f.year - today.year)*12 + (datos.proyecto.fecha_f.month - today.month)
    context["datos"] = datos
    context["precio_contado"] = precio_contado
    context["m2"] = m2

    return render(request, 'cotizador/cotizador_principal.html', context)

class PDF_cotizacion(View):

    def link_callback(self, uri, rel):

            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

            # make sure that file exists
            if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
            return path

    def get(self, request, id_unidad, id_cliente, info_coti, *args, **kwargs):

        #Creamos la información

        cliente = Clientescontacto.objects.get(id = id_cliente)
        unidad = Unidades.objects.get(id = id_unidad)
        features_unidad = FeaturesUni.objects.filter(unidad = unidad)
        valor_hormigon = Constantes.objects.get(id = 7)

        today = datetime.date.today()

        # Saludo de bienvenida

        saludo = saludo_bienvenida(cliente)

        # Calculo de datos

        m2 = calculo_m2_unidad(unidad)

        precio_contado = m2*unidad.proyecto.desde

        features_unidad = FeaturesUni.objects.filter(unidad = unidad)

        for f2 in features_unidad:

            precio_contado = precio_contado*f2.feature.inc

        datos_recibidos_back = info_coti.split("&")

        datos_para_calculo_cotizacion = {
            "anticipo":float(datos_recibidos_back[3]),
            "cuotas_espera":datos_recibidos_back[0],
            "aporte":datos_recibidos_back[1],
            "cuotas_posesion":datos_recibidos_back[2],
            "observacion":"",
            "descuento":datos_recibidos_back[4]
        }

        datos_cotizacion = plan_financiacion_cotizador(datos_para_calculo_cotizacion["anticipo"], 
        datos_para_calculo_cotizacion["cuotas_espera"], 
        datos_para_calculo_cotizacion["aporte"], 
        datos_para_calculo_cotizacion["cuotas_posesion"], 
        datos_para_calculo_cotizacion['observacion'], 
        datos_para_calculo_cotizacion['descuento'], 
        precio_contado, unidad)

        datos_cotizacion_json = {
            "anticipo":datos_cotizacion[0],
            "anticipo_en_hormigon":datos_cotizacion[1],
            "precio_financiado":datos_cotizacion[2],
            "cuotas_espera":datos_cotizacion[3],
            "importe_del_aporte":datos_cotizacion[4],
            "cuotas_posesion":datos_cotizacion[5],
            "importe_de_las_cuotas_espera":datos_cotizacion[6],
            "aporte":datos_cotizacion[7],
            "importe_de_las_cuotas_posesion":datos_cotizacion[8],
            "importe_de_las_cuotas_posesion_en_hormigon":datos_cotizacion[9],
            "importe_de_las_cuotas_espera_en_hormigon":datos_cotizacion[10],
            "importe_del_aporte_en_hormigon":datos_cotizacion[11],
            "valor_de_la_cuota_espera":datos_cotizacion[12],
            "valor_de_la_cuota_entrega":datos_cotizacion[13],
            "valor_de_la_cuota_posesion":datos_cotizacion[14],
            "observacion":datos_cotizacion[15],
            "descuento":datos_cotizacion[16],
            "total_en_pesos":datos_cotizacion[17],
            "total_en_hormigon":datos_cotizacion[18],
            "precio_de_contado":datos_cotizacion[19],
        }

        # Aqui llamamos y armamos el PDF
      
        template = get_template('cotizador/cotizador_PDF.html')

        contexto = {'cliente':cliente, 
        'unidad':unidad, 
        'datos_cotizacion_json':datos_cotizacion_json,
        'today':today, 
        'logo':'{}{}'.format(settings.STATIC_URL, 'img/link.png'),
        'cabecera':'{}{}'.format(settings.STATIC_URL, 'img/fondo.png'),
        'fondo':'{}{}'.format(settings.STATIC_URL, 'img/fondo.jpg')}

        html = template.render(contexto)
        response = HttpResponse(content_type = "application/pdf")
        
        #response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        
        pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
        
        if pisaStatus.err:
            
            return HttpResponse("Hay un error")

        datos_email = {
            "saludo":saludo,
            "cliente":cliente,
            "unidad":unidad,
            "response":response
        }

        enviar_email = cotizacion_email_cliente(datos_email)

        cotizacion = "cotizacion{}{}.pdf".format(str(cliente.nombre).replace(" ", ""), today)

        # Creo la consulta

        usuario = datosusuario.objects.get(identificacion = request.user.username)

        try:

            tipologia = Tipologia.objects.get(nombre = unidad.tipologia)
        except:

            tipologia = Tipologia(
                nombre = unidad.tipologia
            )
            tipologia.save()

        datos_consulta = {
            "unidad":unidad,
            "cliente":cliente,
            "usuario":usuario,
            "cotizacion":cotizacion,
            "tipologia":tipologia,
        }

        guardar_consulta = cotizacion_consultas_guardar(datos_consulta)

        return redirect('modificarcliente', id = cliente.id)

def cotizacion_consultas_guardar(datos_consulta):

    today = datetime.date.today()

    try:

        new_consulta = Consulta(
            fecha = today,
            proyecto = datos_consulta['unidad'].proyecto,
            cliente = datos_consulta['cliente'],
            medio_contacto = 'RECOMENDACION',
            usuario = datos_consulta['usuario'],
            adjunto_propuesta = (datos_consulta['cotizacion']),
        )

        new_consulta.save()
        new_consulta.tipologia2.add(datos_consulta['tipologia'])
        new_consulta.save()
        
        return "Consulta guardada correctamente"

    except:

        return "Error al crear la consulta"

def cotizacion_email_cliente(datos_email):

    try:

        today = datetime.date.today()

        # Establecemos conexion con el servidor smtp de gmail

        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Construimos el mensaje simple
        
        mensaje = MIMEMultipart()
        mensaje.attach(MIMEText(cuerpo_email_cotizacion(datos_email["saludo"]), 'plain'))
        mensaje['From']=settings.EMAIL_HOST_USER
        mensaje['To']=datos_email["cliente"].email
        mensaje['Subject']="LINK - Tu cotización {}".format(datos_email["cliente"].nombre)

        # Esta es la parte para adjuntar
        
        mRoot = settings.MEDIA_ROOT

        if datos_email["unidad"].plano_venta:

            plano_adjunto = open(mRoot + "/{}".format(datos_email["unidad"].plano_venta.name), 'rb')
            adjunto_MIME = MIMEBase('application', "octet-stream")
            adjunto_MIME.set_payload(plano_adjunto.read())
            encoders.encode_base64(adjunto_MIME)
            adjunto_MIME.add_header('Content-Disposition', 'attachment; filename="Plano de la unidad.pdf"')
            mensaje.attach(adjunto_MIME)


        adjunto_MIME = MIMEBase('application', "octet-stream")
        adjunto_MIME.set_payload(datos_email["response"].content)
        encoders.encode_base64(adjunto_MIME)
        adjunto_MIME.add_header('Content-Disposition', 'attachment; filename="Tu_cotizacion.pdf"')
        mensaje.attach(adjunto_MIME)
        
        with open(mRoot + "/cotizacion{}{}.pdf".format(datos_email["cliente"].nombre, today).replace(" ", ""), 'wb') as f:
            f.write(datos_email["response"].content)
        
        name_coti_adjunta = "cotizacion{}{}.pdf".format(str(datos_email["cliente"].nombre).replace(" ", ""), today)

        # Envio del mensaje
        
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                        datos_email["cliente"].email,
                        mensaje.as_string())

        return "Email enviado correctamente"

    except:

        return "Error inesperado al tratar de enviar el email"

def saludo_bienvenida(cliente):

    hora_actual = datetime.datetime.now()
        
    if hora_actual.hour >= 20:
        saludo = "¡Buenas noches {}!".format(cliente.nombre)
    elif hora_actual.hour >= 13:
        saludo = "¡Buenas tardes {}!".format(cliente.nombre)
    else:
        saludo = "¡Buen dia {}!".format(cliente.nombre)

    return saludo

def cuerpo_email_cotizacion(saludo):
    return """
    
    {}

    Enviamos la cotización de hoy!, cualquier consulta no dudes en comunicarte con nosotros

    Ingresa a www.linkinversiones.com.ar para mas información

    LINK Desarrollos inmobilairios
    Vos confias porque nosotros cumplimos

    Por favor no responder este email
    
    """.format(saludo)
