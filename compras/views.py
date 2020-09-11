import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Proveedores, Certificados
from .models import StockComprasAnticipadas, Compras, Proyectos, Proveedores, Retiros, Comparativas
from .form import StockAntForm
from .filters import CertificadoFilter
from presupuestos.models import Articulos, Constantes, Presupuestos
import sqlite3
import operator
import datetime
import dateutil.parser
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side 
from django.views.generic.base import TemplateView  


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

# ----------------------------------------------------- VISTAS PARA INFORME DE COMPRAS ---------------------------------------------- 

def informecompras(request):

    datos = 0

    if request.method == "POST":

        datos = request.POST.items()

        for dato in datos:

            if dato[0] == "fechainicial":
                fechainicial = dato[1]

            if dato[0] == "fechafinal":
                fechafinal = dato[1]

        datos_compra = Compras.objects.filter(fecha_c__range=(fechainicial, fechafinal))

        cantidad_doc = []
        proyectos = []

        #Listado d rubros

        materiales_electricos = 0
        materiales_electricos_estimado = 0
        materiales_sanitarios = 0
        materiales_sanitarios_esimado = 0
        materiales_pintura = 0
        materiales_pintura_esimado = 0


        monto_total = 0

        monto_estimado = 0

        for d in datos_compra:

            if "FONDO DE REPARO" in str(d.articulo.nombre) or "ANTICIPO" in str(d.articulo.nombre) or "DIANCO" in str(d.proyecto.nombre):
                print("No sumar")

            else:

                cantidad_doc.append((d.proyecto, d.proveedor, d.documento))
                proyectos.append(d.proyecto)
                monto_total = monto_total + d.precio*d.cantidad
                monto_estimado = monto_estimado + d.precio_presup*d.cantidad

                #Listado de los rubros mas importantes

                if "30900" in str(d.articulo.codigo):
                    materiales_electricos = materiales_electricos + d.precio*d.cantidad
                    materiales_electricos_estimado = materiales_electricos_estimado + d.precio_presup*d.cantidad

                
                if "31400" in str(d.articulo.codigo):
                    materiales_sanitarios = materiales_sanitarios + d.precio*d.cantidad
                    materiales_sanitarios_esimado = materiales_sanitarios_esimado + d.precio_presup*d.cantidad

                if "30700" in str(d.articulo.codigo):
                    materiales_pintura = materiales_pintura + d.precio*d.cantidad
                    materiales_pintura_esimado = materiales_pintura_esimado + d.precio_presup*d.cantidad

        
        #Aqui terminamos de armar la lista

        materiales_rubros = []

        materiales_rubros.append(("Materiales electricos", materiales_electricos, materiales_electricos_estimado, 0))
        materiales_rubros.append(("Materiales sanitarios", materiales_sanitarios, materiales_sanitarios_esimado, 0))
        materiales_rubros.append(("Pintura y afines", materiales_pintura, materiales_pintura_esimado, 0))
        
        
        cantidad_doc = len(set(cantidad_doc))

        datos_proyecto = []

        lista_proyectos = set(proyectos)

        for proyecto in lista_proyectos:

            monto_mat_p = 0
            monto_mo_p = 0
            monto_total_p = 0

            monto_mat_p_est = 0
            monto_mo_p_est = 0
            monto_total_p_est = 0

            for d in datos_compra:

                if proyecto == d.proyecto:

                    if "FONDO DE REPARO" in str(d.articulo.nombre) or "ANTICIPO" in str(d.articulo.nombre):
                        print("No sumar")

                    else:

                        monto_total_p = monto_total_p + d.cantidad*d.precio
                        monto_total_p_est= monto_total_p_est + d.cantidad*d.precio_presup

                    if str(d.articulo.codigo)[0] == "3":
                        monto_mat_p = monto_mat_p + d.cantidad*d.precio
                        monto_mat_p_est = monto_mat_p_est + d.cantidad*d.precio_presup

                    else:

                        if "FONDO DE REPARO" in str(d.articulo.nombre) or "ANTICIPO" in str(d.articulo.nombre):

                            print("No sumar")

                        else:

                            monto_mo_p = monto_mo_p + d.cantidad*d.precio
                            monto_mo_p_est = monto_mo_p_est + d.cantidad*d.precio_presup


            


            datos_proyecto.append((proyecto, monto_total_p, monto_total_p_est, monto_mat_p, monto_mat_p_est, monto_mo_p, monto_mo_p_est))


        try:
            diferencia = (monto_total/monto_estimado-1)*100
            diferencia_plata = monto_estimado - monto_total

        except:
            diferencia = 0
            diferencia_plata = 0

        cantidad_compras = len(datos_compra)

        datos = {"cantidad_compras":cantidad_compras, "cantidad_doc":cantidad_doc, "monto_total":monto_total,
        "fechafinal":fechafinal, "fechainicial":fechainicial, "monto_estimado":monto_estimado,
        "datos_proyecto":datos_proyecto, "diferencia":diferencia, "diferencia_plata":diferencia_plata,
        "materiales_rubros":materiales_rubros}

    return render(request, 'informe_compra_semana.html', {"datos":datos})




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

            
            elif i[0] == "fecha":
                
                fecha = i[1]
            
            
            else:

                resto.append(i)

        valor = 1


        try:


            for i in resto:

                if i[0] == "csrfmiddlewaretoken":

                    print("Basura")


                elif valor == 1:

                    valor = 2
    
                    articulo = Articulos.objects.get(nombre=i[1])

                elif valor == 2:

                    valor = 3

                    cantidad = i[1]
                    
                
                elif valor == 3:

                    valor = 4

                    precio = i[1]


                elif valor == 4:

                    valor = 1

                    partida= i[1]

                    partida_original = i[1]

                    partida = float(partida) - float(cantidad)*articulo.valor

                    if float(partida) > 0:

                        imprevisto = "PREVISTO"

                    elif float(partida) == 0:

                        imprevisto = "IMPREVISTO"

                        presupuesto_imprevisto = Presupuestos.objects.get(proyecto__id = proyecto)

                        partida = presupuesto_imprevisto.imprevisto - float(cantidad)*float(precio)

                        presupuesto_imprevisto.imprevisto = partida

                        presupuesto_imprevisto.save()

                    else:

                        imprevisto = "IMPREVISTO"

                        presupuesto_imprevisto = Presupuestos.objects.get(proyecto__id = proyecto)

                        partida = presupuesto_imprevisto.imprevisto - float(cantidad)*float(precio) + partida_original

                        presupuesto_imprevisto.imprevisto = partida

                        presupuesto_imprevisto.save()

                    b = Compras(
                        proyecto = Proyectos.objects.get(id=proyecto),
                        proveedor = Proveedores.objects.get(name=proveedor),
                        nombre = doc,
                        tipo = tipo,
                        documento = doc,
                        articulo = articulo,
                        cantidad = float(cantidad),
                        precio = float(precio),
                        precio_presup = articulo.valor,
                        fecha_c = fecha,
                        fecha_a = fecha,
                        partida = partida,
                        imprevisto = imprevisto,
                        )

                    b.save()

            return redirect('Compras')
           
        except:

            mensaje = "**Los datos ingresados no son correctos"

            datos = {'proyectos': proyectos, 'proveedores':proveedores, 'compras':compras, 'articulos':articulos, 'mensaje':mensaje}
    
    else:

        datos = {'proyectos': proyectos, 'proveedores':proveedores, 'compras':compras, 'articulos':articulos, 'mensaje':mensaje}


    return render(request, 'cargacompras.html', {'datos':datos})

