from django.shortcuts import render, redirect
from .models import Inventario, Tarea, SubTarea, Operario, Partediario
from presupuestos.models import Articulos
import datetime
import re

# Create your views here.

def inventario(request):

    context = {}

    context['articulos'] = Articulos.objects.all()

    return render(request, 'inventario.html', context)

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




