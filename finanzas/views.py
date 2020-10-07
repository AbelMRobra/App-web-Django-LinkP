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

    datos_total = []

    try:

        for d in datos:

            cotizacion = d.pago_pesos/d.pago

            datos_total.append((d, cotizacion))

    except:

        datos_total = 0

    return render(request, 'pagos.html', {'datos':datos_total, 'cuota':cuota})

def editar_pagos(request, id_pago):

    pago = Pago.objects.get(id = id_pago)

    cotizacion = pago.pago_pesos/pago.pago

    if request.method == 'POST':

        datos_crear = request.POST.items()

        pagado = 0

        for i in datos_crear:

            if  'fecha' in i[0] and i[1] != "":

                pago.fecha = str(i[1])
                pago.save()

            if  'documento1' in i[0] and i[1] != "":

                pago.documento_1 = i[1]
                pago.save()

            if  'documento2' in i[0] and i[1] != "":

                pago.documento_2 = i[1]
                pago.save()

            if  'precio1' in i[0] and i[1] != "":

                cotizacion = i[1]

                precio1 = float(pagado)/float(cotizacion)
                pago.pago = precio1
                pago.save()

            if  'precio2' in i[0] and i[1] != "":

                pago.pago_pesos = i[1]
                pagado = i[1]

                pago.save()


        return redirect('Pagos', id_cuota = pago.cuota.id)

    return render(request, 'editar_pagos.html', {'pago':pago, 'cotizacion':cotizacion})

def pagos(request, id_cuota):

    cuota = Cuota.objects.get(id = id_cuota)

    datos = Pago.objects.filter(cuota = cuota)

    datos_total = []

    try:

        for d in datos:

            cotizacion = d.pago_pesos/d.pago

            datos_total.append((d, cotizacion))

    except:

        datos_total = 0

    return render(request, 'pagos.html', {'datos':datos_total, 'cuota':cuota})

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


def EliminarCuentaCorriente(request, id_cuenta):

    datos = CuentaCorriente.objects.get(id = id_cuenta)

    cuotas = len(Cuota.objects.filter(cuenta_corriente = datos))
    pagos = len(Pago.objects.filter(cuota__cuenta_corriente = datos))

    otros_datos = [cuotas, pagos]

    if request.method == 'POST':

        datos.delete()

        return redirect('Cuenta corriente proyecto', id_proyecto = datos.venta.proyecto.id)

    return render(request, 'eliminar_cuenta.html', {"datos":datos, "otros_datos":otros_datos})

### Armando resumen de cuenta corriente


