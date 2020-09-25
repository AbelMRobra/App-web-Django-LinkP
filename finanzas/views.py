from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView  
from presupuestos.models import Proyectos, Presupuestos, Constantes, Modelopresupuesto
from .models import Almacenero, CuentaCorriente, Cuota, Pago, RegistroAlmacenero, ArchivosAdmFin
from proyectos.models import Unidades
from ventas.models import Pricing, VentasRealizadas
import datetime
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side


# Create your views here.

def resumencredinv(request):

    busqueda = 1
    datos_almacenados = ArchivosAdmFin.objects.filter(resumen_credito_inv__isnull = False)
    datos = 0
    fecha = 0

    fechas = []

    for dato in datos_almacenados:
        if dato.resumen_credito_inv: 
            fechas.append((dato.fecha, str(dato.fecha)))

    fechas = list(set(fechas))

    fechas.sort( reverse=True)

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAdmFin.objects.get(fecha = dato[1])
                busqueda = 0
                fecha = dato[1]


    datos = {"fechas":fechas,
        "busqueda":busqueda,
        "datos":datos,
        "fecha":fecha}

    return render(request, 'resumencredinv.html', {"datos":datos})


def eliminar_pago(request, id_pago):

    pago = Pago.objects.get(id = id_pago)

    if request.method == 'POST':

        pago.delete()

        return redirect('Pagos', id_cuota = pago.cuota.id)

    return render(request, 'eliminar_pago.html', {"pago":pago})


def editar_cuota(request, id_cuota):

    cuota = Cuota.objects.get(id = id_cuota)

    if request.method == 'POST':

        datos = request.POST.items()

        for i in datos:

            if  'fecha' in i[0] and i[1] != "":

                cuota.fecha = str(i[1])

                cuota.save()

            if  'concepto' in i[0] and i[1] != "":

                cuota.concepto = str(i[1])

                cuota.save()

            if  'precio' in i[0] and i[1] != "":

                cuota.precio = float(i[1])

                cuota.save()

            if  'tipo_venta' in i[0]:

                if i[1] == "HORM":

                    cuota.constante = Constantes.objects.get(nombre = "Hº VIVIENDA")
                    
                    cuota.save()

                if i[1] == "USD":

                    cuota.constante = Constantes.objects.get(nombre = "USD")

                    cuota.save()

        return redirect('Cuenta corriente venta', id_cliente = cuota.cuenta_corriente.id)

    return render(request, 'editar_cuota.html', {"cuota":cuota})

def agregar_cuota(request, id_cuenta):

    cuenta = CuentaCorriente.objects.get(id = id_cuenta)

    if request.method == 'POST':

        datos = request.POST.items()

        for i in datos:


            if  'fecha' in i[0]:

                fecha = i[1]

            if  'concepto' in i[0]:

                concepto = i[1]

            if  'precio' in i[0]:

                precio = i[1]

            if  'tipo_venta' in i[0]:

                if i[1] == "HORM":
                    constante = Constantes.objects.get(nombre = "Hº VIVIENDA"),

                if i[1] == "USD":
                    constante = Constantes.objects.get(nombre = "USD"),

                precio_pesos = float(precio)/constante[0].valor

                try:

                    c = Cuota(

                        cuenta_corriente = cuenta,
                        fecha = fecha,
                        precio = float(precio),
                        constante = constante[0],
                        precio_pesos = precio_pesos,                        
                        concepto = concepto,
                        )

                    c.save()

                    return redirect('Cuenta corriente venta', id_cliente = cuenta.id)

                except:

                    print("Hay un error")

    return render(request, 'agregar_cuota.html', {"cuenta":cuenta})

def pagos(request, id_cuota):

    cuota = Cuota.objects.get(id = id_cuota)

    datos = Pago.objects.filter(cuota = cuota)

    return render(request, 'pagos.html', {'datos':datos, 'cuota':cuota})

