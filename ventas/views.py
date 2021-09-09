# Modelos de la BBDD usados
from django.contrib.auth.decorators import permission_required
from .models import EstudioMercado, PricingResumen, FeaturesProjects, FeaturesUni, DosierDeVenta, Clientescontacto
from proyectos.models import Unidades, Proyectos
from finanzas.models import Almacenero
from rrhh.models import datosusuario
from ventas.models import Pricing, ArchivosAreaVentas, VentasRealizadas, ArchivoFechaEntrega, ArchivoVariacionHormigon, ReclamosPostventa
from presupuestos.models import Constantes, Desde, Registrodeconstantes
from crm.models import Consulta, Tipologia

# Librerias matematicas
import numpy as np
import numpy_financial as npf

from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
from numpy.lib import twodim_base
from datetime import date
from django.shortcuts import redirect
from django.template.loader import get_template
import datetime
import string
import requests
from datetime import date
import operator
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side 
from django.views.generic.base import TemplateView 
from django.http import HttpResponse 
from xhtml2pdf import pisa
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from .functions import calculo_cotizacion
from .wabot import WABot
import smtplib


def appcomercial(request):
    return render(request, 'appcomercial_principal.html')

def apparchivoscomercial(request):
    return render(request, 'apparchivoscomercial.html')

def reportereclamos(request):

    list_category = ReclamosPostventa.objects.all().values_list('clasificacion')
    list_category = list(set(list_category))

    list_project = ReclamosPostventa.objects.all().values_list('proyecto')
    list_project = list(set(list_project))

    category_data = []

    for l in list_category:
        porcentual_l = len(ReclamosPostventa.objects.filter(clasificacion = l[0]))/len(ReclamosPostventa.objects.all())*100

        category_data.append((l[0], porcentual_l))

    status_data = []

    for p in list_project:
        listos = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "LISTO"))
        trabajando = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "TRABAJANDO"))
        problemas = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "PROBLEMAS"))
        espera = len(ReclamosPostventa.objects.filter(proyecto = p[0], estado = "ESPERA"))
        status_data.append((listos, trabajando, problemas, espera))

    category_data = sorted(category_data, key=lambda x: x[1], reverse=True)

    listos = len(ReclamosPostventa.objects.filter(estado = "LISTO"))
    trabajando = len(ReclamosPostventa.objects.filter(estado = "TRABAJANDO"))
    problemas = len(ReclamosPostventa.objects.filter(estado = "PROBLEMAS"))
    todos = len(ReclamosPostventa.objects.all())
    general_data = [listos, trabajando, problemas, todos]

    days = []

    data_list = ReclamosPostventa.objects.filter(estado = "LISTO")

    for i in data_list:
        if i.fecha_solucion:
            inicio = i.fecha_reclamo
            final = i.fecha_solucion
            dias = (final - inicio).days
            days.append(dias)

    days = np.array(days)
    promedio = np.mean(days)
    maximo = np.max(days)
    minimo = np.min(days)
    

    return render(request, 'reporte_reclamo.html', {'minimo':minimo, 'maximo':maximo,'promedio':promedio,'general_data':general_data, 'satus_data':status_data, 'category_data':category_data, 'list_project':list_project})

def reclamo(request, id_reclamo):

    if request.method == 'POST':

        datos = request.POST.items()

        for i in datos:

            if i[0] == "LISTO":

                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)
                reclamo.fecha_solucion = datetime.date.today()
                reclamo.estado = "LISTO"
                reclamo.save()

            if i[0] == "TRABAJANDO":

                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)

                reclamo.estado = "TRABAJANDO"
                reclamo.fecha_solucion = None
                reclamo.save()

            if i[0] == "PROBLEMAS":

                reclamo = ReclamosPostventa.objects.get(id = id_reclamo)

                reclamo.estado = "PROBLEMAS"
                reclamo.fecha_solucion = None
                reclamo.save()

    datos = ReclamosPostventa.objects.get(id = id_reclamo)

    

    return render(request, 'reclamo.html', {'datos':datos})

def crearreclamo(request):

    proyectos = list(set(ReclamosPostventa.objects.values_list('proyecto')))
    clasificacion = list(set(ReclamosPostventa.objects.values_list('clasificacion')))

    if request.method == 'POST':

        b = ReclamosPostventa(
                numero = request.POST['numero'],
                fecha_reclamo = request.POST['fecha'],
                propietario = request.POST['propietario'],
                usuario = request.POST['usuario'],
                telefono = request.POST['telefono'],
                email = request.POST['email'],
                proyecto = request.POST['proyecto'],
                unidad = request.POST['unidad'],
                estado = "ESPERA",
                clasificacion = request.POST['clasificacion'],
                descripcion = request.POST['descripcion'],
                )

        b.save()

        return redirect('Reclamos Postventa')

    return render(request, 'agregarreclamo.html', {'proyectos':proyectos, 'clasificacion':clasificacion})

def editarreclamo(request, id_reclamo):

    datos = ReclamosPostventa.objects.get(id = id_reclamo)

    proyectos = list(set(ReclamosPostventa.objects.values_list('proyecto')))
    clasificacion = list(set(ReclamosPostventa.objects.values_list('clasificacion')))
    responsable = datosusuario.objects.values_list('identificacion')

    if request.method == 'POST':
        reclamo = ReclamosPostventa.objects.get(id = id_reclamo)
        reclamo.numero = request.POST['numero']
        reclamo.fecha_reclamo = request.POST['fecha']
        reclamo.propietario = request.POST['propietario']
        reclamo.usuario = request.POST['usuario']
        reclamo.telefono = request.POST['telefono']
        reclamo.email = request.POST['email']
        reclamo.proyecto = request.POST['proyecto']
        reclamo.unidad = request.POST['unidad']
        reclamo.clasificacion = request.POST['clasificacion']
        reclamo.descripcion = request.POST['descripcion']
        if request.POST['fecha_solucion']:
            reclamo.fecha_solucion = request.POST['fecha_solucion']
        try:
            usuario = datosusuario.objects.get(identificacion = request.POST['responsable'])
            reclamo.responsable = usuario
            reclamo.save()
        except:
            reclamo.save()

        return redirect('Reclamo', id_reclamo = datos.id)

    return render(request, 'editar_reclamo.html', {'responsable':responsable, 'datos':datos, 'proyectos':proyectos, 'clasificacion':clasificacion})

def reclamospostventa(request):

    datos = ReclamosPostventa.objects.all().order_by("-numero")

    #----> Aqui empieza el filtro

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        datos_viejos = datos

        datos = []   

        for i in palabra_buscar:

            if i[0] == "palabra":
        
                palabra_buscar = i[1]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                lista_palabra = palabra.split()

                buscar = (str(i.proyecto)+str(i.usuario)+str(i.propietario)+str(i.descripcion)+str(i.numero)+str(i.clasificacion))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)

    #----> Aqui termina el filtro

    return render(request, 'reclamospostventa.html', {'datos':datos})

def informeventa(request):

    if request.method == 'POST':
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAreaVentas(
                      fecha = request.POST['fecha'],
                    informe_venta = request.FILES['adjunto']
                )
              
                datos.save()
            if dato[0] == "delete":
                archivo = ArchivosAreaVentas.objects.get(id = int(request.POST['delete']))
                archivo.informe_venta = None
                archivo.save()


    data = ArchivosAreaVentas.objects.filter(informe_venta__isnull = False).order_by("-fecha")

    datos = {"data":data}

    return render(request, 'informe_venta.html', {"datos":datos})