def totalcuentacte(request, id_proyecto):

    proyectos = Proyectos.objects.all()

    datos_primeros = []

    listado = []

    for proyecto in proyectos:

        cuotas = Cuota.objects.filter(cuenta_corriente__venta__proyecto = proyecto)

        if len(cuotas)>0:
            datos_primeros.append(proyecto)
            
            for c in cuotas:

                listado.append(c.cuenta_corriente.venta.proyecto)

    listado = set(list(listado))

    proy = 0

    cantidad_cuentas = len(CuentaCorriente.objects.all())


    if id_proyecto != "0":

        proy = Proyectos.objects.get(id = id_proyecto)

        cantidad_cuentas = len(CuentaCorriente.objects.filter(venta__proyecto__id = id_proyecto))
    
    #Establecemos un rango para hacer el cash de ingreso
    
    fecha_inicial_hoy = datetime.date.today()

    fecha_inicial_2 = datetime.date(fecha_inicial_hoy.year, fecha_inicial_hoy.month, 1)

    fechas = []

    contador = 0
    contador_year = 1

    for f in range(26):

        if (fecha_inicial_2.month + contador) == 13:
            
            year = fecha_inicial_2.year + contador_year
            
            fecha_cargar = date(year, 1, fecha_inicial_2.day)

            fechas.append(fecha_cargar)
            
            contador_year += 1

            contador = - (12 - contador)

        else:

            mes = fecha_inicial_2.month + contador

            year = fecha_inicial_2.year + contador_year - 1

            fecha_cargar = date(year, mes, fecha_inicial_2.day)

            fechas.append(fecha_cargar)

        contador += 1

    #Aqui hacemos los totalizadores generales

    if id_proyecto != "0":

        cuotas_anteriores = Cuota.objects.filter(fecha__lt = fecha_inicial_hoy, cuenta_corriente__venta__proyecto__id = id_proyecto)
        pagos_anteriores = Pago.objects.filter(fecha__lt = fecha_inicial_hoy, cuota__cuenta_corriente__venta__proyecto__id = id_proyecto)
        cuotas_posteriores= Cuota.objects.filter(fecha__gt = fecha_inicial_hoy, cuenta_corriente__venta__proyecto__id = id_proyecto)
        pagos_posteriores = Pago.objects.filter(fecha__gt = fecha_inicial_hoy, cuota__cuenta_corriente__venta__proyecto__id = id_proyecto)


    else:

        cuotas_anteriores = Cuota.objects.filter(fecha__lt = fecha_inicial_hoy)
        pagos_anteriores = Pago.objects.filter(fecha__lt = fecha_inicial_hoy)
        cuotas_posteriores = Cuota.objects.filter(fecha__gt = fecha_inicial_hoy)

    total_original = 0
    total_cobrado = 0
    total_pendiente = 0
    total_acobrar= 0

    for cuo in cuotas_anteriores:

        total_original = total_original + cuo.precio

    for pag in pagos_anteriores:

        total_cobrado = total_cobrado +  pag.pago

    for cuot in cuotas_posteriores:

        total_acobrar= total_acobrar + cuot.precio

    total_pendiente = total_original - total_cobrado

    otros_datos = [total_cobrado, total_pendiente, total_acobrar]
    

    #Aqui buscamos agrupar proyecto - sumatorias de cuotas y pagos - mes
    
    datos_segundos = []

    total_fecha = []

    fecha_inicial = 0

    for f in fechas:

        total = 0
        total_link = 0

        datos_terceros = []

        if fecha_inicial == 0:

                fecha_inicial = fecha_inicial_hoy

        else:

            #Aqui calculamos el saldo de cuotas totales - Uso el id_proyecto para filtrar

            if id_proyecto != "0":

                cuotas = Cuota.objects.filter(fecha__range = (fecha_inicial, f), cuenta_corriente__venta__proyecto__id = id_proyecto)
                
                pagos = Pago.objects.filter(fecha__range = (fecha_inicial, f), cuota__cuenta_corriente__venta__proyecto__id = id_proyecto)


            else:

                cuotas = Cuota.objects.filter(fecha__range = (fecha_inicial, f))
                
                pagos = Pago.objects.filter(fecha__range = (fecha_inicial, f))

            total_cuotas = 0
            total_cuotas_link = 0
            total_pagado = 0
            total_pagado_link = 0
            saldo = 0
            saldo_link = 0

            if len(cuotas)>0:

                for c in cuotas:

                    total_cuotas = total_cuotas + c.precio*c.constante.valor

                    if c.cuenta_corriente.venta.unidad.asig == "HON. LINK" or c.cuenta_corriente.venta.unidad.asig == "TERRENO":

                        total_cuotas_link = total_cuotas_link + c.precio*c.constante.valor 

            if len(pagos)>0:

                for p in pagos:

                    total_pagado = total_pagado + p.pago*p.cuota.constante.valor

                    if p.cuota.cuenta_corriente.venta.unidad.asig == "HON. LINK" or p.cuota.cuenta_corriente.venta.unidad.asig == "TERRENO":

                        total_pagado_link = total_pagado_link + p.pago*p.cuota.constante.valor 

            saldo = total_cuotas-total_pagado

            total = total + saldo


            #Aqui calculamos el saldo de cuotas de LINK

            saldo_link = total_cuotas_link-total_pagado_link

            total_link = total_link + saldo_link
            
            datos_terceros.append((fecha_inicial, saldo, saldo_link))

            fecha_inicial = f

            horm = Constantes.objects.get(nombre = "Hº VIVIENDA")
            
            total_horm = total/horm.valor

            total_horm_link = total_link/horm.valor

            datos_segundos.append((datos_terceros, total, total_horm, total_link, total_horm_link))
            
    return render(request, 'totalcuentas.html', {"fechas":fechas, "datos":datos_segundos, "datos_primero":datos_primeros, "total_fechas":total_fecha, "listado":listado, "proy":proy, "cantidad_cuentas":cantidad_cuentas, "otros_datos":otros_datos})



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
        pago_pesos = 0
        saldo_cuota = 0
        pagos_realizados = []

        for pago in pagos:

            if pago.cuota == cuota:

                pago_cuota = pago_cuota + pago.pago
                pago_pesos = pago_pesos + pago.pago_pesos

                pagos_realizados.append(pago)

        saldo_cuota = cuota.precio - pago_cuota
        saldo_pesos = saldo_cuota*cuota.constante.valor

        if pago_cuota == 0:
            cotizacion = 0
        else:
            cotizacion = pago_pesos/pago_cuota

        datos_cuenta.append((cuota, pago_cuota, saldo_cuota, saldo_pesos, pagos_realizados, cotizacion))

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