# ----------------------------------------------------- VISTAS PARA LISTAR COMPRAS ----------------------------------------------


def comparativas(request):
    datos  = Comparativas.objects.order_by("-fecha_c")

    if request.method == 'POST':

        datos_post = request.POST.items()

        id_selec = 0

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

            if d[0] != 'csrfmiddlewaretoken' and d[0] != 'NO APROBADA' and d[0] != 'APROBADA':
                

                comparativa = Comparativas.objects.get(id = id_selec)

                comparativa.comentario = str(d[0]) + ": " + str(d[1])

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
    proyecto = 0

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        for i in palabra_buscar:
            if i[0] != "csrfmiddlewaretoken":
                pro = i[1]
        datos = Compras.objects.filter(documento__startswith="O", proyecto = pro)

        proyecto = Proyectos.objects.get(id = pro)

    #Establecemos el periodo de tiempo

    inicio_fecha = date.today() - datetime.timedelta(days = 365)

    fechas = []

    contador = 0

    for fecha in range(14):
        fecha_agregar = inicio_fecha + datetime.timedelta(days = ((365*contador/12)))
        fechas.append(fecha_agregar)
        contador +=1 


    fechas_compras = []

    monto_compras = 0
    monto_presupuesto = 0

    contador = 0

    for dato in range(13):

        volumen_comprado = 0
        volumen_presupuesto = 0
        rendimiento = 100

        for compra in datos:

            date_object = datetime.datetime.strptime(str(compra.fecha_c), '%Y-%m-%d')
            date_object = dateutil.parser.parse(str(date_object)).date()

            if date_object >= fechas[contador] and date_object < fechas[contador +1]:
                volumen_comprado = volumen_comprado + (compra.cantidad*compra.precio)/1000
                monto_compras = monto_compras + (compra.cantidad*compra.precio)/1000

                if compra.precio_presup != None:
                    volumen_presupuesto = volumen_presupuesto + (compra.cantidad*compra.precio_presup)/1000
                    monto_presupuesto = monto_presupuesto + (compra.cantidad*compra.precio_presup)/1000
        
        
        if volumen_presupuesto != 0:
            rendimiento = (volumen_comprado/volumen_presupuesto)*100

        fechas_compras.append((fechas[contador], volumen_comprado, volumen_presupuesto, rendimiento))
        contador += 1

    inc_total = (monto_compras/monto_presupuesto)*100

    datos = {"datos":fechas_compras,
    "montocompras":monto_compras,
    "inc":inc_total,
    "proyectos":proyectos,
    "proyecto":proyecto}

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

