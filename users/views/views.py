import os
import datetime
import requests
from datetime import date
import pandas as pd
import numpy as np
from statistics import mode
from xhtml2pdf import pisa
from statistics import mode
import smtplib
from email.mime.text import MIMEText


from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth import models


from agenda import settings

from finanzas.models import Almacenero, RegistroAlmacenero, Arqueo, RetirodeSocios, Honorarios
from presupuestos.models import Presupuestos, InformeMensual, TareasProgramadas, Bitacoras
from proyectos.models import Proyectos, Unidades
from ventas.models import VentasRealizadas
from compras.models import Compras, Comparativas, AvisoOrdenesCompras
from registro.models import RegistroValorProyecto
from rrhh.models import datosusuario, mensajesgenerales, NotaDePedido, Vacaciones, MonedaLink, EntregaMoneda, Anuncios, Seguimiento, Minutas, Acuerdos, PremiosMonedas, Logros, RegistroContable, CanjeMonedas, DicRegistroContable, ArqueoChanchito


from users.models import Atajos
from users.funciones.functions import Avisos


class PdfMinutas(View):

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

    def get(self, request, id_minuta, *args, **kwargs):

        #Creamos la información

        minuta = Minutas.objects.get(id = id_minuta)

        acuerdos = Acuerdos.objects.filter(minuta = minuta)

        # Aqui llamamos y armamos el PDF
      
        template = get_template('minutas/pdfminuta.html')
        contexto = {'minuta':minuta, 
        'acuerdos':acuerdos, 
        'fecha':datetime.date.today(),
        'logo':'{}{}'.format(settings.STATIC_URL, 'img/Linkp.png'),
        'cabecera':'{}{}'.format(settings.STATIC_URL, 'img/fondo.png'),
        'fondo':'{}{}'.format(settings.STATIC_URL, 'img/fondo.jpg')}
        html = template.render(contexto)
        response = HttpResponse(content_type = "application/pdf")
        
        #response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        
        pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
        
        if pisaStatus.err:
            
            return HttpResponse("Hay un error")

        return response

def linkp(request):

    try:
        user = datosusuario.objects.get(identificacion = request.user.username)

        if len(Logros.objects.filter(usuario = user, nombre = "Curioso")) == 0:

            b = Logros(
                usuario = user,
                nombre = "Curioso",
                descrip = "Encontraste una pagina secreta ;)"
            )

            b.save()
    except:
        pass

    return render(request, 'users/linkp.html')


def vacaciones(request):

    # Determinamos las fechas

    hoy = datetime.date.today()

    if hoy.month < 4:

        abril = datetime.date(hoy.year, 4, 1)
        marzo = datetime.date(hoy.year, 3, 1)
        febrero = datetime.date(hoy.year, 2, 1)
        enero = datetime.date(hoy.year, 1, 1)
        diciembre = datetime.date((hoy.year - 1), 12, 1)
        noviembre = datetime.date((hoy.year - 1), 11, 1)
        octubre = datetime.date((hoy.year - 1), 10, 1)

        fechas = [octubre, noviembre, diciembre, enero, febrero, marzo, abril]

        datos = Vacaciones.objects.filter(fecha_inicio__gte = octubre, fecha_final__lte = abril)
           
    return render(request, "users/holidays.html", {'fechas':fechas, 'datos':datos})

def password(request):

    mensaje = 0

    if request.method == 'POST':

        usuario = User.objects.get(id = request.user.id)
        
        usuario.set_password(request.POST["password"])

        usuario.save()

        mensaje = 1

    return render(request, "users/password.html", {'mensaje':mensaje})