def consultapagos(request):

    datos_viejo = Pago.objects.order_by("-fecha")

    datos = []

    for d in datos_viejo:

        cotizacion = 0

        if d.pago != 0:

            cotizacion = d.pago_pesos/d.pago

        datos_subir = (d, cotizacion)

        datos.append(datos_subir)

    return render(request, 'pagos_total.html', {"datos":datos})


def ingresounidades(request, estado, proyecto):

    estado_marcado = estado

    proyecto_marcado = proyecto

    listado = []

    datos_proyectos = datos = VentasRealizadas.objects.all().exclude(unidad__estado_iibb = "SI", unidad__estado_comision = "SI")

    for d in datos_proyectos:

        listado.append(d.proyecto)

    listado = set(list(listado))

    if proyecto == "0":

        if estado == "0":

            datos = VentasRealizadas.objects.all().exclude(unidad__estado_iibb = "SI", unidad__estado_comision = "SI")

        if estado == "1":

            datos = VentasRealizadas.objects.filter(unidad__estado = "SEÑADA")

        if estado == "2":

            datos = VentasRealizadas.objects.filter(unidad__estado_iibb = "NO")

        if estado == "3":

            datos = VentasRealizadas.objects.filter(unidad__estado_comision = "NO")

    else:

        if estado == "0":

            datos = VentasRealizadas.objects.filter(proyecto__id = proyecto).exclude(unidad__estado_iibb = "SI", unidad__estado_comision = "SI")

        if estado == "1":

            datos = VentasRealizadas.objects.filter(unidad__estado = "SEÑADA", proyecto__id = proyecto)

        if estado == "2":

            datos = VentasRealizadas.objects.filter(unidad__estado_iibb = "NO", proyecto__id = proyecto)

        if estado == "3":

            datos = VentasRealizadas.objects.filter(unidad__estado_comision = "NO", proyecto__id = proyecto)


    if request.method == 'POST':

        proyecto_elegido = request.POST.items()

        for i in proyecto_elegido:

            if i[0] == 'ingresar':

                unidad = Unidades.objects.get(id = i[1])

                unidad.estado = "VENDIDA"

                unidad.save()

            if i[0] == 'comision':

                unidad = Unidades.objects.get(id = i[1])

                unidad.estado_comision = "SI"

                unidad.save()

            if i[0] == 'iibb':

                unidad = Unidades.objects.get(id = i[1])

                unidad.estado_iibb = "SI"

                unidad.save()


    return render(request, 'ingresounidades.html',{'datos':datos, 'estado':estado_marcado, 'proyecto':proyecto_marcado, 'listado':listado})

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

        # Aqui calculo el IVA sobre compras

        iva_compras = (presupuesto.imprevisto + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.credito + presupuesto.fdr)*0.07875

        almacenero.pendiente_iva_ventas = iva_compras


        almacenero.save()


        # Calculo el resto de las cosas

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

        # -----------------> Aqui empieza para el precio promedio contado

        if len(Unidades.objects.filter(proyecto = dato.proyecto, estado = "DISPONIBLE")) > 0:

            datos_unidades = Unidades.objects.filter(proyecto = dato.proyecto, estado = "DISPONIBLE")

            m2_totales = 0

            sumatoria_contado = 0

            for d in datos_unidades:

                if d.sup_equiv > 0:

                    m2 = d.sup_equiv

                else:

                    m2 = d.sup_propia + d.sup_balcon + d.sup_comun + d.sup_patio
            
                try:

                    param_uni = Pricing.objects.get(unidad = d)
                    
                    desde = d.proyecto.desde

                    if d.tipo == "COCHERA":
                        desde = d.proyecto.desde*d.proyecto.descuento_cochera

                    if param_uni.frente == "SI":
                        desde = desde*d.proyecto.recargo_frente

                    if param_uni.piso_intermedio == "SI":
                        desde =desde*d.proyecto.recargo_piso_intermedio

                    if param_uni.cocina_separada == "SI":
                        desde = desde*d.proyecto.recargo_cocina_separada

                    if param_uni.local == "SI":
                        desde = desde*d.proyecto.recargo_local

                    if param_uni.menor_45_m2 == "SI":
                        desde = desde*d.proyecto.recargo_menor_45

                    if param_uni.menor_50_m2 == "SI":
                        desde = desde*d.proyecto.recargo_menor_50

                    if param_uni.otros == "SI":
                        desde = desde*d.proyecto.recargo_otros 

                    #Aqui calculamos el contado/financiado
                    
                    contado = desde*m2 

                    sumatoria_contado = sumatoria_contado + contado
                    m2_totales = m2_totales + m2

                except:

                    print("Esta unidad no tiene parametros")


            if m2_totales == 0:

                precio_promedio_contado = 0

            else:

                precio_promedio_contado = sumatoria_contado/m2_totales

        else:

            if "THAMES" in dato.proyecto.nombre:

                precio_promedio_contado = 66657.5

            elif "#300" in dato.proyecto.nombre:

                precio_promedio_contado = 95825

            else:

                precio_promedio_contado = 0

    # -----------------> Aqui termina para el precio promedio contado

        datos_completos.append((dato, total_costo, total_ingresos, saldo_proyecto, rentabilidad, presupuesto, pricing, saldo_proyecto_pesimista, rentabilidad_pesimista, precio_promedio_contado))

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

            iva_compras = (presupuesto.imprevisto + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.credito + presupuesto.fdr)*0.07875

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

                    iva_compras = (presupuesto.imprevisto + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.credito + presupuesto.fdr)*0.07875

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