def agregar_pagos(request, id_cuota):

    cuota = Cuota.objects.get(id = id_cuota)

    if request.method == 'POST':

        datos_crear = request.POST.items()

        pagado = 0

        for i in datos_crear:

            if  'fecha' in i[0]:

                fecha = i[1]

            if  'documento1' in i[0]:

                documento1 = i[1]

            if  'documento2' in i[0]:

                documento2 = i[1]

            if  'precio1' in i[0]:

                cotizacion = i[1]

                precio1 = float(pagado)/float(cotizacion)

            if  'precio2' in i[0]:

                precio2 = i[1]

                pagado = precio2

        c = Pago(

            cuota = cuota,
            fecha = fecha,
            pago = precio1,
            pago_pesos = float(precio2),                       
            documento_1 = documento1,
            documento_2 = documento2,
            )

        c.save()

        return redirect('Pagos', id_cuota = cuota.id)

    return render(request, 'agregar_pagos.html', {'cuota':cuota})

def eliminar_cuota(request, id_cuota):

    cuota = Cuota.objects.get(id = id_cuota)

    if request.method == 'POST':

        cuota.delete()

        return redirect('Cuenta corriente venta', id_cliente = cuota.cuenta_corriente.id)

    return render(request, 'eliminar_cuota.html', {"cuota":cuota})

def crearcuenta(request, id_proyecto):

    proyecto = Proyectos.objects.get(id = id_proyecto)

    datos = VentasRealizadas.objects.filter(proyecto = id_proyecto)

    if request.method == 'POST':

        datos_crear = request.POST.items()

        for i in datos_crear:

            if i[0] == 'ventas':

                b = CuentaCorriente(
                    venta = VentasRealizadas.objects.get(id=i[1]),

                    )

                b.save()

            if  'fecha' in i[0]:

                fecha = i[1]

            if  'concepto' in i[0]:

                concepto = i[1]

            if  'precio' in i[0]:

                precio = i[1]

            if  'cuotas' in i[0]:

                cuotas = i[1]

                constante = Constantes.objects.get(nombre = "Hº VIVIENDA")

                precio_pesos = float(precio)/constante.valor

                for i in range(int(cuotas)):

                    c = Cuota(

                        cuenta_corriente = b,
                        fecha = fecha,
                        precio = float(precio),
                        constante = constante,
                        precio_pesos = precio_pesos,                        
                        concepto = concepto,
                        )

                    c.save()

                    fecha_objeto = datetime.datetime.strptime(str(fecha), '%Y-%m-%d')

                    fecha_dia = fecha_objeto.day

                    if fecha_objeto.month == 12:

                        fecha_mes = 1

                        fecha_ano = (fecha_objeto.year + 1)

                    else:

                        fecha_mes = (fecha_objeto.month + 1)

                        fecha_ano = fecha_objeto.year

                    hoy = date.today()

                    fecha = hoy.replace(fecha_ano, fecha_mes, fecha_dia)

        return redirect('Cuenta corriente venta', b.id)


    return render(request, 'crearcuenta.html', {"datos":datos, "proyecto":proyecto})


def ctacteproyecto(request, id_proyecto):

    proyecto = Proyectos.objects.get(id = id_proyecto)

    datos = CuentaCorriente.objects.filter(venta__proyecto = proyecto)

    return render(request, 'ctacteproyecto.html', {"proyecto":proyecto, "datos":datos})

    ### Armando resumen de cuenta corriente


