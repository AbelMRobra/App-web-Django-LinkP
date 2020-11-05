from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from finanzas.models import Almacenero, RegistroAlmacenero
from presupuestos.models import Presupuestos
from proyectos.models import Proyectos, Unidades
from ventas.models import VentasRealizadas
from compras.models import Compras, Comparativas
from registro.models import RegistroValorProyecto
from rrhh.models import datosusuario, mensajesgenerales
import datetime
from datetime import date

def guia(request):

    datos = 0

    otros_datos = 0

    try:
        datos = datosusuario.objects.get(identificacion = request.user)

        if datos:

            otros_datos = datosusuario.objects.order_by("area")


    except:

        datos = 0


    return render(request, "users/guia.html", {"datos":datos, "otros_datos":otros_datos})


def dashboard(request):


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

        total_unidades = Unidades.objects.filter(proyecto = p)

        unidades_vendidas = Unidades.objects.filter(proyecto = p).exclude(estado = "DISPONIBLE")

        if len(total_unidades) != 0:

            avance = (len(unidades_vendidas)/len(total_unidades))*100

            ventas_barras.append((p, int(avance)))

    ventas_barras = sorted(ventas_barras, reverse=True, key=lambda tup: tup[1])

    date = datetime.date.today()

    fecha_inicio = datetime.date(date.year, date.month, 1)

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

    deptos_disp = len(Unidades.objects.filter(estado = "DISPONIBLE", tipo = "DEPARTAMENTO"))
    cocheras_disp = len(Unidades.objects.filter(estado = "DISPONIBLE", tipo = "COCHERA"))

    datos_unidades = [deptos_disp, cocheras_disp]


    return render(request, "users/dashboard.html", {"datos_barras":barras, "ventas_barras":ventas_barras, "ventas":ventas_realizadas, "datos_compras":datos_compras, "datos_unidades":datos_unidades})

def inicio(request):

    # Esta parte es para Pablo

    compras_espera = Comparativas.objects.filter(estado = "ESPERA")
    compras_adjunto_ok = Comparativas.objects.filter(estado = "ADJUNTO ✓")
    mensajesdeldia = mensajesgenerales.objects.all()
    
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
                fdr = presupuesto.fdr 

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

    return render(request, "users/inicio.html", {"datos_barras":barras, "datos_logo":datos_logo, "datos_pl":datos_pl, "mensajesdeldia":mensajesdeldia})

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