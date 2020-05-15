from django.shortcuts import render
from .models import EstudioMercado
from proyectos.models import Unidades, Proyectos
from datetime import date

# Create your views here.

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


    print(meses)
    print(datos_link)


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

        contador = 0

        for dato in datos_elegidos:
            if contador == 0:
                contador += 1
            elif contador == 1:
                proyecto = Proyectos.objects.get(id = dato[1])
                contador += 1

            elif contador == 2:
                estado = dato[1]
                contador += 1

            elif contador == 3:
                asig = dato[1]

        
        try:
            unidades = Unidades.objects.filter(proyecto = proyecto, asig__contains = asig, estado = estado )

            if len(unidades) == 0:
                mensaje = 1
            else:
                datos_unidades = 1

                datos = []
                otros_datos = []

                m2_totales = 0
                
                cantidad = len(unidades)

                departamentos = 0

                cocheras = cantidad - departamentos

                for dato in unidades:

                    if dato.sup_balcon == None:
                        dato.sup_balcon = 0

                    if dato.sup_patio == None:
                        dato.sup_patio = 0

                    m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio
                    m2_totales = m2_totales + m2
                    datos.append((dato, m2))

                    if dato.tipo == "DEPARTAMENTO":
                        departamentos = departamentos + 1

                cocheras = cantidad - departamentos
                
                otros_datos.append(m2_totales)
                otros_datos.append(cantidad)
                otros_datos.append(departamentos)
                otros_datos.append(cocheras)
                

        except:
            mensaje = 1

    datos = {"proyectos":proyectos, "datos":datos, "mensaje":mensaje, "datos_unidades":datos_unidades, "otros_datos":otros_datos}

    return render(request, 'panelunidades.html', {"datos":datos})


