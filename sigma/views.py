from django.shortcuts import render, redirect
from .models import Inventario, Tarea, SubTarea, Operario
import datetime

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

    datos_totales = []

    for d in datos:

        subtareas = SubTarea.objects.filter(vinculacion = d)

        datos_totales.append((d, subtareas))


    return render(request, 'tareas.html', {"datos":datos_totales})


def login(request):

    if request.method == 'POST':

        if Operario.objects.get(dni = request.POST['dni']):

            return redirect('Parte diarios', dni = request.POST['dni'])

    return render(request, 'login.html')

def partesdiarios(request, dni):

    datos = Operario.objects.filter(dni = int(dni))


    return render(request, 'partediarios.html', {"datos":datos})



