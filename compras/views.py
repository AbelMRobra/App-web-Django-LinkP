import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Proveedores, Certificados
from .models import StockComprasAnticipadas, Compras, Proyectos, Proveedores, Retiros, Comparativas
from .form import StockAntForm
from .filters import CertificadoFilter
from presupuestos.models import Articulos, Constantes
import sqlite3
import operator
import datetime
import dateutil.parser
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt 


#Función para calcular el stock


def funcionstock():

    compras = Compras.objects.filter(tipo = "ANT")
    retiros = Retiros.objects.all()   

    for i in compras:

        for c in retiros:

            if i.nombre == c.compra.nombre:

                if i.articulo == c.articulo:

                    i.cantidad = i.cantidad - c.cantidad
    stock = []
    
    for i in compras:

        if not i.cantidad == 0:
            
            stock.append(i)
    
    return stock

# ----------------------------------------------------- VISTAS PARA RETIROS ---------------------------------------------- 

def listaretiros(request):

    datos = Retiros.objects.all()

    return render(request, 'retirolist.html', {"datos":datos})



# ----------------------------------------------------- VISTAS PARA VER COMPRAS DISPONIBLES----------------------------------------------

def comprasdisponibles(request):

    if request.method == "POST":

        datos = request.POST.items()

        for i in datos:
        
            print(i)

            if i[0] == "compra":

                compra_c = i

                if i[1] != "":

                    stock = funcionstock()

                    compra = []

                    for c in stock:

                        if c.nombre == i[1]:
                            
                            compra.append(c)
                    
                    return render(request, 'retiros.html', {"compra":compra})
            
            elif i[0] == "documento":

                print(compra_c)
                print(documento_c)


    lista = []

    compras = Compras.objects.all()

    for i in compras:

        if i.tipo == "ANT":

            lista.append((i.nombre, i.proyecto, i.proveedor, i.documento))
   
    datos = list(set(lista))

    return render(request, 'retiros.html', {"datos":datos})


# ----------------------------------------------------- VISTAS PARA INGRESAR COMPRAS ----------------------------------------------

def cargacompras(request):

    proyectos = Proyectos.objects.all()
    proveedores = Proveedores.objects.all()
    compras = Compras.objects.all()
    articulos = Articulos.objects.all()

    mensaje = ""

    datos = {'proyectos': proyectos, 'proveedores':proveedores, 'compras':compras, 'articulos':articulos, 'mensaje':mensaje}

    if request.method == 'POST':

        datos_p = request.POST.items()

        resto = []

        for i in datos_p:

            if i[0] == "proyecto":
                
                proyecto = i[1]

            elif i[0] == "proveedores":
                
                proveedor = i[1]

            elif i[0] == "tipo":

                if i[1] == "1":

                    tipo = "ANT"
                
                else:

                    tipo = "NORMAL"

            elif i[0] == "nombre":
                
                nombre = i[1]

            elif i[0] == "doc":
                
                doc = i[1]
            
            else:

                resto.append(i)

        valor = 1


        for i in resto:

            try:

                if i[0] == "csrfmiddlewaretoken":

                    print("Basura")


                elif valor == 1:

                    valor = 2
    
                    articulo = i[1]

                elif valor == 2:

                    valor = 3

                    cantidad = i[1]
                
                elif valor == 3:

                    valor = 1

                    precio = i[1]

                    prueba = Articulos.objects.get(nombre=articulo)
                    print(prueba)

                    b = Compras(
                        proyecto = Proyectos.objects.get(id=proyecto),
                        proveedor = Proveedores.objects.get(id=proveedor),
                        nombre = nombre,
                        tipo = tipo,
                        documento = doc,
                        articulo = Articulos.objects.get(nombre=articulo),
                        cantidad = cantidad,
                        precio = precio,
                    )

                    b.save()
           
            except:

                mensaje = "**Los datos ingresados no son correctos"

                datos = {'proyectos': proyectos, 'proveedores':proveedores, 'compras':compras, 'articulos':articulos, 'mensaje':mensaje}
        return redirect('Compras')
    else:

        datos = {'proyectos': proyectos, 'proveedores':proveedores, 'compras':compras, 'articulos':articulos, 'mensaje':mensaje}


    return render(request, 'cargacompras.html', {'datos':datos})

# ----------------------------------------------------- VISTAS PARA LISTAR COMPRAS ----------------------------------------------


def comparativas(request):
    datos  = Comparativas.objects.order_by("-fecha_c")

    if request.method == 'POST':

        datos_post = request.POST.items()

        for d in datos_post:


            if d[0] == 'APROBADA':
                id_selec = d[1]

                comparativa = Comparativas.objects.get(id = id_selec)

                comparativa.estado = "AUTORIZADA"

                comparativa.save()

            if d[0] == 'NO APROBADA':
                id_selec = d[1]

                comparativa = Comparativas.objects.get(id = id_selec)

                comparativa.estado = "NO AUTORIZADA"

                comparativa.save()

    return render(request, 'comparativas.html', {'datos':datos})