def historialventa(request):

    busqueda = 1
    datos_pricing = ArchivosAreaVentas.objects.filter(historial_venta__isnull = False)
    datos = 0
    fecha = 0

    fechas = []

    for dato in datos_pricing:

        if dato.historial_venta: 
            fechas.append((dato.fecha, str(dato.fecha)))

    fechas = list(set(fechas))

    fechas.sort( reverse=True)

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAreaVentas.objects.get(fecha = dato[1])
                busqueda = 0
                fecha = dato[1]

    # ----> Aqui armo la fecha de inicio

    today = datetime.date.today()

    fecha_1 = datetime.date(today.year, 1, 1)
    fecha_2 = datetime.date((today.year - 1), 1, 1)

    ventas_1 = VentasRealizadas.objects.filter(fecha__gte = fecha_1, unidad__asig = "PROYECTO")

    ventas_2 = VentasRealizadas.objects.filter(fecha__gte = fecha_2, fecha__lte = fecha_1, unidad__asig = "PROYECTO")

    proyectos = Proyectos.objects.all()

    list_p = []

    for p in proyectos:

        ventas_p = len(VentasRealizadas.objects.filter(fecha__gte = fecha_1, unidad__proyecto = p, unidad__asig = "PROYECTO"))

        if ventas_p > 0:
            list_p.append((p, ventas_p))

    list_p.sort(key=lambda tup: tup[1], reverse=True)


    list_ritmo = []

    fecha = fecha_1

    for i in range(12):

        fecha_i = fecha
        if fecha_i.month != 12:
            fecha_f = datetime.date(fecha_i.year, (fecha_i.month + 1), 1)
        else:
            fecha_f = datetime.date((fecha_i.year + 1), 1, 1)
        ventas_n = len(VentasRealizadas.objects.filter(fecha__gte = fecha_i, fecha__lte = fecha_f, unidad__asig = "PROYECTO"))

        list_ritmo.append((fecha_i, ventas_n))

        fecha = fecha_f

    # ------> Aqui estudiamos la parte del descuento

    pricing = 0
    real = 0
    unidades_chequeadas = 0
    monto_neto = 0
    contado = 0
    m2_v = 0
    monto_h = 0

    lista_venta_des = []

    for v in ventas_1:

        dato = v.unidad

        if dato.sup_equiv > 0:

                m2 = dato.sup_equiv
        else:

            m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio           
        try:

            param_uni = Pricing.objects.get(unidad = dato)
            
            desde = PricingResumen.objects.filter(fecha__lte = v.fecha, proyecto = dato.proyecto).order_by("-fecha")
            desde = desde[0].base_precio

            if dato.tipo == "COCHERA":
                desde = desde*dato.proyecto.descuento_cochera

            if param_uni.frente == "SI":
                desde = desde*dato.proyecto.recargo_frente

            if param_uni.piso_intermedio == "SI":
                desde =desde*dato.proyecto.recargo_piso_intermedio

            if param_uni.cocina_separada == "SI":
                desde = desde*dato.proyecto.recargo_cocina_separada

            if param_uni.local == "SI":
                desde = desde*dato.proyecto.recargo_local

            if param_uni.menor_45_m2 == "SI":
                desde = desde*dato.proyecto.recargo_menor_45

            if param_uni.menor_50_m2 == "SI":
                desde = desde*dato.proyecto.recargo_menor_50

            if param_uni.otros == "SI":
                desde = desde*dato.proyecto.recargo_otros 

            pricing = pricing + desde*m2 

            unidades_chequeadas += 1

            real = real + v.precio_contado

            pricing_un = desde*m2

            descuento_un = (1 - v.precio_contado/pricing_un)*100

            lista_venta_des.append((v, pricing_un, descuento_un, v.fecha))

        except:
            lista_venta_des.append((v, "S/PRG", "S/D", v.fecha))

        monto_neto = monto_neto + v.precio_venta

        fecha_buscar = datetime.date(v.fecha.year, v.fecha.month, 1)

        registro_h = Registrodeconstantes.objects.filter(constante__nombre = "Hº VIVIENDA", fecha = fecha_buscar)[0].valor

        monto_h = monto_h + (v.precio_venta/registro_h)

        if (v.precio_venta - v.anticipo) < v.precio_venta*0.05:

            contado += 1

        m2_v = m2_v + m2

    if pricing == 0:
        
        descuento = 0
    else:   
        descuento = (real/pricing - 1)*100 

    pricing_2 = 0
    real_2 = 0
    unidades_chequeadas_2 = 0   
    contado_2 = 0
    m2_v_2 = 0

    for v in ventas_2:

        dato = v.unidad

        if dato.sup_equiv > 0:

                m2 = dato.sup_equiv

        else:

            m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio
           
        try:

            param_uni = Pricing.objects.get(unidad = dato)
            
            desde = PricingResumen.objects.filter(fecha__lte = v.fecha, proyecto = dato.proyecto).order_by("-fecha")

            desde = desde[0].base_precio

            if dato.tipo == "COCHERA":
                desde = desde*dato.proyecto.descuento_cochera

            if param_uni.frente == "SI":
                desde = desde*dato.proyecto.recargo_frente

            if param_uni.piso_intermedio == "SI":
                desde =desde*dato.proyecto.recargo_piso_intermedio

            if param_uni.cocina_separada == "SI":
                desde = desde*dato.proyecto.recargo_cocina_separada

            if param_uni.local == "SI":
                desde = desde*dato.proyecto.recargo_local

            if param_uni.menor_45_m2 == "SI":
                desde = desde*dato.proyecto.recargo_menor_45

            if param_uni.menor_50_m2 == "SI":
                desde = desde*dato.proyecto.recargo_menor_50

            if param_uni.otros == "SI":
                desde = desde*dato.proyecto.recargo_otros 

            pricing_2 = pricing_2 + desde*m2 

            unidades_chequeadas_2 += 1

            real_2 = real_2 + v.precio_contado

            pricing_un = desde*m2

            descuento_un = (1 - v.precio_contado/pricing_un)*100

            lista_venta_des.append((v, pricing_un, descuento_un, v.fecha))

        except:
            lista_venta_des.append((v, "S/PRG", "S/D", v.fecha))

        if (v.precio_venta - v.anticipo) < v.precio_venta*0.05:

            contado_2 += 1
    
        m2_v_2 = m2_v_2 + m2

    descuento_2 = (real_2/pricing_2 - 1)*100   
    ventas_1 = len(ventas_1)
    ventas_2 = len(ventas_2)
    if ventas_1 == 0:
        contado = 0
    else:
        contado = ((contado/ventas_1))*100
    financiado = 100 - contado
    contado_2 = ((contado_2/ventas_2))*100
    financiado_2 = 100 - contado_2

    hoy = datetime.date.today()

    diferencia = abs((hoy - fecha_1).days)  

    if ventas_1 > 0:
        ritmo = diferencia/ventas_1   
        ritmo_mes = (ritmo)**(-1)*30
    else:
        ritmo = 0
        ritmo_mes = 0  

    if m2_v == 0:
        m3_m2 = 0
    else:
        m3_m2 = monto_h/m2_v

    datos_panel = [ventas_1, ventas_2, fecha_1, fecha_2, list_p, list_ritmo, descuento, unidades_chequeadas, descuento_2, unidades_chequeadas_2, ritmo, monto_neto, contado, financiado, contado_2, financiado_2, ritmo_mes, m2_v, m2_v_2, monto_h, m3_m2]

    lista_venta_des = sorted(lista_venta_des, key=lambda tup: tup[3], reverse=True)

    datos = {"fechas":fechas,
    "busqueda":busqueda,
    "datos":datos,
    "fecha":fecha,
    "datos_panel":datos_panel,
    "lista_venta_des":lista_venta_des}

    return render(request, 'historial_venta.html', {"datos":datos})

def folleto(request):

    datos = Proyectos.objects.all()

    proyecto = 0

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                proyecto = Proyectos.objects.get(nombre = dato[1])
 

    return render(request, 'folleto.html', {"datos":datos, "proyecto":proyecto})

def evousd(request):

    if request.method == 'POST':
        datos_p = request.POST.items()
        for d in datos_p:
            if d[0] == "fecha":
                b = ArchivosAreaVentas(
                    fecha = request.POST['fecha'],
                    evo_usd = request.FILES['adjunto']
                )

                b.save()
            if d[0] == "delete":
                archivo = ArchivosAreaVentas.objects.get(id = int(request.POST['delete']))
                archivo.evo_usd = None
                archivo.save()


    data = ArchivosAreaVentas.objects.filter(evo_usd__isnull = False).order_by("-fecha")

    datos = {"data":data}

    return render(request, 'evousd.html', {"datos":datos})

def encuestapostventa(request):

    if request.method == 'POST':
        datos_elegidos = request.POST.items()
        for dato in datos_elegidos:

            if dato[0] == "fecha":
                b = ArchivosAreaVentas(
                    fecha = request.POST['fecha'],
                    encuesta_postventa = request.FILES['adjunto']
                )
          
                b.save()
            if dato[0] == "delete":
                archivo = ArchivosAreaVentas.objects.get(id = int(request.POST['delete']))
                archivo.encuesta_postventa = None
                archivo.save()

    data = ArchivosAreaVentas.objects.filter(encuesta_postventa__isnull = False).order_by("-fecha")

    datos = {"data":data}

    return render(request, 'encuestapostventa.html', {"datos":datos})

def invmer(request):

    if request.method == 'POST':

        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAreaVentas(
                    fecha = request.POST['fecha'],
                    invest_mercado = request.FILES['adjunto']
                    )
              

                datos.save()
            if dato[0] == "delete":
                archivo = ArchivosAreaVentas.objects.get(id = int(request.POST['delete']))
                archivo.invest_mercado = None
                archivo.save()


    data = ArchivosAreaVentas.objects.filter(invest_mercado__isnull = False).order_by("-fecha")

    datos = {"data":data}

    return render(request, 'inv_merc.html', {"datos":datos})

def informe_redes(request):

    if request.method == 'POST':
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAreaVentas(
                      fecha = request.POST['fecha'],
                    informe_redes = request.FILES['adjunto']
                )

                datos.save()
            if dato[0] == "delete":
                archivo = ArchivosAreaVentas.objects.get(id = int(request.POST['delete']))
                archivo.informe_redes = None
                archivo.save()



    data = ArchivosAreaVentas.objects.filter(informe_redes__isnull = False).order_by("-fecha")

    datos = {"data":data}

    return render(request, 'informe_redes.html', {"datos":datos})

def cajaarea(request):

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for d in datos_elegidos:

            if d[0] == "fecha":
                datos = ArchivosAreaVentas(fecha = request.POST['fecha'],
                caja_area = request.FILES['adjunto']
                )

                datos.save()         

            if d[0] == "delete":
                archivo = ArchivosAreaVentas.objects.get(id = int(request.POST['delete']))    
                archivo.caja_area = None
                archivo.save()

    data = ArchivosAreaVentas.objects.filter(caja_area__isnull = False).order_by("-fecha")        

    datos = {"data":data}

    return render(request, 'caja_area.html', {"datos":datos})

def fechaentrega(request):

    if request.method == 'POST':
         datos_elegidos = request.POST.items()
         for dato in datos_elegidos:
            if dato[0] == "fecha":
                b = ArchivoFechaEntrega(
                            fecha = request.POST['fecha'],
                            archivo = request.FILES['adjunto']
                )

                b.save()
            if dato[0] == "delete":
                archivo = ArchivoFechaEntrega.objects.get(id = int(request.POST['delete']))
                archivo.archivo = None
                archivo.save()


    data = ArchivoFechaEntrega.objects.filter(archivo__isnull = False).order_by("-fecha")

    datos = {"data":data}

    return render(request, 'fechaentrega.html', {"datos":datos})

def radiografia(request):

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAreaVentas(
                    fecha = request.POST['fecha'],
                    radiografia_cliente = request.FILES['adjunto']
                )
                
                datos.save()
            if dato[0] == "delete":
                archivo = ArchivosAreaVentas.objects.get(id = int(request.POST['delete']))
                archivo.radiografia_cliente = None
                archivo.save()


    data = ArchivosAreaVentas.objects.filter(radiografia_cliente__isnull = False).order_by("-fecha")

    datos = {"data":data}

    return render(request, 'radiografiaclientes.html', {"datos":datos})