def totalcuentacte(request):

    proyectos = Proyectos.objects.all()

    datos_primeros = []

    for proyecto in proyectos:

        cuotas = Cuota.objects.filter(cuenta_corriente__venta__proyecto = proyecto)

        if len(cuotas)>0:
            datos_primeros.append(proyecto)

    #Hasta aqui tenemos todos los proyectos y todas las cuotas quitando a los proyectos en 0

    
    #Establecemos un rango para hacer el cash de ingreso
    
    fecha_inicial = datetime.date.today()

    fechas = []

    contador = 0
    contador_year = 1

    for f in range(26):


        if (fecha_inicial.month + contador) == 13:
            
            year = fecha_inicial.year + contador_year
            
            fecha_cargar = date(year, 1, fecha_inicial.day)

            fechas.append(fecha_cargar)
            
            contador_year += 1

            contador = - (12 - contador)

        else:

            mes = fecha_inicial.month + contador

            year = fecha_inicial.year + contador_year - 1

            fecha_cargar = date(year, mes, fecha_inicial.day)

            fechas.append(fecha_cargar)

        contador += 1


    #Aqui buscamos agrupar proyecto - sumatorias de cuotas y pagos - mes
    
    datos_segundos = []

    fecha_inicial = 0

    for f in fechas:

        datos_terceros = []

        for p in datos_primeros:

            if fecha_inicial == 0:

                fecha_inicial = f

            else:
                cuotas = Cuota.objects.filter(fecha__range = (fecha_inicial, f))
                
                pagos = Pago.objects.filter(fecha__range = (fecha_inicial, f))

                total_cuotas = 0
                total_pagado = 0
                saldo = 0

                if len(cuotas)>0:

                    for c in cuotas:

                        total_cuotas = total_cuotas + c.precio*c.constante.valor

                if len(pagos)>0:

                    for p in pagos:

                        total_pagado = total_pagado + p.pago*p.cuota.constante.valor

                saldo = total_cuotas-total_pagado

                
                dato = (p, f, saldo)
                datos_terceros.append(dato)

        datos_segundos.append(datos_terceros)

        print(datos_segundos)
        

    return render(request, 'totalcuentas.html', {"fechas":fechas, "datos":datos_segundos, "datos_primero":datos_primeros})



def resumenctacte(request, id_cliente):

    ctacte = CuentaCorriente.objects.get(id = id_cliente)

    cuotas = Cuota.objects.filter(cuenta_corriente = ctacte)

    nombre_conceptos = []

    datos = []

    for cuota in cuotas:

        nombre_conceptos.append(cuota.concepto)

    nombre_conceptos = set(nombre_conceptos)

    saldo_total_pesos = 0

    for nombre in nombre_conceptos:

        moneda = 0
        total_moneda = 0
        cuotas_t = 0
        total_pagado = 0


        for cuota in cuotas:

            if nombre == cuota.concepto:

                moneda = cuota.constante
                total_moneda = total_moneda + cuota.precio

                cuotas_t = (cuotas_t + 1)

                pagos = Pago.objects.filter(cuota = cuota)

                for pago in pagos:

                    total_pagado = total_pagado + pago.pago

        saldo_moneda = total_moneda - total_pagado
        saldo_pesos = saldo_moneda*moneda.valor
        saldo_total_pesos = saldo_total_pesos + saldo_pesos

        datos.append((nombre, moneda, total_moneda, cuotas_t, total_pagado, saldo_moneda, saldo_pesos))

    #Aqui creo la curva de ingresos por mes

    fechas = []

    for cuota in cuotas:

        fecha_nueva = date(cuota.fecha.year, cuota.fecha.month, 1 )
        fechas.append(fecha_nueva)

    fechas = list(set(fechas))

    fechas.sort()

    datos_cuotas = []

    deuda_md = 0
    pago_md = 0

    for fecha in fechas:

        deuda_md = 0
        pago_md = 0

        hoy = datetime.date.today()

        if fecha < hoy:

            print("viejo")

        else:

            if fecha.month == 12:

                año = fecha.year + 1

                fecha_final = date(año, 1, fecha.day)

            else:

                mes = fecha.month + 1

                fecha_final = date(fecha.year, mes, fecha.day)

            fecha_final = fecha_final + timedelta(days = -1)

            cuotas = Cuota.objects.filter(fecha__range = (fecha, fecha_final), cuenta_corriente  = ctacte)

            for cuota in cuotas:

                pagos = Pago.objects.filter(cuota = cuota)

                for pago in pagos:

                    pago_md = pago_md + pago.pago*pago.cuota.constante.valor 

                deuda_md = deuda_md + cuota.precio*cuota.constante.valor 

            saldo_md = deuda_md - pago_md

            datos_cuotas.append((fecha, saldo_md))
        

    return render(request, 'resumencta.html', {"ctacte":ctacte, "datos":datos, "datos_cuotas":datos_cuotas, "saldo_total_pesos":saldo_total_pesos})

