from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from finanzas.models import Almacenero, RegistroAlmacenero, Arqueo, RetirodeSocios, Honorarios
from presupuestos.models import Presupuestos
from proyectos.models import Proyectos, Unidades
from ventas.models import VentasRealizadas
from compras.models import Compras, Comparativas
from registro.models import RegistroValorProyecto
from rrhh.models import datosusuario, mensajesgenerales, NotaDePedido
import datetime
from datetime import date
import pandas as pd
import numpy as np

def guia(request):

    datos = 0

    otros_datos = 0

    try:
        datos = datosusuario.objects.get(identificacion = request.user)

        if datos:

            otros_datos = datosusuario.objects.order_by("area").exclude(estado = "NO ACTIVO")

    except:

        datos = 0

    return render(request, "users/guia.html", {"datos":datos, "otros_datos":otros_datos})


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

    # Esta parte es para Pablo

    compras_espera = Comparativas.objects.filter(estado = "ESPERA")
    compras_adjunto_ok = Comparativas.objects.filter(estado = "ADJUNTO ✓")
    mensajesdeldia = mensajesgenerales.objects.all()

    # -----> Aqui para decirte si tenes pendiente firmar

    usuario = request.user.username

    datos_mensajeria = len(NotaDePedido.objects.filter(copia__contains = str(usuario)).exclude(visto__contains = str(usuario))) + len(NotaDePedido.objects.filter(destinatario__contains = str(usuario)).exclude(visto__contains = str(usuario)))
    
    datos_pl = []

    if len(compras_espera) > 0 or len(compras_adjunto_ok) > 0:

        
        datos_pl.append((len(compras_espera), len(compras_adjunto_ok)))
       
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

            )

            b.save()

    Registro_presupuestos = RegistroValorProyecto.objects.filter(fecha =date)

    if len(Registro_presupuestos) == 0:

        presupuestos = Presupuestos.objects.all()

        for p in presupuestos:

            b = RegistroValorProyecto(

                proyecto = p.proyecto,
                fecha = date,
                precio_proyecto = p.valor,

            )

            b.save()


    barras = []

    datos_barras = Presupuestos.objects.order_by("-saldo")

    for db in datos_barras:

        if db.valor != 0:

            avance = (100 - db.saldo/db.valor*100)

            barras.append((db, int(avance)))

    barras = sorted(barras,reverse=True, key=lambda tup: tup[1])

    return render(request, "users/inicio.html", {"datos_barras":barras, "datos_logo":datos_logo, "datos_pl":datos_pl, "mensajesdeldia":mensajesdeldia, "datos_mensajeria":datos_mensajeria})

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
                return redirect('/')

        else:

            return render(request, "users/logine.html", {'form': form}) 

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')