def resumenprecio(request):


    busqueda = 1
    datos_pricing = PricingResumen.objects.all()
    datos = 0
    fecha = 0

    fechas = []

    datos_presupuesto = []

    #--> Parte para calcular precio presupuesto

    datos_desde = Desde.objects.all()

    constantes = Constantes.objects.all()

    usd_blue = Constantes.objects.get(nombre = "USD_BLUE")

    for i in datos_desde:

        costo = i.presupuesto.valor

        #Aqui calculo el precio min y sugerido

        costo = (costo/(1 + i.parametros.tasa_des_p))*(1 + i.parametros.soft)
        
        costo = costo*(1 + i.parametros.imprevitso)

        porc_terreno = i.parametros.terreno/i.parametros.proyecto.m2*100
        porc_link = i.parametros.link/i.parametros.proyecto.m2*100

        aumento_tem = i.parametros.tem_iibb*i.parametros.por_temiibb*(1+i.parametros.ganancia)

        aumento_comer = i.parametros.comer*(1+(porc_terreno + porc_link)/100)*(1+i.parametros.ganancia)
        

        costo = costo/(1-aumento_tem- aumento_comer)
        
        m2 = (i.parametros.proyecto.m2 - i.parametros.terreno - i.parametros.link)

        valor_costo = costo/m2

        #Aqui coloco la tasa de descuento


        fecha_entrega =  datetime.datetime.strptime(str(i.presupuesto.proyecto.fecha_f), '%Y-%m-%d')
        ahora = datetime.datetime.utcnow()
        fecha_inicial = ahora + datetime.timedelta(days = (365*2))

        if fecha_entrega > fecha_inicial:
            y = fecha_entrega.year - fecha_inicial.year
            n = fecha_entrega.month - fecha_inicial.month

            meses = y*12 + n

            valor_costo = -np.pv(fv=valor_costo, rate=i.parametros.tasa_des, nper=meses, pmt=0)


        #Calculo el valor final
        
        valor_final = valor_costo*(1 + i.parametros.ganancia)


        # Valorizo en dolares el precio de costo y sugerido

        valor_costo_usd = 0

        valor_final_usd = 0

        for c in constantes:

            if str(c.nombre) == 'USD_BLUE':

                valor_costo_usd = valor_costo/c.valor

                valor_final_usd = valor_final/c.valor

        i.valor_costo = valor_costo
        i.valor_costo_usd = valor_costo_usd
        i.valor_final = valor_final
        i.valor_final_usd = valor_final_usd

        i.save()

        #--> Parte para calcular precio promedio contado

        datos_unidades = Unidades.objects.filter(proyecto = i.parametros.proyecto, estado = "DISPONIBLE")
        unidades_totales = len(Unidades.objects.filter(proyecto = i.parametros.proyecto))
        unidades_disponibles = len(datos_unidades)

        if unidades_totales == 0:
            porcentaje_vendido = 0

        else:
            porcentaje_vendido = (1 - (unidades_disponibles/unidades_totales))*100

        m2_totales = 0

        sumatoria_contado = 0
    
        for dato in datos_unidades:

            if dato.sup_equiv > 0:

                m2 = dato.sup_equiv

            else:

                m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio

            try:

                m2_panel = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio

                venta = VentasRealizadas.objects.get(unidad = dato.id)

                venta.m2 = m2_panel

                venta.asignacion = dato.asig

                venta.save()
            
            except:

                basura = 1
            
            try:

                param_uni = Pricing.objects.get(unidad = dato)
                
                desde = dato.proyecto.desde

                if dato.tipo == "COCHERA":
                    desde = dato.proyecto.desde*dato.proyecto.descuento_cochera

                if param_uni.frente == "SI":
                    desde = desde*dato.proyecto.recargo_frente

                if param_uni.piso_intermedio == "SI":
                    desde =desde*dato.proyecto.recargo_piso_intermedio

                if param_uni.cocina_separada == "SI":
                    desde = desde*dato.proyecto.recargo_cocina_separada

                if param_uni.local == "SI":
                    desde = desde*dato.proyecto.recargo_local

                if param_uni.menor_45_m2 == "SI":
                    desde = desde*dato.proyecto.recargo_menor_45

                if param_uni.menor_50_m2 == "SI":
                    desde = desde*dato.proyecto.recargo_menor_50

                if param_uni.otros == "SI":
                    desde = desde*dato.proyecto.recargo_otros 

                #Aqui calculamos el contado/financiado
                
                contado = desde*m2 

                sumatoria_contado = sumatoria_contado + contado
                m2_totales = m2_totales + m2

            except:

                basura = 1


        if m2_totales == 0:

            precio_promedio_contado = 0

        else:

            precio_promedio_contado = sumatoria_contado/m2_totales

        precio_promedio_contado_plus = precio_promedio_contado*1.05

        if valor_final == 0:

            var = 0

        else:

            var = ((precio_promedio_contado/i.valor_final)-1)*100

        fecha_pricing = PricingResumen.objects.order_by("-fecha")

        datos_presupuesto.append((i, precio_promedio_contado, precio_promedio_contado_plus, var, porcentaje_vendido, fecha_pricing))

    

    for dato in datos_pricing:
        
        fechas.append((dato.fecha, str(dato.fecha)))

    fechas = list(set(fechas))

    fechas.sort( reverse=True)

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:
            if dato[0] == "fecha":
                datos = PricingResumen.objects.filter(fecha = dato[1])
                busqueda = 0
                fecha = dato[1]


    datos = {"fechas":fechas,
    "busqueda":busqueda,
    "datos":datos,
    "fecha":fecha,
    "datos_presupuesto":datos_presupuesto}

    return render(request, 'resumenprecio.html', {"datos":datos})

def estmercado(request):

    datos_estudio = EstudioMercado.objects.all()

    estudios = []
    meses = []
    datos_link = []
    datos_otros = []
    grafico = 0

    for dato in datos_estudio:

        estudios.append(str(dato.fecha))
        meses.append(dato.meses)

    estudios = list(set(estudios))
    meses = list(set(meses))
    meses.sort()

    if request.method == 'POST':

        grafico = 1

        estudio = request.POST.items()

        for dato in estudio:

            if dato[0] == 'csrfmiddlewaretoken':
                pass

            else:

                for i in datos_estudio:
                    if str(i.fecha) == dato[1]:
                        if i.empresa == "LINK":
                            datos_link.append(i)
                        else:
                            datos_otros.append(i)

    datos = {
        "link":datos_link,
        "otros":datos_otros,
        "meses":meses,
        "estudios":estudios,
        "graficos":grafico,
    }

    return render(request, 'estmercado.html', {"datos":datos})

def panelunidades(request):

    datos = Unidades.objects.all().order_by("orden")

    proyectos = []

    datos_unidades = 0

    mensaje = 0

    otros_datos = 0


    for dato in datos:
        proyectos.append(dato.proyecto)

    proyectos = list(set(proyectos))

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        list_proyectos = []
        aisgnacion = []
        disponibilidad = []

        for dato in datos_elegidos:

            if "Asig" in str(dato[0]):
                aisgnacion.append(dato[1])

            elif "Disp" in str(dato[0]):
                disponibilidad.append(dato[1])

            elif str(dato[0]) == "csrfmiddlewaretoken":
                basura = 1

            else:
                list_proyectos.append(dato[0])

        if len(list_proyectos)==0 or len(aisgnacion)==0 or len(disponibilidad)==0:
            mensaje = 1

        else:
            mensaje = 2
            otros_datos = []
            datos_tabla_unidad = []
            m2_totales = 0
            monto_total = 0
            cocheras = 0

            for proy in list_proyectos:
                for asig in aisgnacion:
                    for disp in disponibilidad:
                        
                        datos_unidades = Unidades.objects.filter(proyecto__nombre = proy, asig = asig, estado=disp)
                        
                        for dato in datos_unidades:
                            if dato.sup_equiv > 0:

                                m2 = round(dato.sup_equiv, 2)

                            else:

                                m2 = round((dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio), 2)
                            
                            contado = m2*dato.proyecto.desde

                            features_unidad = FeaturesUni.objects.filter(unidad = dato)

                            for f2 in features_unidad:

                                contado = contado*f2.feature.inc

                            monto_total = monto_total + contado

                            desde = round((contado/m2), 4)

                            datos_tabla_unidad.append((dato, m2, contado, dato.id))
                            
                            m2_totales = m2_totales + m2
                            
                            if dato.tipo == "COCHERA":
                                cocheras += 1
                            

            cantidad = len(datos_tabla_unidad)

            departamentos = cantidad - cocheras

            otros_datos.append((m2_totales, cantidad, departamentos, cocheras, monto_total))

            datos_unidades = datos_tabla_unidad

            datos_unidades.sort(key=lambda datos_unidades: datos_unidades[3], reverse=False)


    datos = {"proyectos":proyectos, "datos":datos, "mensaje":mensaje, "datos_unidades":datos_unidades, "otros_datos":otros_datos}

    return render(request, 'panelunidades.html', {"datos":datos})

