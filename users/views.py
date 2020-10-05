from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from finanzas.models import Almacenero, RegistroAlmacenero
from presupuestos.models import Presupuestos
from registro.models import RegistroValorProyecto
import datetime
from datetime import date

def guia(request):

    return render(request, "users/guia.html")


def dashboard(request):

    barras = []

    datos_barras = Presupuestos.objects.order_by("-saldo")

    for db in datos_barras:

        if db.valor != 0:

            avance = (100 - db.saldo/db.valor*100)

            barras.append((db, int(avance)))

    barras = sorted(barras,reverse=True, key=lambda tup: tup[1])

    return render(request, "users/dashboard.html", {"datos_barras":barras})

def inicio(request):

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

    return render(request, "users/inicio.html", {"datos_barras":barras})

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