def ctactecliente(request, id_cliente):

    ctacte = CuentaCorriente.objects.get(id = id_cliente)

    cuotas = Cuota.objects.filter(cuenta_corriente = ctacte)

    pagos = Pago.objects.all()

    datos_cuenta = []

    for cuota in cuotas:

        pago_cuota = 0
        saldo_cuota = 0
        pagos_realizados = []

        for pago in pagos:

            if pago.cuota == cuota:

                pago_cuota = pago_cuota + pago.pago

                pagos_realizados.append(pago)

        saldo_cuota = cuota.precio - pago_cuota
        saldo_pesos = saldo_cuota*cuota.constante.valor

        datos_cuenta.append((cuota, pago_cuota, saldo_cuota, saldo_pesos, pagos_realizados))

    datos_cuenta = sorted(datos_cuenta, key=lambda datos: datos[0].fecha)

    return render(request, 'ctacte.html', {"ctacte":ctacte, "datos_cuenta":datos_cuenta})

def panelctacote(request):

    datos_ventas = VentasRealizadas.objects.all()

    datos = []

    for dato in datos_ventas:

        datos.append((dato.proyecto.id, dato.proyecto.nombre))

    datos = set(datos)

    if request.method == 'POST':

        proyecto_elegido = request.POST.items()

        for i in proyecto_elegido:

            if i[0] == 'proyecto':

                return redirect('Cuenta corriente proyecto', id_proyecto=i[1])

    return render(request, 'panelctacte.html', {"datos":datos})

def ingresounidades(request):

    datos = VentasRealizadas.objects.filter(unidad__estado = "SEÑADA")


    if request.method == 'POST':

        proyecto_elegido = request.POST.items()

        for i in proyecto_elegido:

            if i[0] == 'ingresar':

                unidad = Unidades.objects.get(id = i[1])

                unidad.estado = "VENDIDA"

                unidad.save()


    return render(request, 'ingresounidades.html',{'datos':datos})

