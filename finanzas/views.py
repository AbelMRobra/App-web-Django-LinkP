from django.shortcuts import render
from django.shortcuts import redirect
from presupuestos.models import Proyectos, Presupuestos, Constantes, Modelopresupuesto
from .models import Almacenero, CuentaCorriente, Cuota, Pago, RegistroAlmacenero
from proyectos.models import Unidades
from ventas.models import Pricing, VentasRealizadas
import datetime
from datetime import date


# Create your views here.

def crearcuenta(request):

    datos = VentasRealizadas.objects.all()

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

            if  'tipo_venta' in i[0]:

                if i[1] == "HORM":
                    constante = Constantes.objects.get(nombre = "Hº VIVIENDA"),

                if i[1] == "USD":
                    constante = Constantes.objects.get(nombre = "USD"),

                precio_pesos = float(precio)/constante[0].valor

                for i in range(int(cuotas)):

                    c = Cuota(

                        cuenta_corriente = b,
                        fecha = fecha,
                        precio = float(precio),
                        constante = constante[0],
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


    return render(request, 'crearcuenta.html', {"datos":datos})


def ctacteproyecto(request, id_proyecto):


    proyecto = Proyectos.objects.get(id = id_proyecto)

    datos = CuentaCorriente.objects.filter(venta__proyecto = proyecto)

    return render(request, 'ctacteproyecto.html', {"proyecto":proyecto, "datos":datos})

    ### Armando resumen de cuenta corriente

def resumenctacte(request, id_cliente):

    ctacte = CuentaCorriente.objects.get(id = id_cliente)

    cuotas = Cuota.objects.filter(cuenta_corriente = ctacte)

    nombre_conceptos = []

    datos = []

    for cuota in cuotas:

        nombre_conceptos.append(cuota.concepto)

    nombre_conceptos = set(nombre_conceptos)

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


    print(datos)

    return render(request, 'resumencta.html', {"ctacte":ctacte, "datos":datos})

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