def variacionh(request):

    datos = ArchivoVariacionHormigon.objects.order_by("-fecha")

    busqueda = 0

    if request.method == 'POST':

        try:

            b = ArchivoVariacionHormigon(

                archivo = request.FILES['adjunto'],
            )

            b.save()

        except:
            
            busqueda = ArchivoVariacionHormigon.objects.get(id = request.POST['fecha']) 

    datos_hormigon = Registrodeconstantes.objects.filter(constante__nombre = "Hº VIVIENDA").order_by('fecha')

    year = datos_hormigon[0].fecha.year

    year_now = datetime.date.today().year

    datos_h = []

    valor_anterior = 0

    valor_inicial = 0

    while year != (year_now+1):

        datos_year = []

        month = 1

        for i in range(12):
            
            dia = datetime.date(year, month, 1)

            valor = Registrodeconstantes.objects.filter(constante__nombre = "Hº VIVIENDA", fecha = dia)

            if month == 12:

                if valor_inicial != 0 and len(valor) != 0:

                    variacion_anual = (valor[0].valor/valor_inicial-1)*100
                else:
                    variacion_anual = 0

            if len(valor) != 0:

                if valor_anterior == 0:

                    variacion = 0

                    datos_year.append((dia, valor[0].valor, variacion))

                    valor_anterior = valor[0].valor

                    if month == 12:
                        valor_inicial = valor[0].valor

                else:

                    variacion = (valor[0].valor/valor_anterior-1)*100

                    datos_year.append((dia, valor[0].valor, variacion))

                    valor_anterior = valor[0].valor

                    if month == 12:
                        valor_inicial = valor[0].valor

            else:
                datos_year.append((dia, 0, 0))

            if month == 12:

                datos_year.append(variacion_anual)

            month += 1

      
        datos_h.append(datos_year)

        datos_h.sort(key=lambda datos_h: datos_h, reverse=True)

        year += 1

        horm = Constantes.objects.get(nombre = "Hº VIVIENDA")

    try:

        year_now = datetime.date.today()

        if year_now.month != 1:

            fecha_aux = datetime.date(year_now.year, year_now.month - 1 , 1)

        else:

            fecha_aux = datetime.date(year_now.year -1 , 12 , 1)

        valor_aux = Registrodeconstantes.objects.get(constante__nombre = "Hº VIVIENDA", fecha = fecha_aux)

        var = (horm.valor/valor_aux.valor - 1)*100

    except:

        var = 0


    return render(request, 'variacionhormigon.html', {"var":var, "datos_h":datos_h, "datos":datos, "busqueda":busqueda, "horm":horm})

def editarasignacion(request, id_unidad):

    id_unidad = id_unidad

    datos = Unidades.objects.get(id = id_unidad)

    if request.method == 'POST':

        valor_elegido = request.POST.items()

        for valor in valor_elegido:
            
            if valor[0] == "asignacion":

                if valor[1] == "1":
                    datos.asig = "PROYECTO"

                    datos.save()

                if valor[1] == "2":
                    datos.asig = "TERRENO"

                    datos.save()

                if valor[1] == "3":
                    datos.asig = "HON. LINK"

                    datos.save()

                if valor[1] == "4":

                    datos.asig = "SOCIOS"

                    datos.save()


                return redirect ('Panel de unidades')

    return render(request, 'editarasig.html', {"datos":datos} )

def dosier(request):
    data_project = Proyectos.objects.all()

    if request.method == 'POST':
        try: 
            proyecto = Proyectos.objects.get(id = int(request.POST['proyecto']))
            new = DosierDeVenta(
                fecha = request.POST['fecha'],
                proyecto = proyecto,
                adjunto = request.FILES['adjunto']
            )
            new.save()

        except:
            pass

        try:
            seleccionado = DosierDeVenta.objects.get(id = int(request.POST['delete']))
            seleccionado.delete()
        except:
            pass
        try:
            proyecto = Proyectos.objects.get(id = int(request.POST['proyecto']))
            seleccionado = DosierDeVenta.objects.get(id = int(request.POST['editar']))
            seleccionado.fecha = request.POST['fecha']
            seleccionado.proyecto = proyecto
            try:
                seleccionado.adjunto = request.FILES['adjunto']
                seleccionado.save()
            except:
                seleccionado.save()
        except:
            pass


    dosier = DosierDeVenta.objects.all().order_by('fecha')


    return render(request, 'dosier.html', {'data_project': data_project, 'dosier': dosier})

def pricing(request, id_proyecto):

    context = {}

    #Aqui empieza para cambiar el precio base

    precio_nuevo = 0

    if request.method == 'GET':

        nuevo_precio = request.GET.items()

        for precio in nuevo_precio:

            datos_modificar = Proyectos.objects.get(id = id_proyecto)

            precio_nuevo = precio[1]

            datos_modificar.desde = precio_nuevo

            datos_modificar.save()

    proyecto = Proyectos.objects.get(id = id_proyecto)

    datos = Unidades.objects.filter(proyecto = proyecto).order_by("orden")

    mensaje = 0
    otros_datos = 0
    anticipo = 0.4
    fecha_entrega =  datetime.datetime.strptime(str(proyecto.fecha_f), '%Y-%m-%d')

    ahora = datetime.datetime.utcnow()

    y = fecha_entrega.year - ahora.year
    n = fecha_entrega.month - ahora.month
    meses = y*12 + n

    financiado = 0
    financiado_m2 = 0
    fin_ant = 0
    valor_cuotas = 0

    mensaje = 2
    otros_datos = []
    datos_tabla_unidad = []
    m2_totales = 0
    m2_totales_disp = 0
    cocheras = 0
    ingreso_ventas = 0
    iibb = 0
    comision = 0
    unidades_socios = 0
    contado_total = 0

    #Datos resumenes de arriba

    sumatoria_contado = 0
    sumatoria_financiado = 0

   
    for dato in datos:

        if dato.sup_equiv > 0:

            m2 = round(dato.sup_equiv, 2)

        else:

            m2 = round((dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio), 2)

        try:

            m2_panel = round((dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio), 2)

            venta = VentasRealizadas.objects.get(unidad = dato.id)

            venta.m2 = m2_panel

            venta.asignacion = dato.asig

            venta.save()
        
        except:

            basura = 1
        
        try:
            contado = m2*dato.proyecto.desde
        
        except:

            contado = 0
            context['mensajes'] = ["El proyecto no tiene un precio desde para calcular"]

        features_unidad = FeaturesUni.objects.filter(unidad = dato)

        if len(features_unidad) != 0:

            for f2 in features_unidad:

                contado = contado*f2.feature.inc

            desde = round((contado/m2), 4)
        
        else:

            desde = 0
            context['mensajes'] = ["El proyecto no tiene features"]

        #Aqui calculamos el contado/financiado
        
        values = [0]

        for m in range((meses)):
            values.append(1)

        anticipo = 0.4

        valor_auxiliar = npf.npv(rate=(dato.proyecto.tasa_f/100), values=values)

        incremento = (meses/(1-anticipo)/(((anticipo/(1-anticipo))*meses)+valor_auxiliar))

        financiado = contado*incremento

        financiado_m2 = financiado/m2
        
        fin_ant = financiado*anticipo

        valor_cuotas = (financiado - fin_ant)/meses

        #Aqui actualizamos los datos del almacenero

        if (dato.estado == "DISPONIBLE" and dato.asig == "PROYECTO") or (dato.asig == "SOCIOS") or (dato.estado == "SEÑADA" and dato.asig == "PROYECTO"):
            
            ingreso_ventas = ingreso_ventas + contado

            if dato.asig == "SOCIOS":

                unidades_socios = unidades_socios + contado

        #Aqui calculamos IIBB -> IIBB en estado "NO" -- HON.LINK o TERRENO

        if (dato.estado_iibb == "NO"):

            iibb = iibb + contado


        #Aqui calculamos comision -> comsion en estado "NO" -- PROYECTO (No socios)

        if (dato.estado_comision == "NO" and dato.asig == "PROYECTO"):

            comision = comision + contado*0.03 

        #except:

            #desde = "NO DEFINIDO"
            #contado = "NO DEFINIDO"

        venta = 0

        try:
  
            venta= VentasRealizadas.objects.filter(unidad = dato.id).exclude(estado = "BAJA")

            contador = 0

            for v in venta:
                contador += 1

            if contador == 0:
                venta = 0
    
        except:
            venta = 0


        #Aqui vamos armando los m2 totales y los m2 de cocheras

        m2_totales = m2_totales + m2

        try:

            if dato.asig == "PROYECTO":

                sumatoria_contado = sumatoria_contado + contado
                sumatoria_financiado = sumatoria_financiado + financiado
                m2_totales_disp = m2_totales_disp + m2

        except:
            basura = 1
        
        if dato.tipo == "COCHERA":
            cocheras += 1
                           
        #Aqui sumamos los datos

        # m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio

        contado_total += contado

        datos_tabla_unidad.append((dato, m2, desde, dato.id, contado, financiado, financiado_m2, fin_ant, valor_cuotas, venta))


    try:
        
        almacenero = Almacenero.objects.get(proyecto = proyecto)

        #Aqui resto el 6%  --> Ya no resto el 6%, solo guardo los cambios en la BBDD

        almacenero.ingreso_ventas = ingreso_ventas - ingreso_ventas*0.00
        almacenero.save()
        almacenero.unidades_socios = unidades_socios - unidades_socios*0.00
        almacenero.save()
        almacenero.pendiente_comision = comision
        almacenero.save()

        #################### Comento el calculo de IIBB

        # almacenero.pendiente_iibb_tem = (almacenero.cuotas_a_cobrar + iibb + almacenero.pendiente_iibb_tem_link)*0.02235
        
        almacenero.save()

    except:
        context['mensajes'].append("No se encontro un almacenero para vincular")

    cantidad = len(datos_tabla_unidad)

    departamentos = cantidad - cocheras

    #Aqui calculo promedio contado y promedio financiado

    try:

        promedio_contado = sumatoria_contado/m2_totales_disp
        promedio_financiado = sumatoria_financiado/m2_totales_disp

    except:
        promedio_contado = 0
        promedio_financiado = 0
        context['mensajes'].append("No se encontro desglose de superficie") 
    
    proyecto.precio_pricing = promedio_contado
    proyecto.save()

    if request.method == 'GET':

        nuevo_precio = request.GET.items()

        for precio in nuevo_precio:

            precio_nuevo = precio[1]

            date = datetime.date.today()

            b = PricingResumen(
                proyecto = proyecto,
                fecha = date,
                precio_prom_contado = promedio_contado,
                precio_prom_financiado = promedio_financiado,
                base_precio = precio_nuevo,
                anticipo = 0.4,
                cuotas_pend = meses,
            )
            
            b.save()

    otros_datos.append((m2_totales, cantidad, departamentos, cocheras, promedio_contado, promedio_financiado))

    datos_unidades = datos_tabla_unidad

    anticipo = anticipo*100

    context["proyecto"] = proyecto
    context["datos"] = datos
    context["mensaje"] = mensaje
    context["datos_unidades"] = datos_unidades
    context["otros_datos"] = otros_datos
    context["anticipo"] = anticipo
    context["meses"] = meses
    context['m2_totales'] = m2_totales
    context['contado_total'] = contado_total

    return render(request, 'pricing.html', context)