def dashboard(request):

    # En esta parte resolvemos el grafico del arqueo

    data_cruda = Arqueo.objects.order_by("-fecha")

    fecha = data_cruda[0].fecha

    data = data_cruda[0]

    data_frame = pd.read_excel(data.arqueo)

    array_usd = np.array(data_frame['USD'])

    usd = sum(array_usd)

    array_euro = np.array(data_frame['EUROS'])

    euro = sum(array_euro)

    nombre_columnas = data_frame.columns

    banco = 0

    for n in nombre_columnas:

        if "BANCO" in n:

            banco = banco + sum(np.array(data_frame[n]))


    array_pesos = np.array(data_frame['EFECTIVO'])

    pesos = sum(array_pesos)

    array_cheques = np.array(data_frame['CHEQUES'])

    cheques = sum(array_cheques)

    array_me = np.array(data_frame['MONEDA EXTRANJERA'])

    me = sum(array_me)

    consolidado = pesos + cheques + me + banco

    porcentaje_pesos = pesos/consolidado*100
    porcentaje_banco = banco/consolidado*100
    porcentaje_cheques = cheques/consolidado*100
    porcentaje_me = me/consolidado*100

    arqueo = [fecha, consolidado, porcentaje_pesos, porcentaje_me, porcentaje_cheques, porcentaje_banco, usd, euro]


    #Calculos para tablero de avance de presupuesto

    barras = []

    datos_barras = Presupuestos.objects.order_by("-saldo").exclude(proyecto__nombre = "DIANCO - LAMADRID 1137")

    for db in datos_barras:

        if db.valor != 0:

            avance = (100 - db.saldo/db.valor*100)

            barras.append((db, int(avance)))

    barras = sorted(barras,reverse=True, key=lambda tup: tup[1])


    #Calculos para tablero de ventas

    proyectos = Proyectos.objects.all()

    ventas_barras = []

    for p in proyectos:

        total_unidades = Unidades.objects.filter(proyecto = p, asig = "PROYECTO")

        unidades_vendidas = Unidades.objects.filter(proyecto = p, asig = "PROYECTO").exclude(estado = "DISPONIBLE")

        if len(total_unidades) != 0:

            avance = (len(unidades_vendidas)/len(total_unidades))*100

            ventas_barras.append((p, int(avance)))

    ventas_barras = sorted(ventas_barras, reverse=True, key=lambda tup: tup[1])

    date = datetime.date.today()

    fecha_inicio = date - datetime.timedelta(days=90)

    ventas_realizadas = len(VentasRealizadas.objects.filter(fecha__gt = fecha_inicio))


    #Calculo para compras

    compras = Compras.objects.filter(fecha_c__gt = fecha_inicio)

    comprado = 0
    estimado = 0

    for c in compras:
        comprado = comprado + c.cantidad*c.precio
        estimado = estimado + c.cantidad*c.precio_presup

    if estimado == 0:

        diferencia = 0

    else:

        diferencia = (comprado/estimado-1)*100

    datos_compras = [comprado, estimado, diferencia]


    #Calculo para unidades

    deptos_disp = len(Unidades.objects.filter(estado = "DISPONIBLE", tipo = "DEPARTAMENTO", asig = "PROYECTO"))
    cocheras_disp = len(Unidades.objects.filter(estado = "DISPONIBLE", tipo = "COCHERA", asig = "PROYECTO"))

    datos_unidades = [deptos_disp, cocheras_disp]


    # -----------------> Aqui calculo indice LINK

    datos = Almacenero.objects.all()

    datos_completos = []
    datos_finales = []

    saldo_caja_total = 0
    pendiente_gastar_total = 0
    ingresos_total = 0
    descuento_total = 0

    for dato in datos:

        presupuesto = "NO"

        pricing = "NO"

        almacenero = dato

        presupuesto = Presupuestos.objects.get(proyecto = dato.proyecto)

        # Aqui calculo el IVA sobre compras

        iva_compras = (presupuesto.imprevisto + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.credito + presupuesto.fdr)*0.07875

        almacenero.pendiente_iva_ventas = iva_compras

        almacenero.save()

        # Calculo el resto de las cosas

        retiro_socios = sum(np.array(RetirodeSocios.objects.values_list('monto_pesos').filter(proyecto = dato.proyecto)))
        saldo_caja = almacenero.cuotas_cobradas - almacenero.gastos_fecha - almacenero.Prestamos_dados
        saldo_caja_total = saldo_caja_total + saldo_caja
        pend_gast = almacenero.pendiente_admin + almacenero.pendiente_comision + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.imprevisto + presupuesto.credito + presupuesto.fdr - almacenero.pendiente_adelantos + almacenero.pendiente_iva_ventas + almacenero.pendiente_iibb_tem +almacenero.cheques_emitidos
        pendiente_gastar_total = pendiente_gastar_total + pend_gast
        prest_cobrar = almacenero.prestamos_proyecto + almacenero.prestamos_otros
        total_ingresos = prest_cobrar + almacenero.cuotas_a_cobrar + almacenero.ingreso_ventas + saldo_caja
        ingresos_total = ingresos_total + total_ingresos
        margen = total_ingresos - pend_gast
        descuento = almacenero.ingreso_ventas*0.06
        descuento_total = descuento_total + descuento
        margen_2 = margen - descuento 
               
        datos_completos.append((dato, saldo_caja, pend_gast, total_ingresos, margen, descuento, margen_2))

    # -----------------> Aqui calculo los totalizadores

    margen1_total = ingresos_total - pendiente_gastar_total
    margen2_total = margen1_total - descuento_total


    # -----------------> Aqui calculo la parte de honorarios

    honorarios = Honorarios.objects.order_by("-fecha")
    caja_actual = honorarios[0].caja_actual
    subtotal_1 = honorarios[0].cuotas + honorarios[0].ventas
    ingresos = subtotal_1 + honorarios[0].creditos
    comision = honorarios[0].comision_venta*honorarios[0].ventas
    subtotal_2 = honorarios[0].estructura_gio + honorarios[0].aportes + honorarios[0].socios + comision
    costos = subtotal_2  + honorarios[0].deudas
    honorario = ingresos - costos + honorarios[0].caja_actual
    honorarios2 = honorario

    # -----------------> Aqui calculo los totalizadores con los honorarios

    caja_total = caja_actual + saldo_caja_total
    costos_totales = pendiente_gastar_total + costos
    ingresos_totales = ingresos_total + ingresos
    margen1_completo = margen1_total

    # -----------------> Información para graficos

    retiro_honorarios = 0
    honorarios_beneficio2 = 0
    honorarios_beneficio1 = 0

    datos_finales.append((saldo_caja_total , pendiente_gastar_total, ingresos_total, descuento_total, margen1_total, margen2_total))

    datos_finales_2 = [margen1_completo]


    # -----------------> Esta es la parte del historico

    datos_historicos = RegistroAlmacenero.objects.order_by("fecha")

    fechas = []

    for d in datos_historicos:

        if not d.fecha in fechas:

            fechas.append(d.fecha)

    datos_registro = []

    for fecha in fechas:

        datos = RegistroAlmacenero.objects.filter(fecha = fecha)

        saldo_caja_total = 0
        pendiente_gastar_total = 0
        ingresos_total = 0
        descuento_total = 0
        honorario = 0


        for dato in datos:

            almacenero = dato

            #Calculo el resto de las cosas

            retiro_socios = almacenero.retiro_socios
            saldo_caja = almacenero.cuotas_cobradas - almacenero.gastos_fecha - almacenero.Prestamos_dados
            
            pend_gast = almacenero.pendiente_admin + almacenero.pendiente_comision + almacenero.saldo_mat + almacenero.saldo_mo + almacenero.imprevisto + almacenero.credito + almacenero.fdr - almacenero.pendiente_adelantos + almacenero.pendiente_iva_ventas + almacenero.pendiente_iibb_tem +almacenero.cheques_emitidos
            
            prest_cobrar = almacenero.prestamos_proyecto + almacenero.prestamos_otros
            total_ingresos = prest_cobrar + almacenero.cuotas_a_cobrar + almacenero.ingreso_ventas + saldo_caja
            
            margen = total_ingresos - pend_gast
            descuento = almacenero.ingreso_ventas*0.06
            
            margen_2 = margen - descuento
            honorario = almacenero.honorarios

            pendiente_gastar_total = pendiente_gastar_total + pend_gast
            saldo_caja_total = saldo_caja_total + saldo_caja
            descuento_total = descuento_total + descuento
            ingresos_total = ingresos_total + total_ingresos

            # Me falta calcular la parte de honorarios


        margen1 = ingresos_total - pendiente_gastar_total

        datos_registro.append(margen1)


    return render(request, "users/dashboard.html", {"fechas":fechas, "datos_finales_2":datos_finales_2, "indice":margen1_completo, "datos_registro":datos_registro, "datos_barras":barras, "ventas_barras":ventas_barras, "ventas":ventas_realizadas, "datos_compras":datos_compras, "datos_unidades":datos_unidades, "arqueo":arqueo})