def consolidado(request):

    datos = Almacenero.objects.all()

    datos_completos = []
    datos_finales = []

    costo_total = 0
    ingresos_total = 0
    descuento_total = 0


    for dato in datos:

        presupuesto = "NO"

        pricing = "NO"

        almacenero = dato

        presupuesto = Presupuestos.objects.get(proyecto = dato.proyecto)

        #Aqui calculo el IVA sobre compras

        iva_compras = (presupuesto.imprevisto+ presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.credito + presupuesto.fdr + presupuesto.credito)*0.0789209928265611

        almacenero.pendiente_iva_ventas = iva_compras

        #Calculo el resto de las cosas

        pend_gast = almacenero.pendiente_admin + almacenero.pendiente_comision + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.imprevisto + presupuesto.credito + presupuesto.fdr - almacenero.pendiente_adelantos + almacenero.pendiente_iva_ventas + almacenero.pendiente_iibb_tem
        prest_cobrar = almacenero.prestamos_proyecto + almacenero.prestamos_otros
        total_costo = almacenero.cheques_emitidos + almacenero.gastos_fecha + pend_gast + almacenero.Prestamos_dados        
        
        
        costo_total = costo_total + total_costo

        descuento = almacenero.ingreso_ventas*0.06
        descuento_total = descuento_total + descuento
        
        total_ingresos = prest_cobrar + almacenero.cuotas_cobradas + almacenero.cuotas_a_cobrar + almacenero.ingreso_ventas
        
        ingresos_total = ingresos_total + total_ingresos

        saldo_caja = almacenero.cuotas_cobradas - almacenero.gastos_fecha - almacenero.Prestamos_dados
        saldo_proyecto = total_ingresos - total_costo
        rentabilidad = (saldo_proyecto/total_costo)*100


        total_ingresos_pesimista = total_ingresos - descuento
        saldo_proyecto_pesimista = total_ingresos_pesimista - total_costo
        rentabilidad_pesimista = (saldo_proyecto_pesimista/total_costo)*100

        try:

            modelo = Modelopresupuesto.objects.filter(proyecto = dato.proyecto)

            presupuesto = len(modelo)

        except:

            pass

        try:

            pricing = Pricing.objects.filter(unidad__proyecto = dato.proyecto)

            pricing = len(pricing)

        except:

            pass

        datos_completos.append((dato, total_costo, total_ingresos, saldo_proyecto, rentabilidad, presupuesto, pricing, saldo_proyecto_pesimista, rentabilidad_pesimista))

    beneficio_total = ingresos_total - costo_total
    beneficio_total_pesimista = beneficio_total - descuento_total
    rendimiento_total = beneficio_total/costo_total*100
    rendimiento_total_pesimista = beneficio_total_pesimista/costo_total*100

    datos_finales.append((ingresos_total, costo_total, beneficio_total, rendimiento_total, descuento_total, rendimiento_total_pesimista, beneficio_total_pesimista))


    #Esta es la parte del historico

    datos_historicos = RegistroAlmacenero.objects.order_by("fecha")

    fechas = []

    for d in datos_historicos:

        if not d.fecha in fechas:

            fechas.append(d.fecha)

    datos_registro = []

    for fecha in fechas:


        datos = RegistroAlmacenero.objects.filter(fecha = fecha)

        datos_completos_registro = []
        datos_finales_registro = []

        costo_total = 0
        ingresos_total = 0
        descuento_total = 0


        for dato in datos:

            presupuesto = "NO"

            pricing = "NO"

            almacenero = dato

            presupuesto = Presupuestos.objects.get(proyecto = dato.proyecto)

            #Aqui calculo el IVA sobre compras

            iva_compras = (presupuesto.imprevisto+ presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.credito + presupuesto.fdr + presupuesto.credito)*0.0789209928265611

            almacenero.pendiente_iva_ventas = iva_compras

            #Calculo el resto de las cosas

            pend_gast = almacenero.pendiente_admin + almacenero.pendiente_comision + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.imprevisto + presupuesto.credito + presupuesto.fdr - almacenero.pendiente_adelantos + almacenero.pendiente_iva_ventas + almacenero.pendiente_iibb_tem
            prest_cobrar = almacenero.prestamos_proyecto + almacenero.prestamos_otros
            total_costo = almacenero.cheques_emitidos + almacenero.gastos_fecha + pend_gast + almacenero.Prestamos_dados                    
            
            costo_total = costo_total + total_costo

            descuento = almacenero.ingreso_ventas*0.06
            descuento_total = descuento_total + descuento
            
            total_ingresos = prest_cobrar + almacenero.cuotas_cobradas + almacenero.cuotas_a_cobrar + almacenero.ingreso_ventas
            
            ingresos_total = ingresos_total + total_ingresos

            saldo_caja = almacenero.cuotas_cobradas - almacenero.gastos_fecha - almacenero.Prestamos_dados
            saldo_proyecto = total_ingresos - total_costo
            rentabilidad = (saldo_proyecto/total_costo)*100

            total_ingresos_pesimista = total_ingresos - descuento
            saldo_proyecto_pesimista = total_ingresos_pesimista - total_costo
            rentabilidad_pesimista = (saldo_proyecto_pesimista/total_costo)*100

            try:

                modelo = Modelopresupuesto.objects.filter(proyecto = dato.proyecto)

                presupuesto = len(modelo)

            except:

                pass

            try:

                pricing = Pricing.objects.filter(unidad__proyecto = dato.proyecto)

                pricing = len(pricing)

            except:

                pass

            datos_completos_registro.append((dato, total_costo, total_ingresos, saldo_proyecto, rentabilidad, presupuesto, pricing, saldo_proyecto_pesimista, rentabilidad_pesimista))

        beneficio_total = ingresos_total - costo_total
        beneficio_total_pesimista = beneficio_total - descuento_total
        rendimiento_total = beneficio_total/costo_total*100
        rendimiento_total_pesimista = beneficio_total_pesimista/costo_total*100

        datos_finales_registro.append((ingresos_total, costo_total, beneficio_total, rendimiento_total, descuento_total, rendimiento_total_pesimista, beneficio_total_pesimista))

        datos_registro.append((datos_completos_registro, datos_finales_registro))

    return render(request, 'consolidado.html', {"datos_completos":datos_completos, 'datos_finales':datos_finales, "datos_registro":datos_registro, "fechas":fechas})