def cargarplano(request,**kwargs):
    if request.method=='POST':
        
        id_proyecto=kwargs['id']
        unidad_id=request.POST.get('unidad')
        plano=request.FILES.get('plano')
        
        unidad=Unidades.objects.get(pk=int(unidad_id))
        if unidad:

            unidad.plano_venta=plano

            unidad.save()
            return redirect('Pricing',id_proyecto)
        else:
            mensaje='No se pudo guardar el pdf'
            return redirect('Pricing',id_proyecto)

def panelpricing(request):

    proyectos = Unidades.objects.all()


    datos  = []

    for proyecto in proyectos:
        datos.append(proyecto.proyecto.nombre)

    datos = list(set(datos))

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        contador = 1

        for dato in palabra_buscar:

            if contador == 1:
                contador += 1
            
            
            if dato[0] == "proyecto":


                proyecto = Proyectos.objects.get(nombre = dato[1])

                id_proyecto = proyecto.id
                
                return redirect( 'Pricing', id_proyecto = id_proyecto )


    return render(request, 'panelpricing.html', {"datos":datos})

def cargarventa(request):

    datos = VentasRealizadas.objects.order_by("-fecha")

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        datos_viejos = datos

        datos = []   

        for i in palabra_buscar:

            if i[0] == "palabra":
        
                palabra_buscar = i[1]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                lista_palabra = palabra.split()

                buscar = (str(i.unidad.proyecto.nombre)+str(i.comprador)+str(i.unidad.piso_unidad)+str(i.unidad.nombre_unidad)+str(i.unidad.tipologia)+str(i.asignacion)+str(i.estado))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)

        datos_unidades = datos
    
    #Aqui termina el filtro

    return render(request, 'cargarventas.html', {'datos':datos})

def cargar_venta(request):

    datos = Unidades.objects.all()

    mensaje = 0

    if request.method == 'POST':

        datos_formulario = request.POST.items()

        comprador = request.POST['comprador']
        precio_venta = request.POST['precio_venta']
        precio_venta_hormigon = request.POST['precio_venta_H']
        anticipo = request.POST['anticipo']
        cuotas_pend = request.POST['cuotas']
        tipo_venta = request.POST['tipo_venta']
        unidad = Unidades.objects.get(id = int(request.POST['unidad']))
        fecha = request.POST['fecha']
        proyecto = Proyectos.objects.get(id = unidad.proyecto.id)
        observaciones = request.POST['observaciones']

        operaciones = VentasRealizadas.objects.filter(unidad = unidad)

        if len(operaciones) > 1:
            mensaje = "Esta unidad se encuentra asignada"

        else:

            #Aqui calculo el precio pricing

            precio_pricing = 0

            if unidad.sup_equiv > 0:

                    m2 = unidad.sup_equiv

            else:

                m2 = unidad.sup_propia + unidad.sup_balcon + unidad.sup_comun + unidad.sup_patio

            try:

                desde = unidad.proyecto.desde

                features_unidad = FeaturesUni.objects.filter(unidad = unidad)

                for f2 in features_unidad:

                    contado = desde*f2.feature.inc

                #Aqui calculamos el contado/financiado
                
                contado = desde*m2           

                precio_pricing = contado

            except:
                pass

            precio_desde = 0
        
            try:

                #Aqui calculo el precio desde --------------------->

                
                desde = Desde.objects.get(presupuesto__proyecto = unidad.proyecto)

                costo = desde.presupuesto.valor

                #Aqui calculo el precio min y sugerido

                costo = (costo/(1 + desde.parametros.tasa_des_p))*(1 + desde.parametros.soft)
                
                costo = costo*(1 + desde.parametros.imprevitso)

                porc_terreno = desde.parametros.terreno/desde.parametros.proyecto.m2*100

                porc_link = desde.parametros.link/desde.parametros.proyecto.m2*100

                aumento_tem = desde.parametros.tem_iibb*desde.parametros.por_temiibb*(1+desde.parametros.ganancia)

                aumento_comer = desde.parametros.comer*(1+(porc_terreno + porc_link)/100)*(1+desde.parametros.ganancia)
                
                costo = costo/(1-aumento_tem- aumento_comer)
                
                m2_proyecto = (desde.parametros.proyecto.m2 - desde.parametros.terreno - desde.parametros.link)

                valor_costo = costo/m2_proyecto

                #Aqui coloco la tasa de descuento

                fecha_entrega =  datetime.datetime.strptime(str(desde.presupuesto.proyecto.fecha_f), '%Y-%m-%d')
                ahora = datetime.datetime.utcnow()
                fecha_inicial = ahora + datetime.timedelta(days = (365*2))

                if fecha_entrega > fecha_inicial:
                    y = fecha_entrega.year - fecha_inicial.year
                    n = fecha_entrega.month - fecha_inicial.month

                    meses = y*12 + n

                    valor_costo = -np.pv(fv=valor_costo, rate=desde.parametros.tasa_des, nper=meses, pmt=0)


                #Calculo el valor final
                
                valor_final = valor_costo*(1 + desde.parametros.ganancia)

                precio_desde = valor_final*m2

            except:
                pass

            b = VentasRealizadas(

                comprador = comprador,
                fecha = fecha,
                tipo_venta = tipo_venta,
                unidad = unidad,
                tipo_unidad = "n",
                proyecto = proyecto,
                m2 = m2,
                asignacion = unidad.asig,
                precio_venta = precio_venta,
                precio_venta_hormigon = precio_venta_hormigon,
                precio_contado = request.POST["precio_contado"],
                precio_pricing = precio_pricing,
                precio_desde = precio_desde,
                anticipo = anticipo,
                cuotas_pend = cuotas_pend,
                observaciones = observaciones,

            )

            b.save()

            unidad.estado = "SEÑADA"
            unidad.save()

            nombre_unidad = str(unidad.piso_unidad) + "-"+ str(unidad.nombre_unidad) + "-"+ str(unidad.proyecto.nombre)

            send = "Han cargado una venta en la unidad {}".format(nombre_unidad)

            id = "-488788454"

            token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

            url = "https://api.telegram.org/bot" + token + "/sendMessage"

            params = {
                'chat_id' : id,
                'text' : send
            }

            requests.post(url, params=params)

            return redirect( 'Cargar Venta' )

    return render(request, 'cargar_venta.html', {'datos':datos, 'mensaje':mensaje})

def editarventa(request, id_venta):

    datos = VentasRealizadas.objects.get(id = id_venta)

    if request.method == 'POST':

        datos.comprador = request.POST['comprador']
        datos.precio_venta = request.POST['precio_venta']
        datos.precio_venta_hormigon = request.POST['precio_venta_H']
        datos.precio_contado = request.POST["precio_contado"]
        datos.anticipo = request.POST['anticipo']
        datos.cuotas_pend = request.POST['cuotas']
        datos.tipo_venta = request.POST['tipo_venta']
        datos.fecha = request.POST['fecha']
        datos.observaciones = request.POST['observaciones']
        datos.save()

        return redirect( 'Cargar Venta' )


    return render(request, 'editar_venta.html', {'datos':datos})

def eliminarventa(request, id_venta):

    datos = VentasRealizadas.objects.get(id = id_venta)

    if request.method == 'POST':

        unidad = Unidades.objects.get(id = datos.unidad.id)

        unidad.estado = "DISPONIBLE"

        unidad.save()

        datos.delete()

        return redirect( 'Cargar Venta' )

    return render(request, 'eliminar_venta.html', {'datos':datos})

def detalleventa(request, id_venta):

    datos = VentasRealizadas.objects.get(id = id_venta)

    return render(request, 'detallesventa.html', {'datos':datos})