def inicio(request):

    context = {}
    context["todos_atajos"] = Atajos.objects.all()
    datos_vista_usuario = {}

    if request.method == 'POST':
        try:
            try:
                atajo_a_salir = Atajos.objects.get(id = int(request.POST["atajo_delete"]))
                atajo_a_salir.usuario.remove(datosusuario.objects.get(identificacion = request.user.username))
            except:
                atajo_a_entrar = Atajos.objects.get(id = int(request.POST["atajo_entrar"]))
                atajo_a_entrar.usuario.add(datosusuario.objects.get(identificacion = request.user.username))
        except:
            if request.POST['tutorial']:
                usuario = datosusuario.objects.get(identificacion = request.user.username)
                usuario.tutorial = "SI"
                usuario.save()


    #  Atajos
    try:

        usuario = datosusuario.objects.get(identificacion = request.user.username)
        atajos = Atajos.objects.filter(usuario = usuario)
        datos_vista_usuario["usuario"] = usuario
        datos_vista_usuario["atajos"] = atajos
        datos_vista_usuario["cantidad_atajos"] = len(Atajos.objects.filter(usuario = usuario))
    except:

        usuario = 0
        datos_vista_usuario["usuario"] = 0
        datos_vista_usuario["atajos"] = []
        datos_vista_usuario["cantidad_atajos"] = 0

    context["datos_vista_usuario"] = datos_vista_usuario

    # Saludo de bienvenida

    hora_actual = datetime.datetime.now()
    if hora_actual.hour >= 20:
        mensaje_bievenida = "¡Buenas noches {}!".format(request.user.first_name)
    elif hora_actual.hour >= 13:
        mensaje_bievenida = "¡Buenas tardes {}!".format(request.user.first_name)
    else:
        mensaje_bievenida = "¡Buen dia {}!".format(request.user.first_name)

    context["mensaje_bievenida"] = mensaje_bievenida

    # Seguimiento de proyectos

    data_proyecto_siguiendo = []
    if usuario:
        if usuario.proyecto:
            proyecto_siguiendo = usuario.proyecto
            if len(Presupuestos.objects.filter(proyecto = usuario.proyecto)) == 1:
                datos_presupuesto = Presupuestos.objects.filter(proyecto = usuario.proyecto)[0]
                try:
                    avance_proyecto = ((datos_presupuesto.valor - datos_presupuesto.saldo)/datos_presupuesto.valor)*100
                    pendiente_proyecto = 100 - avance_proyecto
                except:
                    avance_proyecto = 0
                    pendiente_proyecto = 100
                data_proyecto_siguiendo.append((usuario.proyecto, avance_proyecto, pendiente_proyecto))

    else:
        data_proyecto_siguiendo = 0
    
    datos_vista_usuario["data_proyecto_siguiendo"] = data_proyecto_siguiendo
    
    # La creación de monedas

    usuarios = datosusuario.objects.all().exclude(estado = "NO ACTIVO")

    hoy = datetime.date.today()
    fecha_control = datetime.date(hoy.year, hoy.month, 1)

    for u in usuarios:

        moneda = MonedaLink.objects.filter(usuario_portador = u, fecha__gte = fecha_control)

        if len(moneda) == 0:

            numero = 0

            for i in range(10):

                b = MonedaLink(
                    nombre = str(fecha_control)+str(u.identificacion)+str(numero),
                    usuario_portador = u,
                    fecha = fecha_control,
                    tipo = "NORMAL"
                )

                b.save()
                
                numero += 1

    # Esta es la parte de los permisos

    lista_grupos = 0

    grupos = request.user.groups.all()

    for g in grupos :

        lista_grupos = str(lista_grupos)+"-"+str(g.name)

    # Esta parte es para Pablo
    
    mensajesdeldia = mensajesgenerales.objects.all()

    # -----> Aqui para decirte si tenes pendiente firmar correspondencia

    usuario = request.user.username

    datos_mensajeria = len(NotaDePedido.objects.filter(copia__icontains = str(usuario)).exclude(visto__icontains = str(usuario))) + len(NotaDePedido.objects.filter(destinatario__icontains = str(usuario)).exclude(visto__icontains = str(usuario)))
    
    # -----> Aqui para decirte si tenes pendiente firmar OC

    mensaje_oc = 0

    if usuario == "PL":
        
        compras_espera = Comparativas.objects.filter(estado = "ESPERA", autoriza = "PL")
        compras_adjunto_ok = Comparativas.objects.filter(estado = "ADJUNTO ✓", autoriza = "PL")

        if len(compras_espera) > 0 or len(compras_adjunto_ok) > 0:
        
            mensaje_oc = [compras_espera, compras_adjunto_ok, (len(compras_espera) + len(compras_adjunto_ok))]
        
    elif usuario == "SP":

        compras = Comparativas.objects.filter(estado = "ESPERA", autoriza = "SP")
        compras_2 = Comparativas.objects.filter(estado = "ADJUNTO ✓", autoriza = "SP")

        if len(compras) > 0:
        
            mensaje_oc = [compras, compras_2, (len(compras) + len(compras_2))]

    else:

        data_1 = Comparativas.objects.filter(estado = "NO AUTORIZADA", creador = usuario)
        data_2 = Comparativas.objects.filter(visto = "VISTO NO CONFORME", creador = usuario, fecha_c__gte = "2021-02-01")

        if len(data_1) > 0 or len(data_2) > 0:

            mensaje_oc = [data_1, data_2, (len(data_1) + len(data_2))]
        

    datos_logo = 0

    try:
        datos_logo = datosusuario.objects.get(identificacion = request.user)

    except:

        datos_logo = 0

    date = datetime.date.today()

    Registros = RegistroAlmacenero.objects.filter(fecha =date)

    # -----------------> Aqui traigo la parte de honorarios para guardar en los historicos

    honorarios = Honorarios.objects.order_by("-fecha")

    subtotal_1 = honorarios[0].cuotas + honorarios[0].ventas
    ingresos = subtotal_1 + honorarios[0].creditos
    comision = honorarios[0].comision_venta*honorarios[0].ventas
    subtotal_2 = honorarios[0].estructura_gio + honorarios[0].aportes + honorarios[0].socios + comision
    costos = subtotal_2  + honorarios[0].deudas
    honorario = ingresos - costos + honorarios[0].caja_actual
    retiros = honorarios[0].retiro_socios
    honorarios2 = honorario - retiros

    if len(Registros) == 0:
    
        almacenero = Almacenero.objects.all()

        for alma in almacenero:

            presupuesto = Presupuestos.objects.get(proyecto = alma.proyecto)

            b = RegistroAlmacenero(
                fecha = date,
                proyecto = alma.proyecto,
                cheques_emitidos = alma.cheques_emitidos,
                gastos_fecha = alma.gastos_fecha,
                pendiente_admin = alma.pendiente_admin,
                pendiente_comision = alma.pendiente_comision,
                pendiente_adelantos = alma.pendiente_adelantos,
                pendiente_iva_ventas = alma.pendiente_iva_ventas,
                pendiente_iibb_tem = alma.pendiente_iibb_tem,
                pendiente_iibb_tem_link = alma.pendiente_iibb_tem_link,
                prestamos_proyecto = alma.prestamos_proyecto,
                prestamos_otros = alma.prestamos_otros,
                cuotas_cobradas = alma.cuotas_cobradas,
                cuotas_a_cobrar = alma.cuotas_a_cobrar,
                ingreso_ventas = alma.ingreso_ventas,
                ingreso_ventas_link = alma.ingreso_ventas_link,
                Prestamos_dados = alma.Prestamos_dados,
                unidades_socios = alma.unidades_socios,
                saldo_mat = presupuesto.saldo_mat,
                saldo_mo = presupuesto.saldo_mo,
                imprevisto = presupuesto.imprevisto,
                credito = presupuesto.credito, 
                fdr = presupuesto.fdr,
                retiro_socios= sum(np.array(RetirodeSocios.objects.values_list('monto_pesos').filter(proyecto = alma.proyecto))),
                retiro_socios_honorarios = retiros,
                honorarios = honorario,
                tenencia = alma.tenencia,
                financiacion = alma.financiacion,
                inmuebles = alma.inmuebles

            )

            b.save()

    Registro_presupuestos = RegistroValorProyecto.objects.filter(fecha =date)

    # -----------------> Aqui guardo por dia la información de presupuesto

    if len(Registro_presupuestos) == 0:

        presupuestos = Presupuestos.objects.all()

        for p in presupuestos:

            b = RegistroValorProyecto(

                proyecto = p.proyecto,
                fecha = date,
                precio_proyecto = p.valor,

            )

            b.save()

        if settings.ALLOWED_HOSTS:

            # -----------------> Aprovecho para avisar a PL sobre las OC

            today_h = datetime.date.today()

            fecha_pago = datetime.date(2021, 4, 16)

            while fecha_pago <= today_h:
                fecha_pago = fecha_pago + datetime.timedelta(days=14)
        
            fecha_alerta = fecha_pago - datetime.timedelta(days=3)

            if today_h == fecha_alerta:

                compras_espera = len(Comparativas.objects.filter(estado = "ESPERA").exclude(creador = "MES", numero__contains = "POSTV"))
                compras_adjunto_ok = len(Comparativas.objects.filter(estado = "ADJUNTO ✓").exclude(creador = "MES", numero__contains = "POSTV"))
                cantidad_oc = compras_espera + compras_adjunto_ok

                if cantidad_oc == 0:

                    send = "@Pablo, hasta el momento todas las OC estan firmadas para mañana"

                    id = "-585663986"

                    token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

                    url = "https://api.telegram.org/bot" + token + "/sendMessage"

                    params = {
                        'chat_id' : id,
                        'text' : send
                    }

                    requests.post(url, params=params)

                else:

                    send = "@Pablo mañana a las 13 horas deben estar firmadas las OC. Cantidad pendientes {} ".format(cantidad_oc)

                    id = "-585663986"

                    token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

                    url = "https://api.telegram.org/bot" + token + "/sendMessage"

                    params = {
                        'chat_id' : id,
                        'text' : send
                    }

                    requests.post(url, params=params)
            
            # -----------------> Saludamos al grupo
            
            if today_h.weekday() == 0:

                send = "Buen dia y buena semana grupo!, fui activado por {}. Listo para empezar el dia".format(request.user.first_name)

                id = "-455382561"

                token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

                url = "https://api.telegram.org/bot" + token + "/sendMessage"

                params = {
                    'chat_id' : id,
                    'text' : send
                }

                requests.post(url, params=params)

            elif today_h.weekday() == 2:

                send = "Buen miercoles!, fui activado por {}. Listo para ayudar".format(request.user.first_name)

                id = "-455382561"

                token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

                url = "https://api.telegram.org/bot" + token + "/sendMessage"

                params = {
                    'chat_id' : id,
                    'text' : send
                }

                requests.post(url, params=params)

            elif today_h.weekday() == 4:

                send = "Buen viernes!, fui activado por {}. Ultimo tiron".format(request.user.first_name)

                id = "-455382561"

                token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

                url = "https://api.telegram.org/bot" + token + "/sendMessage"

                params = {
                    'chat_id' : id,
                    'text' : send
                }

                requests.post(url, params=params)

            elif today_h.weekday() > 4:

                send = "Buen fin de semana!, fui activado por {} por alguna razón. Lamento molestar".format(request.user.first_name)

                id = "-455382561"

                token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

                url = "https://api.telegram.org/bot" + token + "/sendMessage"

                params = {
                    'chat_id' : id,
                    'text' : send
                }

                requests.post(url, params=params)

        #if hoy.weekday() == 0 or hoy.weekday() == 5:
            

    barras = []

    datos_barras = Presupuestos.objects.order_by("-saldo")

    for db in datos_barras:

        if db.valor != 0:

            avance = (100 - db.saldo/db.valor*100)

            barras.append((db, int(avance)))

    barras = sorted(barras,reverse=True, key=lambda tup: tup[1])


    miembros = datosusuario.objects.all().order_by("identificacion").exclude(estado = "NO ACTIVO")

    hoy = datetime.date.today()

    ## -> Parte de si recibiste monedas hoy

    if len(EntregaMoneda.objects.filter(fecha__gte = datetime.date.today(), usuario_recibe__identificacion = request.user)) > 0:
        moneda_mensaje = EntregaMoneda.objects.filter(fecha__gte = datetime.date.today(), usuario_recibe__identificacion = request.user)[0]
        context["monedas"] = (1, moneda_mensaje)
    
    else:
        context["monedas"] = 0

    ## -> Anuncios
    anuncios = Anuncios.objects.all().exclude(activo = "NO").order_by("-id")
    context["anuncios"] = anuncios

    ## -> Minutas

    minutas_cantidad = len(Acuerdos.objects.filter(responsable__identificacion = request.user.username, estado="NO CHECK"))

    minutas_cantidad_data = Acuerdos.objects.filter(responsable__identificacion = request.user.username, estado="NO CHECK")
    
    ########################################
    # OC observadas por SP
    ########################################

    sp_oc = []

    aux_sp = len(Comparativas.objects.filter(creador = request.user.username, visto = "VISTO NO CONFORME"))
    aux_sp_2 = Comparativas.objects.filter(creador = request.user.username, visto = "VISTO NO CONFORME").values_list("o_c")

    sp_oc.append(aux_sp)
    sp_oc.append(aux_sp_2)

    aviso = AvisoOrdenesCompras.objects.get(id=1)

    identificadores=aviso.usuarios.all().values_list('identificacion',flat=True)
    

    if usuario in identificadores:

        avisos_comparativas = Avisos(usuario,aviso)
        avisos_comparativas['autorizado']=True
    else:
        avisos_comparativas={}

    context["avisos_comparativas"] = avisos_comparativas
    context["lista_grupos"] = lista_grupos
    context["miembros"] = miembros
    context["minutas_cantidad_data"] = minutas_cantidad_data
    context["mensaje_oc"] = mensaje_oc
    context["sp_oc"] = sp_oc
    context["minutas_cantidad"] = minutas_cantidad
    context["mensajesdeldia"] = mensajesdeldia
    context["datos_barras"] = barras
    context["datos_logo"] = datos_logo
    context["datos_mensajeria"] = datos_mensajeria
    context["mensajesdeldia"] = mensajesdeldia


    return render(request, "users/inicio2.html", context)
    
