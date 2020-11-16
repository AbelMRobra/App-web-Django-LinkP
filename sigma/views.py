from django.shortcuts import render, redirect
from .models import Inventario, Tarea, SubTarea, Operario, Partediario
import datetime
import re

# Create your views here.

def inventario(request):

    datos = Inventario.objects.all()

    listado_articulos = []

    for dato in datos:
        listado_articulos.append(dato.articulo.nombre)

    listado_articulos.sort()
    listado_articulos = set(listado_articulos)
    
    
    listado_art_cant = []

    for art in listado_articulos:
        contador = 0
        for dato in datos:
            if dato.articulo.nombre == art:
                contador += 1
        listado_art_cant.append((art, contador))


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

                buscar = (str(i.num_inv)+str(i.articulo))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)

    #Aqui termina el filtro

    datos_viejos = datos
    datos = []

    total_inventario = 0

    for dato in datos_viejos:
        ahora = datetime.datetime.utcnow()
        date_object = datetime.datetime.strptime(str(dato.fecha_compra), '%Y-%m-%d')
        fecha_amort = date_object + datetime.timedelta(days = (365*dato.amortizacion))
        avance = ahora - date_object
        avance_porc = avance/(fecha_amort-date_object)
        valor_amort = dato.articulo.valor - dato.articulo.valor*avance_porc

        total_inventario = total_inventario + valor_amort

        datos.append((dato, valor_amort, fecha_amort))

    datos = {"datos":datos,
    "total":total_inventario,
    "listado":listado_art_cant}


    return render(request, 'inventario.html', {"datos":datos})

def tareas(request):

    datos = Tarea.objects.all()

    #Aqui empieza el filtro

    if request.method == 'POST':

        datos_post = request.POST.items()

        for d in datos_post:

            if d[0] == 'palabra':

                datos_viejos = datos

                datos = []  

                palabra_buscar = request.POST["palabra"]

                if str(palabra_buscar) == "":

                    datos = datos_viejos

                else:
                
                    for i in datos_viejos:

                        palabra =(str(palabra_buscar))

                        lista_palabra = palabra.split()

                        buscar = (str(i.nombre)+str(i.rend)+str(i.unidad))

                        contador = 0

                        for palabra in lista_palabra:

                            contador2 = 0

                            if palabra.lower() in buscar.lower():

                                contador += 1

                        if contador == len(lista_palabra):

                            datos.append(i)


    datos_totales = []

    for d in datos:

        subtareas = SubTarea.objects.filter(vinculacion = d)

        datos_totales.append((d, subtareas))


    

    return render(request, 'tareas.html', {"datos":datos_totales})


def login(request):

    mensaje = 0

    if request.method == 'POST':

        if len(Operario.objects.filter(dni = request.POST['dni'])) > 0:

            return redirect('Parte diarios', dni = request.POST['dni'])

        else:
            mensaje = "Tu documento no se encuentra en nuestra nomina"

    return render(request, 'login.html', {"mensaje":mensaje})

def partesdiarios(request, dni):

    datos = Operario.objects.get(dni = int(dni))
    partes = Partediario.objects.filter(usuario = datos)


    return render(request, 'partediarios.html', {"datos":datos, "partes":partes})

def cargarpartediario(request, dni):

    datos = Operario.objects.get(dni = int(dni))
    subtareas = SubTarea.objects.all()
    operarios = Operario.objects.all()

    if request.method == 'POST':

        texto = request.POST['subtarea']
        numero = int(texto.split()[0])
        b = Partediario(

        usuario = datos,
        lider = str(Operario.objects.get(nombre = request.POST['lider']).dni),
        subtarea = SubTarea.objects.get(id = numero),
        horas = request.POST['rend'],
        avance = request.POST['avance'],
        )
        b.save()

        return redirect('Parte diarios', dni = datos.dni)

    return render(request, 'cargarparte.html', {"datos":datos, 'subtareas':subtareas, 'operarios':operarios})

def cargartarea(request):

    if request.method == 'POST':

        b = Tarea(
            nombre = request.POST['nombre'],
            unidad = request.POST['unidad'],
            descripcion = request.POST['descripcion'],
            rend = request.POST['rend'],
        )

        b.save()

        return redirect ('tareas')

    return render(request, 'creartarea.html')

def cargarsubtarea(request, id_tarea):

    datos = Tarea.objects.get(id = id_tarea)

    if request.method == 'POST':

        b = SubTarea(
            vinculacion = datos,
            nombre = request.POST['nombre'],
            unidad = request.POST['unidad'],
            descripcion = request.POST['descripcion'],
            rend = request.POST['rend'],
        )

        b.save()

        return redirect ('tareas')

    return render(request, 'subtarea.html', {'datos':datos})

def eliminartarea(request, id_tarea):

    datos = Tarea.objects.get(id = id_tarea)

    if request.method == 'POST':

        datos.delete()

        return redirect ('tareas')

    return render(request, 'eliminartarea.html', {'datos':datos})

def eliminarsubtarea(request, id_subtarea):

    datos = SubTarea.objects.get(id = id_subtarea)

    if request.method == 'POST':

        datos.delete()

        return redirect ('tareas')

    return render(request, 'eliminarsubtarea.html', {'datos':datos})