def cotizador(request, id_unidad):

    info_coti_email = 0
    datos = Unidades.objects.get(id = id_unidad)
    today = datetime.date.today()
    tiempo_restante = (datos.proyecto.fecha_f.year - today.year)*12 + (datos.proyecto.fecha_f.month - today.month)
    hormigon = Constantes.objects.get(id = 7)
    cliente = 0
    m2 = 0

    if datos.sup_equiv > 0:

        m2 = datos.sup_equiv

    else:

        m2 = datos.sup_propia + datos.sup_balcon + datos.sup_comun + datos.sup_patio

    precio_contado = m2*datos.proyecto.desde

    features_unidad = FeaturesUni.objects.filter(unidad = datos)

    for f2 in features_unidad:

        precio_contado = precio_contado*f2.feature.inc

    desde = round((precio_contado/m2), 4)

    resultados = []

    if request.method == 'POST':

        if len(Clientescontacto.objects.filter( email = request.POST['email'])) > 0:
            cliente = Clientescontacto.objects.get(email =request.POST['email'])
        else:
            cliente = Clientescontacto(

                nombre = request.POST['nombre'],
                apellido = request.POST['apellido'],
                email = request.POST['email']
            )

            cliente.save()
            if request.POST['telefono']:
                cliente.telefono = request.POST['telefono']
                cliente.save()

        anticipo = request.POST["anticipo"]
        anticipo_h = float(request.POST["anticipo"])/hormigon.valor
        cuota_esp = request.POST["cuotas_esp"]
        aporte = request.POST["aporte"]
        cuotas_p = request.POST["cuotas_p"]
        observacion=request.POST['observacion']
        descuento= float(request.POST['descuento'])
        total_cuotas = float(cuota_esp) + float(cuotas_p)*1.65 + float(aporte)

        cuotas_espera = []
        cuotas_pose = []
        aporte_va = []

        for i in range(1):
            cuotas_espera.append(0)
            cuotas_pose.append(0)
            aporte_va.append(0)

        for i in range(int(cuota_esp)):
            cuotas_espera.append(1)
            cuotas_pose.append(0)
            aporte_va.append(0)

        if int(aporte) > 0:
            aporte_va.pop()
            aporte_va.append(int(aporte))

        for d in range(int(cuotas_p)):
            cuotas_pose.append(1.65)

        precio_contado = precio_contado*(1 - descuento)
        valor_auxiliar_espera = npf.npv(rate=(datos.proyecto.tasa_f/100), values=cuotas_espera)
        valor_auxiliar_pose = npf.npv(rate=(datos.proyecto.tasa_f/100), values=cuotas_pose)
        valor_auxiliar_aporte = npf.npv(rate=(datos.proyecto.tasa_f/100), values=aporte_va)
        factor = valor_auxiliar_aporte + valor_auxiliar_espera + valor_auxiliar_pose
        incremento = (total_cuotas/factor) - 1
        precio_finan = ((precio_contado - float(anticipo))*(1 + incremento)) + float(anticipo)

        importe_cuota_esp = (precio_finan-float(anticipo))/total_cuotas
        importe_aporte = importe_cuota_esp*float(aporte)

        if int(cuotas_p) > 0:

            importe_cuota_p = importe_cuota_esp*1.65

        else:

            importe_cuota_p = 0

        importe_cuota_p_h = importe_cuota_p/hormigon.valor
        importe_aporte_h = importe_aporte/hormigon.valor
        importe_cuota_esp_h = importe_cuota_esp/hormigon.valor

        if cuota_esp != 0:
            valor_cuota_espera = importe_cuota_esp/float(cuota_esp)
        else:
            valor_cuota_espera = 0
        if aporte != 0:
            valor_cuota_entrega = importe_aporte/float(aporte)
        else:
            valor_cuota_entrega = 0
        if cuotas_p != 0:
            valor_cuota_pose = importe_cuota_p/float(cuotas_p)
        else:
            valor_cuota_pose = 0

        resultados = [anticipo, anticipo_h, precio_finan, cuota_esp, importe_aporte, cuotas_p, importe_cuota_esp,
            aporte, importe_cuota_p, importe_cuota_p_h, importe_cuota_esp_h, importe_aporte_h, valor_cuota_espera,
            valor_cuota_entrega, valor_cuota_pose, observacion, descuento]

        info_coti_email = str(cuota_esp)+"&"+str(aporte)+"&"+str(cuotas_p)+"&"+str(anticipo)+"&"+str(descuento)+"&"+str(observacion)

    return render(request, 'cotizador.html', {'info_coti_email':info_coti_email, 'tiempo_restante':tiempo_restante, 'datos':datos, 'resultados':resultados, 'precio_contado':precio_contado, 'm2':m2, 'cliente':cliente})

class PdfCotiza(View):

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
        response_servidor = {"messages": "Perri"}
        cliente = Clientescontacto.objects.get(id = id_cliente)
        unidad = Unidades.objects.get(id = id_unidad)
        features_unidad = FeaturesUni.objects.filter(unidad = unidad)
        valor_hormigon = Constantes.objects.get(id = 7)

        today = datetime.date.today()

        # Saludo de bienvenida
        hora_actual = datetime.datetime.now()
        if hora_actual.hour >= 20:
            mensaje_email = "¡Buenas noches {}!".format(cliente.nombre)
        elif hora_actual.hour >= 13:
            mensaje_email = "¡Buenas tardes {}!".format(cliente.nombre)
        else:
            mensaje_email = "¡Buen dia {}!".format(cliente.nombre)

        data = calculo_cotizacion(unidad, features_unidad, info_coti, valor_hormigon)
        # Aqui llamamos y armamos el PDF
      
        template = get_template('cotizadorpdf.html')
        contexto = {'cliente':cliente, 
        'unidad':unidad, 
        'data':data,
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

        # Establecemos conexion con el servidor smtp de gmail
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Construimos el mensaje simple
        
        mensaje = MIMEMultipart()
        mensaje.attach(MIMEText("""
        
{}

Enviamos la cotización de hoy!, cualquier consulta no dudes en comunicarte con nosotros

Ingresa a www.linkinversiones.com.ar para mas información

LINK Desarrollos inmobilairios
Vos confias porque nosotros cumplimos

Por favor no responder este email

        
        """.format(mensaje_email), 'plain'))
        mensaje['From']=settings.EMAIL_HOST_USER
        mensaje['To']=cliente.email
        mensaje['Subject']="LINK - Tu cotización {}".format(cliente.nombre)

        # Esta es la parte para adjuntar (prueba)
        mRoot = settings.MEDIA_ROOT
        plano_adjunto = open(mRoot + "/{}".format(unidad.plano_venta.name), 'rb')
        adjunto_MIME = MIMEBase('application', "octet-stream")
        adjunto_MIME.set_payload(plano_adjunto.read())
        encoders.encode_base64(adjunto_MIME)
        adjunto_MIME.add_header('Content-Disposition', 'attachment; filename="Plano de la unidad.pdf"')
        mensaje.attach(adjunto_MIME)
        adjunto_MIME = MIMEBase('application', "octet-stream")
        adjunto_MIME.set_payload(response.content)
        encoders.encode_base64(adjunto_MIME)
        adjunto_MIME.add_header('Content-Disposition', 'attachment; filename="Tu_cotizacion.pdf"')
        mensaje.attach(adjunto_MIME)
        
        with open(mRoot + "/cotizacion{}{}.pdf".format(cliente.nombre, today).replace(" ", ""), 'wb') as f:
            f.write(response.content)
        
        name_coti_adjunta = "cotizacion{}{}.pdf".format(str(cliente.nombre).replace(" ", ""), today)

        # Envio del mensaje
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                        cliente.email,
                        mensaje.as_string())

        # Aviso por wp
        try:
            jefe_ventas = datosusuario.objects.get(cargo = "JEFE DE VENTAS")
            send= "Hola!, {} ha enviado una cotización a {} de la siguiente unidad: {}{} - {}".format(request.user.username, cliente.nombre, unidad.piso_unidad, unidad.nombre_unidad, unidad.proyecto)
            bot_wp = WABot(response_servidor)
            bot_wp.send_message_user(str(jefe_ventas.Telefono), send)
            
        except:
            pass
        try:
            send= "Hola {}!, enviamos tu cotización al siguiente email {}, cualquier error o consulta no dudes en consultar! - Equipo Link".format(cliente.nombre, cliente.email)
            bot_wp = WABot(response_servidor)
            bot_wp.send_message_user(str(cliente.telefono), send)
        except:
            pass

        # Creo la consulta

        usuario = datosusuario.objects.get(identificacion = request.user.username)

        try:
            tipologia = Tipologia.objects.get(nombre = unidad.tipologia)
        except:
            tipologia = Tipologia(
                nombre = unidad.tipologia
            )
            tipologia.save()

        #try:
        new_consulta = Consulta(
            fecha = today,
            proyecto = unidad.proyecto,
            cliente = cliente,
            medio_contacto = 'RECOMENDACION',
            usuario = usuario,
            adjunto_propuesta = (name_coti_adjunta),
        )

        new_consulta.save()
        new_consulta.tipologia2.add(tipologia)
        new_consulta.save()

        #except:
            #pass
        
        return redirect('modificarcliente', id = cliente.id)

def featuresproject(request, id_proj):

    if request.method == 'POST':
        data_post = request.POST.items()
        for d in data_post:

            if d[0] != 'csrfmiddlewaretoken':
                aux = d[0].split(sep='&')

                if len(FeaturesUni.objects.filter(feature__nombre = aux[0], unidad = int(aux[1]))) == 1 and d[1] == "off":
                    feature_un = FeaturesUni.objects.filter(feature__nombre = aux[0], unidad = int(aux[1]))
                    feature_un.delete()

                if len(FeaturesUni.objects.filter(feature__nombre = aux[0], unidad = int(aux[1]))) == 0 and d[1] == "on":
                
                    unidad = Unidades.objects.get(id = int(aux[1]))
                    feature = FeaturesProjects.objects.get(proyecto = unidad.proyecto, nombre = aux[0])
                
                    feature_un = FeaturesUni(
                        feature = feature,
                        unidad = unidad)
                    feature_un.save()

    unidades = Unidades.objects.filter(proyecto__id = id_proj).order_by("orden")
  
    features = FeaturesProjects.objects.filter(proyecto__id = id_proj)

    data = []

    for u in unidades:

        unid_features = []

        for f in features:
            if len(FeaturesUni.objects.filter(feature = f, unidad = u)) == 1:
                unid_features.append(("SI", f))
            if len(FeaturesUni.objects.filter(feature = f, unidad = u)) == 0:
                unid_features.append(("NO", f))

        if u.sup_equiv > 0:

            m2 = round(u.sup_equiv, 2)

        else:

            m2 = round((u.sup_propia + u.sup_balcon + u.sup_comun + u.sup_patio), 2)

        base = m2*u.proyecto.desde
        final = base

        features_unidad = FeaturesUni.objects.filter(unidad = u)

        for f2 in features_unidad:

            final = final*f2.feature.inc

        u.contado = final
        u.save()

        data.append((u, unid_features, m2, base, final))

    return render(request, 'featuresproject.html', {'features':features, 'data':data})