# ----------------------------------------------------- VISTAS PARA CARGA DE RETIROS----------------------------------------------

class Reegistrodecompras(TemplateView):

    def get(self, request, *args, **kwargs):
        
        wb = Workbook()

        #Aqui coloco la formula para calcular

        datos = Compras.objects.order_by("fecha_c")

        ws = wb.active
        ws.title = "ADVERTENCIA"

        ws.merge_cells("B2:K2")
        ws["B2"] = "LEER ATENTAMENTE ANTES DE USAR ESTE DOCUMENTO"

        ws["B2"].alignment = Alignment(horizontal = "center")
        ws["B2"].font = Font(bold = True, color= "CF433F", size = 20)

        ws.merge_cells("B5:K25")
        ws["B5"] = "Este documento contiene informción --> PRIVADA <-- del área de presupuestos, \n la misma es solo para uso interno de LINK INVERSIONES y no debe ser compartida sin previa autorización. Compartir este archivo puede ser considerado como divulgar información confidencial. Si usted esta utilizando este archivo en una computadora que no pertenezca a la empresa, al finalizar --> ELIMINE <-- el archivo. Gracias --AR"
        ws["B5"].alignment = Alignment(horizontal = "center", vertical = "center", wrap_text=True)
        ws["B5"].font = Font(bold = True)
        
        cont = 1
        
        for d in datos:

            if cont == 1:
                ws = wb.create_sheet("My sheet")
                ws.title = "Registrodecompras"
                ws["A"+str(cont)] = "PROYECTO"
                ws["B"+str(cont)] = "ARTICULO"
                ws["C"+str(cont)] = "UNIDAD"
                ws["D"+str(cont)] = "VALOR"
                ws["E"+str(cont)] = "CANTIDAD"
                ws["F"+str(cont)] = "PROVEEDOR"
                ws["G"+str(cont)] = "FECHA"
                ws["H"+str(cont)] = "DOCUMENTO"


                ws["A"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["E"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["F"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont)].alignment = Alignment(horizontal = "center")


                ws["A"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["A"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")
                ws["B"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["B"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")
                ws["C"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["C"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")
                ws["D"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["D"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")
                ws["E"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["E"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")
                ws["F"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["F"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")
                ws["G"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["G"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")
                ws["H"+str(cont)].font = Font(bold = True, color= "FDFFFF")
                ws["H"+str(cont)].fill =  PatternFill("solid", fgColor= "159ABB")


                ws.column_dimensions['A'].width = 23.29
                ws.column_dimensions['B'].width = 63.86
                ws.column_dimensions['C'].width = 7.57
                ws.column_dimensions['D'].width = 12.14
                ws.column_dimensions['E'].width = 18.57
                ws.column_dimensions['F'].width = 46.71
                ws.column_dimensions['G'].width = 12
                ws.column_dimensions['H'].width = 31

                ws["A"+str(cont+1)] = d.proyecto.nombre
                ws["B"+str(cont+1)] = d.articulo.nombre
                ws["C"+str(cont+1)] = d.articulo.unidad
                ws["D"+str(cont+1)] = d.precio
                ws["E"+str(cont+1)] = d.cantidad
                ws["F"+str(cont+1)] = d.proveedor.name
                ws["G"+str(cont+1)] = d.fecha_c
                ws["H"+str(cont+1)] = d.documento


                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["E"+str(cont+1)].number_format = '#,##0.00_-'
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].alignment = Alignment(horizontal = "center")
  

                cont += 1

            else:
                ws = wb["Registrodecompras"]

                ws["A"+str(cont+1)] = d.proyecto.nombre
                ws["B"+str(cont+1)] = d.articulo.nombre
                ws["C"+str(cont+1)] = d.articulo.unidad
                ws["D"+str(cont+1)] = d.precio
                ws["E"+str(cont+1)] = d.cantidad
                ws["F"+str(cont+1)] = d.proveedor.name
                ws["G"+str(cont+1)] = d.fecha_c
                ws["H"+str(cont+1)] = d.documento


                ws["A"+str(cont+1)].font = Font(bold = True)
                ws["A"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["B"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["C"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["D"+str(cont+1)].number_format = '"$"#,##0.00_-'
                ws["E"+str(cont+1)].number_format = '#,##0.00_-'
                ws["F"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["G"+str(cont+1)].alignment = Alignment(horizontal = "center")
                ws["H"+str(cont+1)].alignment = Alignment(horizontal = "center")


                cont += 1

        #Establecer el nombre del archivo
        nombre_archivo = "Registrodecompras.xls"
        #Definir tipo de respuesta que se va a dar
        response = HttpResponse(content_type = "application/ms-excel")
        contenido = "attachment; filename = {0}".format(nombre_archivo)
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response