def almacenero(request):

    datos = Almacenero.objects.all()

    proyectos = []

    for dato in datos:
        proyectos.append((dato.proyecto.id, dato.proyecto.nombre))

    proyectos = list(set(proyectos))

    usd_blue = Constantes.objects.get(nombre = "USD_BLUE")

    datos = 0

    mensaje = 0

    if request.method == 'POST':
        
        try:

            #Trae el proyecto elegido

            proyecto_elegido = request.POST.items()

            #Crea los datos del pricing

            datos = []

            for i in proyecto_elegido:

                if i[0] == "proyecto":
                    proyecto = Proyectos.objects.get(id = i[1])


                    presupuesto = Presupuestos.objects.get(proyecto = proyecto)
                    almacenero = Almacenero.objects.get(proyecto = proyecto)

                    #Aqui calculo el IVA sobre compras

                    iva_compras = (presupuesto.imprevisto+ presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.credito + presupuesto.fdr + presupuesto.credito)*0.0789209928265611

                    almacenero.pendiente_iva_ventas = iva_compras

                    almacenero.save()

                    #Calculo el resto de las cosas
                    
                    pend_gast = almacenero.pendiente_admin + almacenero.pendiente_comision + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.imprevisto + presupuesto.credito + presupuesto.fdr - almacenero.pendiente_adelantos + almacenero.pendiente_iva_ventas + almacenero.pendiente_iibb_tem
                    prest_cobrar = almacenero.prestamos_proyecto + almacenero.prestamos_otros
                    total_costo = almacenero.cheques_emitidos + almacenero.gastos_fecha + pend_gast + almacenero.Prestamos_dados
                    
                    descuento = almacenero.ingreso_ventas*0.06 
                    
                    total_ingresos = prest_cobrar + almacenero.cuotas_cobradas + almacenero.cuotas_a_cobrar + almacenero.ingreso_ventas
                    saldo_caja = almacenero.cuotas_cobradas - almacenero.gastos_fecha - almacenero.Prestamos_dados
                    saldo_proyecto = total_ingresos - total_costo
                    rentabilidad = (saldo_proyecto/total_costo)*100

                    total_ingresos_pesimista = total_ingresos - descuento
                    saldo_proyecto_pesimista = total_ingresos_pesimista - total_costo
                    rentabilidad_pesimista = (saldo_proyecto_pesimista/total_costo)*100

                    #Cargo todo a datos

                    datos.append(proyecto)
                    datos.append(presupuesto)
                    datos.append(almacenero)

                    datos.append((pend_gast, prest_cobrar, total_costo, total_ingresos, rentabilidad, saldo_caja, saldo_proyecto, descuento, saldo_proyecto_pesimista, rentabilidad_pesimista))

            proyectos = 0

        except:

            mensaje = 1

    datos = {"proyectos":proyectos,
    'datos':datos,
    "usd":usd_blue,
    "mensaje":mensaje}

    return render(request, 'almacenero.html', {"datos":datos} )