def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:

        return render(request, "users/welcome.html")
    # En otro caso redireccionamos al login
    return redirect('/login')

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/inicio')

        else:

            return render(request, "users/logine.html", {'form': form}) 

    # Si llegamos al final renderizamos el formulario

    return render(request, "users/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def informes(request):

    if request.method == 'POST':

        data_post = request.POST.items()

        for d in data_post:

            if d[0] == "LISTO":
                    tarea = TareasProgramadas.objects.get(id = int(d[1]))
                    tarea.estado = "LISTO"
                    tarea.save()
            if d[0] == "TRABAJANDO":
                tarea = TareasProgramadas.objects.get(id = int(d[1]))
                tarea.estado = "TRABAJANDO"
                tarea.save()
            if d[0] == "PROBLEMAS":
                tarea = TareasProgramadas.objects.get(id = int(d[1]))
                tarea.estado = "PROBLEMAS"
                tarea.save()

        
    groups = request.user.groups.all().values_list('name', flat=True)

    if "MANDO MEDIO" in groups:
         informes_data = InformeMensual.objects.all().order_by('-fecha')
    else:
        informes_data = InformeMensual.objects.filter(user__identificacion = request.user).order_by('-fecha')
    tareas_data = TareasProgramadas.objects.filter(informe__user__identificacion = request.user).exclude(estado = "LISTO")

    return render(request, 'informes.html', {'tareas_data':tareas_data, 'informes_data':informes_data})

def verinforme(request, id_informe):

    project_list = Proyectos.objects.all()

    informes_data = InformeMensual.objects.get(id = id_informe)

    if request.method == 'POST':

        data_post = request.POST.items()

        for d in data_post:

            if d[0] == "mensaje":
                informes_data.informe = d[1]
                informes_data.save()

            if d[0] == "tareas":
                b = TareasProgramadas(
                    tarea = request.POST['tareas'],
                    informe = informes_data,
                    estado = "ESPERA",
                )
                b.save()

            if d[0] == "LISTO":
                tarea = TareasProgramadas.objects.get(id = int(d[1]))
                tarea.estado = "LISTO"
                tarea.save()
            if d[0] == "TRABAJANDO":
                tarea = TareasProgramadas.objects.get(id = int(d[1]))
                tarea.estado = "TRABAJANDO"
                tarea.save()
            if d[0] == "PROBLEMAS":
                tarea = TareasProgramadas.objects.get(id = int(d[1]))
                tarea.estado = "PROBLEMAS"
                tarea.save()
            if d[0] == "titulo":
                d = Bitacoras(
                    titulo = request.POST['titulo'],
                    proyecto = Proyectos.objects.get(id = int(request.POST['proyecto'])),
                    descrip = request.POST['descrip'],
                    informe = informes_data,
                )

                d.save()
            try:
                if d[0] == "descrip2":
                    bitacora = Bitacoras.objects.get(id = int(request.POST['bitacora']))
                    bitacora.descrip = request.POST['descrip2']
                    bitacora.save()
            except:
                pass


    tareas_data = TareasProgramadas.objects.filter(informe = informes_data)
    bitacoras_data = Bitacoras.objects.filter(informe = informes_data).order_by("-fecha")

    return render(request, 'informes_informe.html', {'bitacoras_data':bitacoras_data, 'project_list':project_list, 'informes_data':informes_data, 'tareas_data':tareas_data})

def informescrear(request):

    usuarios = datosusuario.objects.all().order_by("identificacion")


    if request.method == "POST":

        user = datosusuario.objects.get(id = request.POST['user'])

        b = InformeMensual(
            fecha = request.POST['fecha'],
            user = user,
        )

        b.save()

        return redirect('Informes')
    return render(request, 'informes_crear.html', {'usuarios':usuarios})

def tablerorega(request, id_proyecto, id_area, id_estado):

    if request.method == "POST":

        tarea = Seguimiento.objects.get(id = int(request.POST['id']))
        tarea.area = request.POST['area']
        tarea.nombre = request.POST['nombre']
        tarea.estado = request.POST['estado']
        tarea.proyecto = Proyectos.objects.get(nombre = request.POST['proyecto'])
        tarea.responsable = datosusuario.objects.get(id = int(request.POST['responsable']))
        tarea.save()

        try:
            tarea.fecha_inicio = request.POST['fechai']
            tarea.save()
        except:
            pass
        try:
            tarea.fecha_final = request.POST['fechaf']
            tarea.save()
        except:
            pass

    list_project_all = Proyectos.objects.all()

    group=models.Group.objects.get(name='REGA NIVEL 1')
    users=group.user_set.all()
    list_users = []
    for user in users:
        try:
            us = datosusuario.objects.get(identificacion = user.username)
            list_users.append(us)
        except:
            pass

    if id_proyecto != "0":
        proyecto_el = Proyectos.objects.get(id = int(id_proyecto))
    else:
        proyecto_el = 0

    estado = "Estado"

    areas = ["ADMINISTRACIÓN",
    "COMERCIALIZACIÓN",
    "PRODUCCIÓN"]

    diccionario = {'1': ("ADMINISTRACIÓN", "55, 172, 99 "),
    '2': ("PRODUCCIÓN", "161, 200, 58")}

    if id_area == "0":
        area = ["Área",""]
    else:
        area = diccionario[id_area]

    if id_area == "0":
        list_areas = Seguimiento.objects.all().values_list('area')
        list_areas = list(set(list_areas))
    else:
        list_areas = Seguimiento.objects.filter(area = diccionario[id_area][0]).values_list('area')
        list_areas = list(set(list_areas))
    list_project_dummy = Seguimiento.objects.all().values_list('proyecto')
    list_project_dummy = list(set(list_project_dummy))
    list_project = []

    for l in list_project_dummy:
        proyecto = Proyectos.objects.get(id = int(l[0]))
        list_project.append(proyecto)

    data = []

    for l in list_areas:

        if id_proyecto == "0":
            if id_estado == "0":
                data_list = Seguimiento.objects.filter(area = l[0])
                data.append((l, data_list))
            elif id_estado == "1":
                data_list = Seguimiento.objects.filter(area = l[0]).exclude(estado = "LISTO")
                data.append((l, data_list))
                estado = "Activos"
            elif id_estado == "2":
                data_list = Seguimiento.objects.filter(area = l[0], estado = "TRABAJANDO")
                data.append((l, data_list))
                estado = "Trabajando"
            elif id_estado == "3":
                data_list = Seguimiento.objects.filter(area = l[0], estado = "PROBLEMAS")
                data.append((l, data_list))
                estado = "Problemas"
            elif id_estado == "4":
                data_list = Seguimiento.objects.filter(area = l[0], estado = "LISTO")
                data.append((l, data_list))
                estado = "Listo"
            else:
                data_list = Seguimiento.objects.filter(area = l[0], estado = "ESPERA")
                data.append((l, data_list))
                estado = "Espera"

        else:
            if id_estado == "0":
                data_list = Seguimiento.objects.filter(area = l[0], proyecto__id = int(id_proyecto))
                data.append((l, data_list))
            elif id_estado == "1":
                data_list = Seguimiento.objects.filter(area = l[0], proyecto__id = int(id_proyecto)).exclude(estado = "LISTO")
                data.append((l, data_list))
                estado = "Activos"
            elif id_estado == "2":
                data_list = Seguimiento.objects.filter(area = l[0], proyecto__id = int(id_proyecto), estado = "TRABAJANDO")
                data.append((l, data_list))
                estado = "Trabajando"
            elif id_estado == "3":
                data_list = Seguimiento.objects.filter(area = l[0], proyecto__id = int(id_proyecto), estado = "PROBLEMAS")
                data.append((l, data_list))
                estado = "Problemas"
            elif id_estado == "4":
                data_list = Seguimiento.objects.filter(area = l[0], proyecto__id = int(id_proyecto), estado = "LISTO")
                data.append((l, data_list))
                estado = "Listo"
            else:
                data_list = Seguimiento.objects.filter(area = l[0], proyecto__id = int(id_proyecto), estado = "ESPERA")
                data.append((l, data_list))
                estado = "Espera"

    return render(request, 'seguimiento.html', {'list_project_all':list_project_all, 'list_users':list_users, 'area':area, 'estado':estado, 'proyecto':proyecto_el, 'data':data, 'list_project':list_project, 'id_estado':id_estado, 'id_area':id_area, 'id_proyecto':id_proyecto, 'areas':areas})

def tableroregaadd(request):

    group=models.Group.objects.get(name='REGA NIVEL 1')
    users=group.user_set.all()
    list_users = []
    for user in users:
        try:
            us = datosusuario.objects.get(identificacion = user.username)
            list_users.append(us)
        except:
            pass

    areas = ["ADMINISTRACIÓN",
    "COMERCIALIZACIÓN",
    "PRODUCCIÓN"]

    proyecto = Proyectos.objects.all().order_by("nombre")

    if request.method == "POST":

        datos_p = request.POST.items()
        
        tarea = Seguimiento(
            orden = len(Seguimiento.objects.filter(area = request.POST['area'])),
            area = request.POST['area'],
            proyecto = Proyectos.objects.get(id = int(request.POST['proyecto'])),
            nombre = request.POST['nombre'],
            responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])

        )

        tarea.save()

        try:
            tarea.fecha_inicio = request.POST['fechai']
            tarea.save()
        except:
            pass

        try:
            tarea.fecha_final = request.POST['fechaf']
            tarea.save()
        except:
            pass

        return redirect('Tablero Rega', id_proyecto = 0, id_area = 0, id_estado = 1)


    return render(request, 'seguimiento_add.html', {'areas':areas, 'proyecto':proyecto, 'list_users':list_users})