class DescargarTotalCuentas(TemplateView):

    def get(self, request, *args, **kwargs):


        #color = '#%02x%02x%02x' % (0, 128, 64)
        
        wb = Workbook()
        #Establecemos una lista

        proyectos = Proyectos.objects.all()

        datos_primeros = []

        listado = []

        for proyecto in proyectos:

            cuotas = Cuota.objects.filter(cuenta_corriente__venta__proyecto = proyecto)

            if len(cuotas)>0:
                datos_primeros.append(proyecto)
                
                for c in cuotas:

                    listado.append(c.cuenta_corriente.venta.proyecto)

        listado = set(list(listado))


        #En la primera vuelta sacamos el totalizado

        proy = 0

        cantidad_cuentas = len(CuentaCorriente.objects.all())
        
        #Establecemos un rango para hacer el cash de ingreso
        
        fecha_inicial_hoy = datetime.date.today()

        fecha_inicial_2 = datetime.date(fecha_inicial_hoy.year, fecha_inicial_hoy.month, 1)

        fechas = []

        #Aqui buscamos la ultima fecha

        fecha_ultima = Cuota.objects.order_by("-fecha")

        contador = 0
        
        contador_year = 1

        fecha_cargar = fecha_inicial_2

        while fecha_cargar < fecha_ultima[0].fecha:

            if (fecha_inicial_2.month + contador) == 13:
                
                year = fecha_inicial_2.year + contador_year
                
                fecha_cargar = date(year, 1, fecha_inicial_2.day)

                fechas.append(fecha_cargar)
                
                contador_year += 1

                contador = - (12 - contador)

            else:

                mes = fecha_inicial_2.month + contador

                year = fecha_inicial_2.year + contador_year - 1

                fecha_cargar = date(year, mes, fecha_inicial_2.day)

                fechas.append(fecha_cargar)

            contador += 1

        #Aqui hacemos los totalizadores generales

        cuotas_anteriores = Cuota.objects.filter(fecha__lt = fecha_inicial_hoy)
        pagos_anteriores = Pago.objects.filter(fecha__lt = fecha_inicial_hoy)
        cuotas_posteriores = Cuota.objects.filter(fecha__gt = fecha_inicial_hoy)

        total_original = 0
        total_cobrado = 0
        total_pendiente = 0
        total_acobrar= 0

        for cuo in cuotas_anteriores:

            total_original = total_original + cuo.precio

        for pag in pagos_anteriores:

            total_cobrado = total_cobrado +  pag.pago

        for cuot in cuotas_posteriores:

            total_acobrar= total_acobrar + cuot.precio

        total_pendiente = total_original - total_cobrado

        otros_datos = [total_cobrado, total_pendiente, total_acobrar]



    
        #Aqui buscamos agrupar proyecto - sumatorias de cuotas y pagos - mes
        
        datos_segundos = []

        total_fecha = []

        fecha_inicial = 0

        for f in fechas:

            total = 0
            total_link = 0

            datos_terceros = []

            if fecha_inicial == 0:

                    fecha_inicial = fecha_inicial_hoy

            else:

                cuotas = Cuota.objects.filter(fecha__range = (fecha_inicial, f))
                    
                pagos = Pago.objects.filter(fecha__range = (fecha_inicial, f))

                total_cuotas = 0
                total_cuotas_link = 0
                total_pagado = 0
                total_pagado_link = 0
                saldo = 0
                saldo_link = 0

                if len(cuotas)>0:

                    for c in cuotas:

                        total_cuotas = total_cuotas + c.precio*c.constante.valor

                        if c.cuenta_corriente.venta.unidad.asig == "HON. LINK" or c.cuenta_corriente.venta.unidad.asig == "TERRENO":

                            total_cuotas_link = total_cuotas_link + c.precio*c.constante.valor 

                if len(pagos)>0:

                    for p in pagos:

                        total_pagado = total_pagado + p.pago*p.cuota.constante.valor

                        if p.cuota.cuenta_corriente.venta.unidad.asig == "HON. LINK" or p.cuota.cuenta_corriente.venta.unidad.asig == "TERRENO":

                            total_pagado_link = total_pagado_link + p.pago*p.cuota.constante.valor 

                saldo = total_cuotas-total_pagado

                total = total + saldo

                #Aqui calculamos el saldo de cuotas de LINK

                saldo_link = total_cuotas_link-total_pagado_link

                total_link = total_link + saldo_link
                
                datos_terceros.append((fecha_inicial, saldo, saldo_link))

                fecha_inicial = f

                horm = Constantes.objects.get(nombre = "Hº VIVIENDA")
                
                total_horm = total/horm.valor

                total_horm_link = total_link/horm.valor

                datos_segundos.append((datos_terceros, total, total_horm, total_link, total_horm_link))


        #Aqui termina la primera vuelta -> Total por proyecto

        cont = 10

        ws = wb.active
        ws.title = "Cuotas"
        ws["A"+str(2)] = "RESUMEN MES A MES DE INGRESOS POR CUOTAS A COBRAR"
        ws["A"+str(5)] = "CUENTAS"
        ws["A"+str(6)] = "COBRADO"
        ws["A"+str(7)] = "ADEUDADO"
        ws["A"+str(8)] = "PENDIENTE"

        ws["A"+str(2)].font = Font(bold = True)
        ws["A"+str(5)].font = Font(bold = True, color= "FDFFFF")
        ws["A"+str(5)].fill =  PatternFill("solid", fgColor= "33353B")
        ws["A"+str(6)].font = Font(bold = True, color= "FDFFFF")
        ws["A"+str(6)].fill =  PatternFill("solid", fgColor= "33353B")
        ws["A"+str(7)].font = Font(bold = True, color= "FDFFFF")
        ws["A"+str(7)].fill =  PatternFill("solid", fgColor= "33353B")
        ws["A"+str(8)].font = Font(bold = True, color= "FDFFFF")
        ws["A"+str(8)].fill =  PatternFill("solid", fgColor= "33353B")


        ws["B"+str(5)] = cantidad_cuentas
        ws["B"+str(6)] = otros_datos[0]
        ws["B"+str(7)] = otros_datos[1]
        ws["B"+str(8)] = otros_datos[2]

        ws["B"+str(6)].number_format = '#,##0.00_-"M3"'
        ws["B"+str(7)].number_format = '#,##0.00_-"M3"'
        ws["B"+str(8)].number_format = '#,##0.00_-"M3"'

        for dato in datos_segundos:

            if cont == 10:
                ws = wb.active
                ws["A"+str(cont)] = "FECHA"
                ws["B"+str(cont)] = "TOTAL $"
                ws["C"+str(cont)] = "TOTAL Hº"
                ws["D"+str(cont)] = "TOTAL LINK $"
                ws["E"+str(cont)] = "TOTAL LINK Hª"


                ws["A"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont)].alignment = Alignment(horizontal = "center")

                ws["A"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["B"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["C"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["D"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["E"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["A"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                ws["B"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                ws["C"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                ws["D"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                ws["E"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")


                ws.column_dimensions['A'].width = 15
                ws.column_dimensions['B'].width = 15
                ws.column_dimensions['C'].width = 15
                ws.column_dimensions['D'].width = 15
                ws.column_dimensions['E'].width = 15


                ws["A"+str(cont+1)] = dato[0][0][0]
                ws["B"+str(cont+1)] = dato[1]
                ws["C"+str(cont+1)] = dato[2]
                ws["D"+str(cont+1)] = dato[3]
                ws["E"+str(cont+1)] = dato[4]

                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["C"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                ws["E"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                ws["D"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")


                cont += 1

            else: 

                ws = wb.active
                ws["A"+str(cont+1)] = dato[0][0][0]
                ws["B"+str(cont+1)] = dato[1]
                ws["C"+str(cont+1)] = dato[2]
                ws["D"+str(cont+1)] = dato[3]
                ws["E"+str(cont+1)] = dato[4]

                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["C"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                ws["E"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                ws["D"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")

                cont += 1
        cont = 1


        for proyect in listado:

            #En la primera vuelta sacamos el totalizado

            cantidad_cuentas = len(CuentaCorriente.objects.filter(venta__proyecto = proyect))
            
            #Establecemos un rango para hacer el cash de ingreso
            
            fecha_inicial_hoy = datetime.date.today()

            fecha_inicial_2 = datetime.date(fecha_inicial_hoy.year, fecha_inicial_hoy.month, 1)

            fechas = []

            #Aqui buscamos la ultima fecha

            fecha_ultima = Cuota.objects.filter(cuenta_corriente__venta__proyecto = proyect).order_by("-fecha")

            contador = 0
            
            contador_year = 1

            fecha_cargar = fecha_inicial_2

            while fecha_cargar < fecha_ultima[0].fecha:

                if (fecha_inicial_2.month + contador) == 13:
                    
                    year = fecha_inicial_2.year + contador_year
                    
                    fecha_cargar = date(year, 1, fecha_inicial_2.day)

                    fechas.append(fecha_cargar)
                    
                    contador_year += 1

                    contador = - (12 - contador)

                else:

                    mes = fecha_inicial_2.month + contador

                    year = fecha_inicial_2.year + contador_year - 1

                    fecha_cargar = date(year, mes, fecha_inicial_2.day)

                    fechas.append(fecha_cargar)

                contador += 1

            #Aqui hacemos los totalizadores generales

            cuotas_anteriores = Cuota.objects.filter(fecha__lt = fecha_inicial_hoy, cuenta_corriente__venta__proyecto = proyect)
            pagos_anteriores = Pago.objects.filter(fecha__lt = fecha_inicial_hoy, cuota__cuenta_corriente__venta__proyecto = proyect)
            cuotas_posteriores = Cuota.objects.filter(fecha__gt = fecha_inicial_hoy, cuenta_corriente__venta__proyecto = proyect)

            total_original = 0
            total_cobrado = 0
            total_pendiente = 0
            total_acobrar= 0

            for cuo in cuotas_anteriores:

                total_original = total_original + cuo.precio

            for pag in pagos_anteriores:

                total_cobrado = total_cobrado +  pag.pago

            for cuot in cuotas_posteriores:

                total_acobrar= total_acobrar + cuot.precio

            total_pendiente = total_original - total_cobrado

            otros_datos = [total_cobrado, total_pendiente, total_acobrar]
        
            #Aqui buscamos agrupar proyecto - sumatorias de cuotas y pagos - mes
            
            datos_segundos = []

            total_fecha = []

            fecha_inicial = 0

            for f in fechas:

                total = 0
                total_link = 0

                datos_terceros = []

                if fecha_inicial == 0:

                        fecha_inicial = fecha_inicial_hoy

                else:

                    cuotas = Cuota.objects.filter(fecha__range = (fecha_inicial, f), cuenta_corriente__venta__proyecto = proyect)
                        
                    pagos = Pago.objects.filter(fecha__range = (fecha_inicial, f), cuota__cuenta_corriente__venta__proyecto = proyect)

                    total_cuotas = 0
                    total_cuotas_link = 0
                    total_pagado = 0
                    total_pagado_link = 0
                    saldo = 0
                    saldo_link = 0

                    if len(cuotas)>0:

                        for c in cuotas:

                            total_cuotas = total_cuotas + c.precio*c.constante.valor

                            if c.cuenta_corriente.venta.unidad.asig == "HON. LINK" or c.cuenta_corriente.venta.unidad.asig == "TERRENO":

                                total_cuotas_link = total_cuotas_link + c.precio*c.constante.valor 

                    if len(pagos)>0:

                        for p in pagos:

                            total_pagado = total_pagado + p.pago*p.cuota.constante.valor

                            if p.cuota.cuenta_corriente.venta.unidad.asig == "HON. LINK" or p.cuota.cuenta_corriente.venta.unidad.asig == "TERRENO":

                                total_pagado_link = total_pagado_link + p.pago*p.cuota.constante.valor 

                    saldo = total_cuotas-total_pagado

                    total = total + saldo

                    #Aqui calculamos el saldo de cuotas de LINK

                    saldo_link = total_cuotas_link-total_pagado_link

                    total_link = total_link + saldo_link
                    
                    datos_terceros.append((fecha_inicial, saldo, saldo_link))

                    fecha_inicial = f

                    horm = Constantes.objects.get(nombre = "Hº VIVIENDA")
                    
                    total_horm = total/horm.valor

                    total_horm_link = total_link/horm.valor

                    datos_segundos.append((datos_terceros, total, total_horm, total_link, total_horm_link))


            #Aqui termina la primera vuelta -> Total por proyecto

            cont = 10

            ws = wb.create_sheet("My sheet")
            ws.title = "{0}".format(proyect.nombre)
            ws["A"+str(2)] = "RESUMEN MES A MES DE INGRESOS POR CUOTAS A COBRAR"
            ws["A"+str(5)] = "CUENTAS"
            ws["A"+str(6)] = "COBRADO"
            ws["A"+str(7)] = "ADEUDADO"
            ws["A"+str(8)] = "PENDIENTE"

            ws["A"+str(2)].font = Font(bold = True)
            ws["A"+str(5)].font = Font(bold = True, color= "FDFFFF")
            ws["A"+str(5)].fill =  PatternFill("solid", fgColor= "33353B")
            ws["A"+str(6)].font = Font(bold = True, color= "FDFFFF")
            ws["A"+str(6)].fill =  PatternFill("solid", fgColor= "33353B")
            ws["A"+str(7)].font = Font(bold = True, color= "FDFFFF")
            ws["A"+str(7)].fill =  PatternFill("solid", fgColor= "33353B")
            ws["A"+str(8)].font = Font(bold = True, color= "FDFFFF")
            ws["A"+str(8)].fill =  PatternFill("solid", fgColor= "33353B")


            ws["B"+str(5)] = cantidad_cuentas
            ws["B"+str(6)] = otros_datos[0]
            ws["B"+str(7)] = otros_datos[1]
            ws["B"+str(8)] = otros_datos[2]

            ws["B"+str(6)].number_format = '#,##0.00_-"M3"'
            ws["B"+str(7)].number_format = '#,##0.00_-"M3"'
            ws["B"+str(8)].number_format = '#,##0.00_-"M3"'

            for dato in datos_segundos:

                if cont == 10:
                    ws = wb["{0}".format(proyect.nombre)]
                    ws["A"+str(cont)] = "FECHA"
                    ws["B"+str(cont)] = "TOTAL $"
                    ws["C"+str(cont)] = "TOTAL Hº"
                    ws["D"+str(cont)] = "TOTAL LINK $"
                    ws["E"+str(cont)] = "TOTAL LINK Hª"


                    ws["A"+str(cont)].alignment = Alignment(horizontal = "center")
                    ws["B"+str(cont)].alignment = Alignment(horizontal = "center")
                    ws["C"+str(cont)].alignment = Alignment(horizontal = "center")
                    ws["D"+str(cont)].alignment = Alignment(horizontal = "center")
                    ws["E"+str(cont)].alignment = Alignment(horizontal = "center")

                    ws["A"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                    ws["B"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                    ws["C"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                    ws["D"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                    ws["E"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                    ws["A"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                    ws["B"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                    ws["C"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                    ws["D"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")
                    ws["E"+str(cont)].fill =  PatternFill("solid", fgColor= "33353B")


                    ws.column_dimensions['A'].width = 15
                    ws.column_dimensions['B'].width = 15
                    ws.column_dimensions['C'].width = 15
                    ws.column_dimensions['D'].width = 15
                    ws.column_dimensions['E'].width = 15


                    ws["A"+str(cont+1)] = dato[0][0][0]
                    ws["B"+str(cont+1)] = dato[1]
                    ws["C"+str(cont+1)] = dato[2]
                    ws["D"+str(cont+1)] = dato[3]
                    ws["E"+str(cont+1)] = dato[4]

                    ws["A"+str(cont+1)].font = Font(bold = True)
                    ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                    ws["B"+str(cont+1)].number_format = '"$"#,##0.00_-'
                    ws["C"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                    ws["E"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                    ws["D"+str(cont+1)].number_format = '"$"#,##0.00_-'
                    ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                    ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")


                    cont += 1

                else: 

                    ws = wb["{0}".format(proyect.nombre)]
                    ws["A"+str(cont+1)] = dato[0][0][0]
                    ws["B"+str(cont+1)] = dato[1]
                    ws["C"+str(cont+1)] = dato[2]
                    ws["D"+str(cont+1)] = dato[3]
                    ws["E"+str(cont+1)] = dato[4]

                    ws["A"+str(cont+1)].font = Font(bold = True)
                    ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                    ws["B"+str(cont+1)].number_format = '"$"#,##0.00_-'
                    ws["C"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                    ws["E"+str(cont+1)].number_format = '#,##0.00_-"M3"'
                    ws["D"+str(cont+1)].number_format = '"$"#,##0.00_-'
                    ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                    ws["E"+str(cont+1)].alignment = Alignment(horizontal = "center")

                    cont += 1
            cont = 1

        #Establecer el nombre del archivo
        nombre_archivo = "ResumenCuentaCorriente.xls"
        
        #Definir tipo de respuesta que se va a dar
        response = HttpResponse(content_type = "application/ms-excel")
        contenido = "attachment; filename = {0}".format(nombre_archivo).replace(',', '_')
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response