def compras(request):

    datos = Compras.objects.order_by("-fecha_c")

    #Aqui empieza el filtro

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

                buscar = (str(i.proyecto)+str(i.proveedor)+str(i.articulo)+str(i.cantidad)+str(i.fecha_c)+str(i.documento))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)

    compras = []

    for dato in datos:
        if dato.precio_presup > dato.precio:
            total = dato.cantidad*dato.precio
            v = (1 - (dato.precio/dato.precio_presup))*100 
            compras.append((0,dato, total, -v ))

        elif dato.precio_presup == dato.precio:
            total = dato.cantidad*dato.precio
            compras.append((1,dato, total, 0))

        else:
            total = dato.cantidad*dato.precio
            v = ((dato.precio/dato.precio_presup) - 1)*100
            compras.append((2,dato, total, v))


    return render(request, 'compras.html', {'compras':compras})

# ----------------------------------------------------- VISTAS PARA CERTIFICADOS ----------------------------------------------
 
def certificados(request):

    datos = Certificados.objects.all()

    myfilter = CertificadoFilter(request.GET, queryset=datos)

    datos = myfilter.qs

    datos_enviados = {'datos':datos, 'myfilter':myfilter}

    return render(request, 'certificados.html', datos_enviados )



# ----------------------------------------------------- VISTAS PARA PROVEEDORES ---------------------------------------------- 

def proveedores(request):

    datos = Proveedores.objects.all()

    #Aqui empieza el filtro

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

                print(palabra)

                buscar = (str(i.name)+str(i.descrip)+str(i.phone)+str(i.update))

                if palabra.lower() in buscar.lower():

                    datos.append(i)

    return render(request, 'proveedores.html', {'datos':datos})

# ----------------------------------------------------- VISTAS STOCK ----------------------------------------------
 
def stockproveedores(request):

    compras = Compras.objects.filter(tipo = "ANT")
    retiros = Retiros.objects.all()   

    for i in compras:

        for c in retiros:

            if i.nombre == c.compra.nombre:

                if i.articulo == c.articulo:

                    i.cantidad = i.cantidad - c.cantidad
    datos = []
    
    for i in compras:

        if not i.cantidad == 0:
            
            datos.append(i)

    #Aqui empieza el filtro

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

                buscar = (str(i.proyecto)+str(i.proveedor)+str(i.articulo)+str(i.cantidad))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)


    #Aqui termina el filtro

    return render(request, 'stockprov.html', {'datos':datos})

# ----------------------------------------------------- VISTAS PARA ANALISIS DE COMPRA ----------------------------------------------
 
def analisiscompras(request):

    #Traemos los datos de las compras

    datos = Compras.objects.filter(documento__startswith="O")
    proyectos = Proyectos.objects.all()

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        for i in palabra_buscar:
            if i[0] != "csrfmiddlewaretoken":
                pro = i[1]
        datos = Compras.objects.filter(documento__startswith="O", proyecto = pro)

    #Establecemos el periodo de tiempo

    inicio_fecha = date.today() - datetime.timedelta(days = 365)

    fechas = []

    contador = 0

    for fecha in range(15):
        fecha_agregar = inicio_fecha + datetime.timedelta(days = ((365*contador/12)))
        fechas.append(fecha_agregar)
        contador +=1 


    fechas_compras = []

    monto_compras = 0
    monto_presupuesto = 0

    contador = 0

    for dato in range(14):

        volumen_comprado = 0
        volumen_presupuesto = 0
        rendimiento = 100

        for compra in datos:

            date_object = datetime.datetime.strptime(str(compra.fecha_c), '%Y-%m-%d')
            date_object = dateutil.parser.parse(str(date_object)).date()

            if date_object >= fechas[contador] and date_object < fechas[contador +1]:
                volumen_comprado = volumen_comprado + (compra.cantidad*compra.precio)/1000000
                monto_compras = monto_compras + (compra.cantidad*compra.precio)/1000000

                if compra.precio_presup != None:
                    volumen_presupuesto = volumen_presupuesto + (compra.cantidad*compra.precio_presup)/1000000
                    monto_presupuesto = monto_presupuesto + (compra.cantidad*compra.precio_presup)/1000000
        
        
        if volumen_presupuesto != 0:
            rendimiento = (volumen_comprado/volumen_presupuesto)*100

        fechas_compras.append((fechas[contador], volumen_comprado, volumen_presupuesto, rendimiento))
        contador += 1

    inc_total = (monto_compras/monto_presupuesto)*100

    datos = {"datos":fechas_compras,
    "montocompras":monto_compras,
    "inc":inc_total,
    "proyectos":proyectos}

    return render(request, 'analisiscompras.html', {"datos":datos} )

# ----------------------------------------------------- VISTAS PARA INFORME ----------------------------------------------
 