def anuncios(request):

    if request.method == 'POST':

        datos_p = request.POST.items()

        for d in datos_p:
            if d[0] == "ID":
                anuncio = Anuncios.objects.get(id = int(request.POST["ID"]))
                anuncio.titulo = request.POST["titulo"]
                anuncio.categoria = request.POST["categoria"]
                anuncio.descrip = request.POST["descrip"]
                anuncio.activo = request.POST["activo"]
                try:
                    anuncio.imagen = request.FILES['imagen']
                    anuncio.save()
                except:
                    anuncio.save()
            
            if d[0] == "NUEVO":

                b = Anuncios(
                    titulo = request.POST["titulo"],
                    categoria = request.POST["categoria"],
                    descrip = request.POST["descrip"],
                    activo = "SI",
                    imagen = request.FILES['imagen']
                )

                b.save()

            if d[0] == "delete":
                anuncio = Anuncios.objects.get(id = int(request.POST["delete"]))
                anuncio.delete()


    data = Anuncios.objects.all().order_by("-id")

    return render(request, 'users/anuncios.html', {"data":data})

def minutas(request):

    if request.method == 'POST':
        datos_p = request.POST.items()
        for d in datos_p:

            if d[0] == "delete":
                minuta = Minutas.objects.get(id = int(request.POST['delete']))
                minuta.delete()

    minutas_activas = []

    minutas_archivadas = []

    nombre_reuniones = Minutas.objects.values_list("reunion", flat = True).exclude(reunion = None).order_by("-fecha")

    nombre_reuniones = list(set(nombre_reuniones))    

    for name in nombre_reuniones:
        aux = Minutas.objects.filter(reunion = name).order_by("-fecha")[0:1]
        for a in aux:
            minutas_activas.append(a)
        aux_2 = Minutas.objects.filter(reunion = name).order_by("-fecha")[1:]
        for b in aux_2:
            minutas_archivadas.append(b)

    data_2 = Minutas.objects.filter(reunion = None)

    for d in data_2:

        minutas_activas.append(d)

    minutas_activas = sorted(minutas_activas, key = lambda x : x.fecha, reverse = True)

    user=request.user
    
    acuerdos=Acuerdos.objects.filter(responsable__identificacion=user,estado="NO CHECK")
    
    return render(request, 'minutas/minutasLista.html', {'minutas_activas':minutas_activas,'minutas_archivadas':minutas_archivadas,'acuerdos_pendientes':acuerdos})

