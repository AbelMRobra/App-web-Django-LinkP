from django.shortcuts import render
from .models import EstudioMercado, PricingResumen
from proyectos.models import Unidades, Proyectos
from ventas.models import Pricing, ArchivosAreaVentas
from datetime import date
import datetime

# Create your views here.

def radiografia(request):

    busqueda = 1
    datos_pricing = ArchivosAreaVentas.objects.all()
    datos = 0
    fecha = 0

    fechas = []

    for dato in datos_pricing:
        fechas.append((dato.fecha, str(dato.fecha)))

    fechas = list(set(fechas))

    fechas.sort( reverse=True)

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAreaVentas.objects.get(fecha = dato[1])
                busqueda = 0
                fecha = dato[1]




    datos = {"fechas":fechas,
    "busqueda":busqueda,
    "datos":datos,
    "fecha":fecha}

    return render(request, 'radiografiaclientes.html', {"datos":datos})

def resumenprecio(request):

    busqueda = 1
    datos_pricing = PricingResumen.objects.all()
    datos = 0
    fecha = 0

    fechas = []

    for dato in datos_pricing:
        fechas.append((dato.fecha, str(dato.fecha)))

    fechas = list(set(fechas))

    fechas.sort( reverse=True)

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:
            if dato[0] == "fecha":
                datos = PricingResumen.objects.filter(fecha = dato[1])
                busqueda = 0
                fecha = dato[1]



    datos = {"fechas":fechas,
    "busqueda":busqueda,
    "datos":datos,
    "fecha":fecha}

    return render(request, 'resumenprecio.html', {"datos":datos})





def estmercado(request):

    datos_estudio = EstudioMercado.objects.all()

    estudios = []
    meses = []
    datos_link = []
    datos_otros = []
    grafico = 0

    for dato in datos_estudio:

        estudios.append(str(dato.fecha))
        meses.append(dato.meses)

    estudios = list(set(estudios))
    meses = list(set(meses))
    meses.sort()

    if request.method == 'POST':

        grafico = 1

        estudio = request.POST.items()

        for dato in estudio:

            if dato[0] == 'csrfmiddlewaretoken':
                print("Basura")

            else:

                for i in datos_estudio:
                    if str(i.fecha) == dato[1]:
                        if i.empresa == "LINK":
                            datos_link.append(i)
                        else:
                            datos_otros.append(i)

    datos = {
        "link":datos_link,
        "otros":datos_otros,
        "meses":meses,
        "estudios":estudios,
        "graficos":grafico,
    }

    return render(request, 'estmercado.html', {"datos":datos})

def panelunidades(request):

    datos = Unidades.objects.all()

    proyectos = []

    datos_unidades = 0

    mensaje = 0

    otros_datos = 0


    for dato in datos:
        proyectos.append(dato.proyecto)

    proyectos = list(set(proyectos))


    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        list_proyectos = []
        aisgnacion = []
        disponibilidad = []

        for dato in datos_elegidos:

            if "Asig" in str(dato[0]):
                aisgnacion.append(dato[1])

            elif "Disp" in str(dato[0]):
                disponibilidad.append(dato[1])

            elif str(dato[0]) == "csrfmiddlewaretoken":
                print("basura")

            else:
                list_proyectos.append(dato[0])

        if len(list_proyectos)==0 or len(aisgnacion)==0 or len(disponibilidad)==0:
            mensaje = 1

        else:
            mensaje = 2
            otros_datos = []
            datos_tabla_unidad = []
            m2_totales = 0
            cocheras = 0

            for proy in list_proyectos:
                for asig in aisgnacion:
                    for disp in disponibilidad:
                        datos_unidades = Unidades.objects.filter(proyecto__nombre = proy, asig = asig, estado=disp)
                        for dato in datos_unidades:
                            m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio
                            
                            try:
                                param_uni = Pricing.objects.get(unidad = dato)
                                desde = dato.proyecto.desde

                                if param_uni.frente == "SI":
                                    desde = desde*1.03

                                if param_uni.piso_intermedio == "SI":
                                    desde =desde*1.02

                                if param_uni.cocina_separada == "SI":
                                    desde = desde*1.03

                                if param_uni.local == "SI":
                                    desde = desde*1.75

                                if param_uni.menor_50_m2 == "SI":
                                    desde = desde*1.03

                            except:

                                if dato.tipo == "COCHERA":
                                    try:
                                        desde = dato.proyecto.desde*(1-0.24)
                                    except:
                                        desde = "NO DEFINIDO"

                                else:
                                    desde = "NO DEFINIDO"

                            datos_tabla_unidad.append((dato, m2, desde))
                            m2_totales = m2_totales + m2
                            if dato.tipo == "COCHERA":
                                cocheras += 1
                            


            cantidad = len(datos_tabla_unidad)

            departamentos = cantidad - cocheras

            otros_datos.append((m2_totales, cantidad, departamentos, cocheras))

            datos_unidades = datos_tabla_unidad

    datos = {"proyectos":proyectos, "datos":datos, "mensaje":mensaje, "datos_unidades":datos_unidades, "otros_datos":otros_datos}

    return render(request, 'panelunidades.html', {"datos":datos})