class descargadeventas(TemplateView):

    def get(self, request, *args, **kwargs):
        
        wb = Workbook()

        #Aqui coloco la formula para calcular

        datos = VentasRealizadas.objects.order_by("fecha")

        ws = wb.active
        ws.title = "ADVERTENCIA"

        ws.merge_cells("A2:K2")
        ws["A2"] = "UNA ADVERTENCIA ANTES DE AVANZAR"

        ws["A2"].alignment = Alignment(horizontal = "left")
        ws["A2"].font = Font(bold = True, color= "23346D", size = 20)

        ws.merge_cells("A5:K25")
        ws["A5"] = """
        La información que contiene este documento se considera de caracter CONFIDENCIAL.

         Esto quiere decir debes garantizar su protección y no debe ser divulgada sin el consentimiento de Link Inversiones S.R.L.
         
         Algunas recomendaciones:

         1 - Habla con tu responsable de área antes de pasar este documento
         2 - Si usas este documento fuera de las computadoras de la empresa, borra el archivo y vacia la papelera
         
         Gracias por tu atención

         Saludos!
         """
        ws["A5"].alignment = Alignment(horizontal = "left", vertical = "center", wrap_text=True)
        ws["A5"].font = Font(bold = True)
        
        cont = 1
        
        for d in datos:

            if cont == 1:
                ws = wb.create_sheet("My sheet")
                ws.title = "REGISTRO"
                ws["A"+str(cont)] = "FECHA"
                ws["B"+str(cont)] = "PROYECTO"
                ws["C"+str(cont)] = "COMPRADOR"
                ws["D"+str(cont)] = "PISO"
                ws["E"+str(cont)] = "NOM"
                ws["F"+str(cont)] = "TIPO"
                ws["G"+str(cont)] = "TIPOLOGIA"
                ws["H"+str(cont)] = "SUPERFICIE"
                ws["I"+str(cont)] = "ASIGNACIÓN"
                ws["J"+str(cont)] = "PRECIO DE VENTA"
                ws["K"+str(cont)] = "ANOTACIONES"


                ws["A"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["I"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["J"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["K"+str(cont)].alignment = Alignment(horizontal = "center")


                ws["A"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["A"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["B"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["B"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["C"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["C"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["D"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["D"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["E"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["E"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["F"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["F"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["G"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["G"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["H"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["H"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["I"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["I"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["J"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["J"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["K"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["K"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")


                ws.column_dimensions['A'].width = 12
                ws.column_dimensions['B'].width = 12
                ws.column_dimensions['C'].width = 22
                ws.column_dimensions['D'].width = 6.86
                ws.column_dimensions['E'].width = 5
                ws.column_dimensions['F'].width = 15
                ws.column_dimensions['G'].width = 10
                ws.column_dimensions['H'].width = 10.29
                ws.column_dimensions['I'].width = 11.86
                ws.column_dimensions['J'].width = 16
                ws.column_dimensions['K'].width = 40

                ws["A"+str(cont+1)] = d.fecha
                ws["B"+str(cont+1)] = d.proyecto.nombre
                ws["C"+str(cont+1)] = d.comprador
                ws["D"+str(cont+1)] = d.unidad.piso_unidad
                ws["E"+str(cont+1)] = d.unidad.nombre_unidad
                ws["F"+str(cont+1)] = d.unidad.tipo
                ws["G"+str(cont+1)] = d.unidad.tipologia
                ws["H"+str(cont+1)] = d.m2
                ws["I"+str(cont+1)] = d.asignacion
                ws["J"+str(cont+1)] = d.precio_venta
                ws["K"+str(cont+1)] = d.observaciones


                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].font = Font(bold = True)
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].number_format = '#,##0.00_-'
                ws["I"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["J"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["K"+str(cont+1)].alignment = Alignment(horizontal = "left")
  

                cont += 1

            else:
                ws = wb["REGISTRO"]

                ws["A"+str(cont+1)] = d.fecha
                ws["B"+str(cont+1)] = d.proyecto.nombre
                ws["C"+str(cont+1)] = d.comprador
                ws["D"+str(cont+1)] = d.unidad.piso_unidad
                ws["E"+str(cont+1)] = d.unidad.nombre_unidad
                ws["F"+str(cont+1)] = d.unidad.tipo
                ws["G"+str(cont+1)] = d.unidad.tipologia
                ws["H"+str(cont+1)] = d.m2
                ws["I"+str(cont+1)] = d.asignacion
                ws["J"+str(cont+1)] = d.precio_venta
                ws["K"+str(cont+1)] = d.observaciones


                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].font = Font(bold = True)
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].number_format = '#,##0.00_-'
                ws["I"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["J"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["K"+str(cont+1)].alignment = Alignment(horizontal = "left")

                cont += 1

        #Establecer el nombre del archivo
        nombre_archivo = "RegistroVentas.xls"
        #Definir tipo de respuesta que se va a dar
        response = HttpResponse(content_type = "application/ms-excel")
        contenido = "attachment; filename = {0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response

class DescargaPricing(TemplateView):

    def get(self, request, id_proyecto, *args, **kwargs):
        
        wb = Workbook()

        id_proyecto = id_proyecto

        # -----------> Toda la parte de calculo de información

        # Traemos la información necesaria

        proyecto = Proyectos.objects.get(id = id_proyecto)
        datos = Unidades.objects.filter(proyecto = proyecto)

        # Calculamos/establecemos algunos parametros

        fecha_entrega =  datetime.datetime.strptime(str(proyecto.fecha_f), '%Y-%m-%d')
        ahora = datetime.datetime.utcnow()
        y = fecha_entrega.year - ahora.year
        n = fecha_entrega.month - ahora.month
        meses = y*12 + n
        anticipo = 0.4

        # Variables a calcular en el proceso

        financiado = 0
        financiado_m2 = 0
        fin_ant = 0
        valor_cuotas = 0
        mensaje = 2
        otros_datos = []
        datos_unidad = []
        m2_totales = 0
        m2_totales_disp = 0
        cocheras = 0
        ingreso_ventas = 0
        iibb = 0
        comision = 0
        unidades_socios = 0
        sumatoria_contado = 0
        sumatoria_financiado = 0

        # Proceso 1: Calculo de datos
        for dato in datos:

            # Calculamos los m2 equivalente y total

            m2_equivalente = round(dato.sup_equiv, 2)
            m2_total = round((dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio), 2)

            # Formula del m2 para calculos

            if dato.sup_equiv > 0:
                m2 = round(dato.sup_equiv, 2)
            else:
                m2 = round((dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio), 2)

            # Calculamos el precio contado y financiado de ser posible, sino establecemos que no esta definido

            
            contado = m2*dato.proyecto.desde
            aumento = 1
            desde = dato.proyecto.desde
            param_uni = FeaturesUni.objects.filter(unidad = dato)
            features_unidad = FeaturesUni.objects.filter(unidad = dato)

            for f2 in features_unidad:

                contado = contado*f2.feature.inc
                aumento = 1*f2.feature.inc
            

            #Aqui calculamos el contado/financiado
         
            values = [0]
            for m in range((meses)):
                values.append(1)
            anticipo = 0.4
            valor_auxiliar = np.npv(rate=(dato.proyecto.tasa_f/100), values=values)
            incremento = (meses/(1-anticipo)/(((anticipo/(1-anticipo))*meses)+valor_auxiliar))
            financiado = contado*incremento
            financiado_m2 = financiado/m2                
            fin_ant = financiado*anticipo
            valor_cuotas = (financiado - fin_ant)/meses


            # Aqui establecemos los datos de la venta

            venta = 0
            try:    
                venta= VentasRealizadas.objects.filter(unidad = dato.id).exclude(estado = "BAJA")
                contador = 0
                for v in venta:
                    contador += 1
                if contador == 0:
                    venta = 0        
            except:
                venta = 0

            #Aqui vamos armando los m2 totales , m2 de proyecto, cantidad de cocheras

            m2_totales = m2_totales + m2
            if dato.estado == "DISPONIBLE":
                try:
                    if dato.asig == "PROYECTO":
                        sumatoria_contado = sumatoria_contado + contado
                        sumatoria_financiado = sumatoria_financiado + financiado
                        m2_totales_disp = m2_totales_disp + m2
                except:
                    pass           
            if dato.tipo == "COCHERA":
                cocheras += 1
                            
            #Aqui sumamos los datos

            datos_unidad.append((dato, m2_equivalente, m2_total, aumento,  contado, desde, financiado, financiado_m2, venta, param_uni))

        # Ordenamos las unidades

        datos_unidad = sorted(datos_unidad, key=lambda unidad : unidad[0].orden)


        #Aqui calculo promedio contado y promedio financiado y otros datos que usaremos en el resumen

        cantidad = len(datos_unidad)
        departamentos = cantidad - cocheras
        promedio_contado = sumatoria_contado/m2_totales_disp
        promedio_financiado = sumatoria_financiado/m2_totales_disp

        # Proceso 2: Creado del Excel

        ws = wb.active
        ws.title = "ADVERTENCIA"

        ws.merge_cells("A2:K2")
        ws["A2"] = "UNA ADVERTENCIA ANTES DE AVANZAR"

        ws["A2"].alignment = Alignment(horizontal = "left")
        ws["A2"].font = Font(bold = True, color= "23346D", size = 20)

        ws.merge_cells("A5:K25")
        ws["A5"] = """
        La información que contiene este documento se considera de caracter CONFIDENCIAL.
        
         Esto quiere decir debes garantizar su protección y no debe ser divulgada sin el consentimiento de Link Inversiones S.R.L.
         
         Algunas recomendaciones:

         1 - Habla con tu responsable de área antes de pasar este documento
         2 - Si usas este documento fuera de las computadoras de la empresa, borra el archivo y vacia la papelera
         
         Gracias por tu atención

         Saludos!
         """
        ws["A5"].alignment = Alignment(horizontal = "left", vertical = "center", wrap_text=True)
        ws["A5"].font = Font(bold = True)

        ws = wb.create_sheet("My sheet")
        ws.title = "RESUMEN"

        ws["A2"] = "PROYECTO"
        ws["A3"] = "FECHA DE ENTREGA"
        ws["A4"] = "CANTIDAD DE UNIDADES"
        ws["A5"] = "M2 TOTALES"
        ws["A6"] = "PRECIO DE REPOSICIÓN CONTADO"
        ws["A7"] = "PRECIO DE REPOSICIÓN FINANCIADO"
        ws["A8"] = "PRECIO DESDE"

        ws["A2"].font = Font(bold = True, color= "FDFFFF")
        ws["A2"].fill =  PatternFill("solid", fgColor= "23346D")
        ws["A3"].font = Font(bold = True, color= "FDFFFF")
        ws["A3"].fill =  PatternFill("solid", fgColor= "23346D")
        ws["A4"].font = Font(bold = True, color= "FDFFFF")
        ws["A4"].fill =  PatternFill("solid", fgColor= "23346D")
        ws["A5"].font = Font(bold = True, color= "FDFFFF")
        ws["A5"].fill =  PatternFill("solid", fgColor= "23346D")
        ws["A6"].font = Font(bold = True, color= "FDFFFF")
        ws["A6"].fill =  PatternFill("solid", fgColor= "23346D")
        ws["A7"].font = Font(bold = True, color= "FDFFFF")
        ws["A7"].fill =  PatternFill("solid", fgColor= "23346D")
        ws["A8"].font = Font(bold = True, color= "FDFFFF")
        ws["A8"].fill =  PatternFill("solid", fgColor= "23346D")

        ws["B2"] = proyecto.nombre
        ws["B2"].font = Font(bold = True)
        ws["B2"].alignment = Alignment(horizontal = "center")
        ws["B3"] = fecha_entrega
        ws["B4"] = cantidad
        ws["B5"] = m2_totales
        ws["B6"] = promedio_contado
        ws["B7"] = promedio_financiado
        ws["B8"] = dato.proyecto.desde
 
        ws["B5"].number_format = '#,##0.00_-"M2"'
        ws["B6"].number_format = '"$ "#,##0.00_-'
        ws["B7"].number_format = '"$ "#,##0.00_-'
        ws["B8"].number_format = '"$ "#,##0.00_-'



        ws.column_dimensions['A'].width = 40
        ws.column_dimensions['B'].width = 20
        
        cont = 1
        
        for d in datos_unidad:

            if cont == 1:
                ws = wb.create_sheet("My sheet")
                ws.title = "DETALLE"
                ws["A"+str(cont)] = "PISO"
                ws["B"+str(cont)] = "N"
                ws["C"+str(cont)] = "TIPO"
                ws["D"+str(cont)] = "TIPOLOGIA"
                ws["E"+str(cont)] = "M2 EQUIV"
                ws["F"+str(cont)] = "M2"
                ws["G"+str(cont)] = "ESTADO"
                ws["H"+str(cont)] = "CONTADO"
                ws["I"+str(cont)] = "CONTADO M2"
                ws["J"+str(cont)] = "FINANCIADO"
                ws["K"+str(cont)] = "FINANCIADO M2"
                ws["L"+str(cont)] = "ASIGNACIÓN"
                ws["M"+str(cont)] = "VENDIDO A"
                ws["N"+str(cont)] = "%V"

                ws["A"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["I"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["J"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["K"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["L"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["M"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["N"+str(cont)].alignment = Alignment(horizontal = "center")
                

                ws["A"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["A"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["B"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["B"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["C"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["C"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["D"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["D"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["E"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["E"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["F"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["F"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["G"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["G"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["H"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["H"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["I"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["I"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["J"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["J"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["K"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["K"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["L"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["L"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["M"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["M"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                ws["N"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["N"+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")

                features_project = FeaturesProjects.objects.filter(proyecto = proyecto)

                alphabet_string = string.ascii_uppercase
                alphabet_list = list(alphabet_string)
                cont_alph = 14
                
                for f in features_project:

                    ws[str(alphabet_list[cont_alph])+str(cont)] = f.nombre
                    ws.column_dimensions[str(alphabet_list[cont_alph])].width = 15
                    ws[str(alphabet_list[cont_alph])+str(cont)].alignment = Alignment(horizontal = "center")
                    ws[str(alphabet_list[cont_alph])+str(cont)].font = Font(bold = True, color= "FDFFFF")
                    ws[str(alphabet_list[cont_alph])+str(cont)].fill =  PatternFill("solid", fgColor= "23346D")
                    cont_alph += 1
                
 
                ws.column_dimensions['A'].width = 12
                ws.column_dimensions['B'].width = 8
                ws.column_dimensions['C'].width = 18
                ws.column_dimensions['D'].width = 15
                ws.column_dimensions['E'].width = 10
                ws.column_dimensions['F'].width = 10
                ws.column_dimensions['G'].width = 12
                ws.column_dimensions['H'].width = 15
                ws.column_dimensions['I'].width = 15
                ws.column_dimensions['J'].width = 15
                ws.column_dimensions['K'].width = 15
                ws.column_dimensions['L'].width = 15
                ws.column_dimensions['M'].width = 20
                ws.column_dimensions['N'].width = 10
                



                # Aqui empiezan los datos

                ws["A"+str(cont+1)] = d[0].piso_unidad
                ws["B"+str(cont+1)] = d[0].nombre_unidad
                ws["C"+str(cont+1)] = d[0].tipo
                ws["D"+str(cont+1)] = d[0].tipologia
                ws["E"+str(cont+1)] = d[1]
                ws["F"+str(cont+1)] = d[2]
                ws["G"+str(cont+1)] = d[0].estado
                ws["H"+str(cont+1)] = d[4]
                ws["I"+str(cont+1)] = d[5]
                ws["J"+str(cont+1)] = d[6]
                ws["K"+str(cont+1)] = d[7]
                ws["L"+str(cont+1)] = d[0].asig

                if d[8] == 0:

                    ws["M"+str(cont+1)] = "SIN COMPRADOR"

                else:
                    ws["M"+str(cont+1)] = d[8][0].comprador

                ws["N"+str(cont+1)] = d[3]


                cont_alph = 14
                
                for f in features_project:

                    aux = len(FeaturesUni.objects.filter(feature = f, unidad = d[0]))

                    if aux:

                        ws[str(alphabet_list[cont_alph])+str(cont+1)] = "SI"
                        ws[str(alphabet_list[cont_alph])+str(cont+1)].alignment = Alignment(horizontal = "center")

                    else:
                        ws[str(alphabet_list[cont_alph])+str(cont+1)] = "NO"
                        ws[str(alphabet_list[cont_alph])+str(cont+1)].alignment = Alignment(horizontal = "center")

                    cont_alph += 1

                


                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].font = Font(bold = True)
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].number_format = '#,##0.00_-"M2"'
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont+1)].number_format = '#,##0.00_-"M2"'
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["I"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["I"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["J"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["K"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["L"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["M"+str(cont+1)].alignment = Alignment(horizontal = "left")
                ws["N"+str(cont+1)].alignment = Alignment(horizontal = "center")  

                cont += 1

            else:
                ws = wb["DETALLE"]

                ws["A"+str(cont+1)] = d[0].piso_unidad
                ws["B"+str(cont+1)] = d[0].nombre_unidad
                ws["C"+str(cont+1)] = d[0].tipo
                ws["D"+str(cont+1)] = d[0].tipologia
                ws["E"+str(cont+1)] = d[1]
                ws["F"+str(cont+1)] = d[2]
                ws["G"+str(cont+1)] = d[0].estado
                ws["H"+str(cont+1)] = d[4]
                ws["I"+str(cont+1)] = d[5]
                ws["J"+str(cont+1)] = d[6]
                ws["K"+str(cont+1)] = d[7]
                ws["L"+str(cont+1)] = d[0].asig

                if d[8] == 0:

                    ws["M"+str(cont+1)] = "SIN COMPRADOR"

                else:
                    ws["M"+str(cont+1)] = d[8][0].comprador
                    
                ws["N"+str(cont+1)] = d[3]

                cont_alph = 14
                
                for f in features_project:

                    aux = len(FeaturesUni.objects.filter(feature = f, unidad = d[0]))

                    if aux:

                        ws[str(alphabet_list[cont_alph])+str(cont+1)] = "SI"
                        ws[str(alphabet_list[cont_alph])+str(cont+1)].alignment = Alignment(horizontal = "center")

                    else:
                        ws[str(alphabet_list[cont_alph])+str(cont+1)] = "NO"
                        ws[str(alphabet_list[cont_alph])+str(cont+1)].alignment = Alignment(horizontal = "center")

                    cont_alph += 1

                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].font = Font(bold = True)
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].number_format = '#,##0.00_-"M2"'
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont+1)].number_format = '#,##0.00_-"M2"'
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["I"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["I"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["J"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["K"+str(cont+1)].number_format = '"$ "#,##0.00_-'
                ws["L"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["M"+str(cont+1)].alignment = Alignment(horizontal = "left")
                ws["N"+str(cont+1)].alignment = Alignment(horizontal = "center")

                cont += 1

        #Establecer el nombre del archivo
        nombre_archivo = "PRICING {}.xls".format(proyecto.nombre)
        #Definir tipo de respuesta que se va a dar
        response = HttpResponse(content_type = "application/ms-excel")
        contenido = "attachment; filename = {0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response