def minutascrear(request):

    mensaje = 0

    if request.method == 'POST':

        datos_p = request.POST.items()

        try:

            minuta = Minutas(
                nombre = request.POST['nombre'],
                integrantes = request.POST['integrantes'],
                fecha = request.POST['fecha'],
                reunion = request.POST['reunion'],
                creador = datosusuario.objects.get(identificacion = request.user.username),
            )

            minuta.save()

            return redirect('Minutas Id', id_minuta = minuta.id)

        except:

            mensaje = "Algún dato de la minuta no esta completo o el creador no esta registrado"

    return render(request, 'minutas/minutasCrear.html', {'mensaje':mensaje})

def minutasmodificar(request, id_minuta):


    #group=models.Group.objects.get(name='REGA NIVEL 1')
    #users=group.user_set.all()

    list_users = datosusuario.objects.filter(estado = "ACTIVO")

    data = Minutas.objects.get(id = int(id_minuta))

    if request.method == 'POST':
        data.creador = datosusuario.objects.get(identificacion = request.POST['creador'])
        data.nombre = request.POST['nombre']
        data.fecha = request.POST['fecha']
        data.integrantes = request.POST['integrantes']
        data.reunion = request.POST['reunion']
        data.save()
        return redirect('Minutas Id', id_minuta = data.id)


    return render(request, 'minutas/minutasModificar.html', {'data':data, 'list_users':list_users})