def informe(request):

    # --> Modelos necesarios

    compras = Compras.objects.all()
    compras_ant = Compras.objects.filter(tipo = "ANT")
    retiros = Retiros.objects.all() 
    constantes = Constantes.objects.get(nombre="USD")  
    proveedores = Proveedores.objects.all()


    # --> Metodo para calcular la cantidad de compras

    lista_compras = []

    for i in compras:

        lista_compras.append(i.nombre)

    lista_compras = len(list(set(lista_compras)))
    
    compras_nominal = 0
    
    
    # --> Metodo para calcular el valor nominal de las compras
    
    for i in compras:
        
        compras_nominal = compras_nominal + (i.precio*i.cantidad)/1000000

    # --> Metodo para calcular el valor actual de las compras

    compras_actualizado = 0
    
    for i in compras:

        articulo = Articulos.objects.get(codigo = i.articulo.codigo) 
        
        compras_actualizado = compras_actualizado + (articulo.valor*i.cantidad)/1000000
        

    # --> Metodo para calcular el stock

    stock = compras_ant

    for i in stock:

        for c in retiros:

            if i.nombre == c.compra.nombre:

                if i.articulo == c.articulo:

                    i.cantidad = i.cantidad - c.cantidad

    stock_valorizado = 0
    
    # --> Metodo para valorizar el stock

    stock_pesos = 0
    stock_horm = 0
    stock_usd = 0

    for i in stock:

        valor = i.articulo.valor
        cantidad = i.cantidad

        valor_act = valor*cantidad

        if "USD" in str(i.articulo.constante):
            stock_usd = stock_usd + valor_act

        elif "HORMIG" in str(i.articulo.nombre):
            stock_horm = stock_horm + valor_act
        else:
            stock_pesos = stock_pesos + valor_act
        
        stock_valorizado = stock_valorizado + valor_act
        stock_valorizado_m = stock_valorizado/1000000

    stock_pesos = (stock_pesos/1000000)/stock_valorizado_m*100
    stock_horm = (stock_horm/1000000)/stock_valorizado_m*100
    stock_usd = (stock_usd/1000000)/stock_valorizado_m*100

    # --> Metodo para valorizar en USD el stock

    usd = Constantes.objects.get(nombre="USD")

    stock_valorizado_usd = stock_valorizado/usd.valor
    stock_valorizado_usd_m = stock_valorizado_usd/1000000


    # --> Modelo para armar la lista de proveedores/activo
    

    lista = proveedores

    for i in lista:

        i.phone = 0

        for c in stock:

            if i == c.proveedor:

                i.phone = i.phone + (c.articulo.valor*c.cantidad)/1000000

    listas = []
    for i in lista:

        listas.append((str(i.name), float(i.phone)))   

    listas = sorted(listas, key=lambda tup: tup[1], reverse=True)

    # --> Modelo para armar el listado de los articulos

    lista_articulos = Articulos.objects.all()

    for i in lista_articulos:

        i.valor = 0

        for c in stock:

            if i == c.articulo:

                i.valor = i.valor + (c.articulo.valor*c.cantidad)/1000000

    listas_art = []

    for i in lista_articulos:

        listas_art.append((str(i.nombre), float(i.valor)))

    
    listas_art = sorted(listas_art, key=lambda tup: tup[1], reverse=True)

    # --> Modelo para armar el stock por fideicomiso

    lista_proyectos = Proyectos.objects.all()

    for i in lista_proyectos:

        i.m2 = 0

        for c in stock:

            if i == c.proyecto:

                i.m2 = i.m2 + (c.articulo.valor*c.cantidad)/1000000

    listas_pro = []

    for i in lista_proyectos:

        if i.m2 != 0:

            listas_pro.append((str(i.nombre), float(i.m2)))

    
    listas_pro = sorted(listas_pro, key=lambda tup: tup[1], reverse=True)

    # --> Comprasas Nominales por fideicomiso

    compras_fidei = []

    for i in lista_proyectos:
        datos_compras = Compras.objects.filter(proyecto = i)
        
        valor_nominal_compras = 0

        for dato in datos_compras:
            if str(dato.articulo.nombre) != "FONDO DE REPARO ACT. UOCRA" and str(dato.articulo.nombre) != "ANTICIPO FINANCIERO ACT. UOCRA":
                valor_nominal_compras = valor_nominal_compras + dato.precio*dato.cantidad

        if valor_nominal_compras != 0:
        
            compras_fidei.append((i, valor_nominal_compras))

    
    datos = {"stock_valorizado":stock_valorizado,
    "stock_valorizado_m":stock_valorizado_m,
    "stock_valorizado_usd":stock_valorizado_usd,
    "stock_valorizado_usd_m":stock_valorizado_usd_m,
    "lista_compras":lista_compras,
    "constantes":constantes,
    "listas":listas,
    "listas_art":listas_art,
    "listas_pro":listas_pro,
    "compras_nominal":compras_nominal,
    "compras_actualizado":compras_actualizado,
    "stock_pesos":stock_pesos,
    "stock_usd":stock_usd,
    "stock_horm":stock_horm,
    "compras_fidei":compras_fidei

    }

    return render(request, 'stockant.html', {'datos': datos})

# ----------------------------------------------------- VISTAS PARA CARGA DE RETIROS----------------------------------------------

def cargaretiro(request, nombre_compra):

    compras = Compras.objects.all()

    for i in compras:
        if str(i.nombre) == "29032019.PUERTAS":
            print(i.nombre)

    return render(request, 'cargaretiro.html',)