class DescargarCuentacorriente(TemplateView):

    def get(self, request, id_cuenta, *args, **kwargs):
        wb = Workbook()

        cuenta = CuentaCorriente.objects.get(id = id_cuenta)
        cuota = Cuota.objects.filter(cuenta_corriente = cuenta)
        pagos = Pago.objects.filter(cuota__cuenta_corriente = cuenta)

        cont = 1

        for c in cuota:

            if cont == 1:
                ws = wb.active
                ws.title = "Cuotas"
                ws["A"+str(cont)] = "FECHA"
                ws["B"+str(cont)] = "PRECIO"
                ws["C"+str(cont)] = "CONSTANTE"
                ws["D"+str(cont)] = "CONCEPTO"
                ws["E"+str(cont)] = "PRECIO PESOS"


                ws["A"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont)].alignment = Alignment(horizontal = "center")

                ws["A"+str(cont)].font = Font(bold = True)
                ws["B"+str(cont)].font = Font(bold = True)
                ws["C"+str(cont)].font = Font(bold = True)
                ws["D"+str(cont)].font = Font(bold = True)
                ws["E"+str(cont)].font = Font(bold = True)


                ws.column_dimensions['A'].width = 11
                ws.column_dimensions['B'].width = 9
                ws.column_dimensions['C'].width = 12
                ws.column_dimensions['D'].width = 20
                ws.column_dimensions['E'].width = 14


                ws["A"+str(cont+1)] = c.fecha
                ws["B"+str(cont+1)] = c.precio
                ws["C"+str(cont+1)] = c.constante.nombre
                ws["D"+str(cont+1)] = c.concepto
                ws["E"+str(cont+1)] = c.precio*c.constante.valor

                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].number_format = '#,##0.00_-'
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].number_format = '"$"#,##0.00_-'

                cont += 1

            else: 
                ws = wb.active
                ws["A"+str(cont+1)] = c.fecha
                ws["B"+str(cont+1)] = c.precio
                ws["C"+str(cont+1)] = c.constante.nombre
                ws["D"+str(cont+1)] = c.concepto
                ws["E"+str(cont+1)] = c.precio*c.constante.valor

                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].number_format = '#,##0.00_-'
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].number_format = '"$"#,##0.00_-'

                cont += 1
        cont = 1
        for p in pagos:

            if cont == 1:
                ws = wb.create_sheet('Pagos')
                ws["A"+str(cont)] = "CUOTA FECHA"
                ws["B"+str(cont)] = "FECHA"
                ws["C"+str(cont)] = "PAGO (MD)"
                ws["D"+str(cont)] = "MONEDA"
                ws["E"+str(cont)] = "PAGO PESOS"
                ws["F"+str(cont)] = "DOCUMENTO 1"
                ws["G"+str(cont)] = "DOCUMENTO 2"

                ws["A"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont)].alignment = Alignment(horizontal = "center")

                ws["A"+str(cont)].font = Font(bold = True)
                ws["B"+str(cont)].font = Font(bold = True)
                ws["C"+str(cont)].font = Font(bold = True)
                ws["D"+str(cont)].font = Font(bold = True)
                ws["E"+str(cont)].font = Font(bold = True)
                ws["F"+str(cont)].font = Font(bold = True)
                ws["G"+str(cont)].font = Font(bold = True)

                ws.column_dimensions['A'].width = 12
                ws.column_dimensions['B'].width = 11
                ws.column_dimensions['C'].width = 11
                ws.column_dimensions['D'].width = 12
                ws.column_dimensions['E'].width = 20
                ws.column_dimensions['F'].width = 25
                ws.column_dimensions['G'].width = 25

                ws["A"+str(cont+1)] = p.cuota.fecha
                ws["B"+str(cont+1)] = p.fecha
                ws["C"+str(cont+1)] = p.pago
                ws["D"+str(cont+1)] = p.cuota.constante.nombre
                ws["E"+str(cont+1)] = p.pago_pesos
                ws["F"+str(cont+1)] = p.documento_1
                ws["G"+str(cont+1)] = p.documento_2

                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont+1)].number_format = '#,##0.00_-'
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")

                cont += 1

            else:
                
                ws = wb["Pagos"]

                ws["A"+str(cont+1)] = p.cuota.fecha
                ws["B"+str(cont+1)] = p.fecha
                ws["C"+str(cont+1)] = p.pago
                ws["D"+str(cont+1)] = p.cuota.constante.nombre
                ws["E"+str(cont+1)] = p.pago_pesos
                ws["F"+str(cont+1)] = p.documento_1
                ws["G"+str(cont+1)] = p.documento_2

                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont+1)].number_format = '#,##0.00_-'
                ws["D"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")

                cont += 1

        #Establecer el nombre del archivo
        nombre_archivo = "Cuenta.-{0}.xls".format(str(cuenta.venta.comprador))
        
        #Definir tipo de respuesta que se va a dar
        response = HttpResponse(content_type = "application/ms-excel")
        contenido = "attachment; filename = {0}".format(nombre_archivo).replace(',', '_')
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response