def minutasid(request, id_minuta):

    group=models.Group.objects.get(name='REGA NIVEL 1')
    users=group.user_set.all()
    list_users = []
    for user in users:
        try:
            us = datosusuario.objects.get(identificacion = user.username)
            list_users.append(us)
        except:
            pass

    if request.method == 'POST':
        datos_p = request.POST.items()
        for d in datos_p:
            if d[0] == "tema":
                acuerdo = Acuerdos.objects.get(id = int(request.POST['id']))
                acuerdo.tema = request.POST['tema']
                try:
                    acuerdo.responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])
                    acuerdo.save()
                except:
                    acuerdo.responsable = None
                    acuerdo.save()

                try:
                    acuerdo.fecha_limite = request.POST['fecha_limite']
                    acuerdo.save()
                except:
                    pass

            if d[0] == "check":
                acuerdo = Acuerdos.objects.get(id = int(request.POST['check']))
                acuerdo.estado = "CHECK"
                acuerdo.save()

            if d[0] == "no_check":
                acuerdo = Acuerdos.objects.get(id = int(request.POST['no_check']))
                acuerdo.estado = "NO CHECK"
                acuerdo.save()

            if d[0] == "acuerdo":
                b = Acuerdos(
                    tema = request.POST['acuerdo'],
                    minuta = Minutas.objects.get(id = int(id_minuta))
                )
                try:
                    b.responsable = datosusuario.objects.get(identificacion = request.POST['responsable'])
                    b.save()
                except:
                    b.save()

            if d[0] == "delete":
                acuerdo = Acuerdos.objects.get(id = int(request.POST['delete']))
                acuerdo.delete()

    data = Minutas.objects.get(id = int(id_minuta))

    acuerdos = Acuerdos.objects.filter(minuta = data)

    acuerdos_viejos = Acuerdos.objects.filter(minuta__id__lt = data.id, estado = "NO CHECK", minuta__reunion = data.reunion)

    return render(request, 'minutas/minutasId.html', {'data':data, 'acuerdos':acuerdos, 'acuerdos_viejos':acuerdos_viejos, 'list_users':list_users})


