from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import ComputosForm
from .filters import ComputosFilter
from proyectos.models import Proyectos
from .models import Plantas, ListaRubros, Tipologias, Computos

# Create your views here.

def listacomputos(request):

    datos = Computos.objects.all()

    myfilter = ComputosFilter(request.GET, queryset=datos)

    datos = myfilter.qs

    c = {'datos':datos, 'myfilter':myfilter}

    return render(request, 'lista_computos.html', c)


#----------------------------------------------- VISTA PARA EL RESUMEN DE COMPUTOS -----------------------------------------------------------

def resumencomputos(request):
    
    rubros = ListaRubros.objects.all()
    tipologia = Tipologias.objects.all()
    computo = Computos.objects.all()

    datos = []

    for i in rubros:

        for c in tipologia:

            total_presupuesto = 0
            total_obra = 0

            for d in computo:
               
                if i == d.rubro and c == d.tipologia:
                    total_presupuesto = total_presupuesto + d.valor_total
                    total_obra = float(total_obra) + float(d.valor_obra)
            
            if total_presupuesto != 0:
                datos.append((i, c , total_presupuesto, total_obra))

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

                buscar = (str(i[0].nombre)+str(i[1].nombre))

                if palabra.lower() in buscar.lower():

                    datos.append(i)


    #Aqui termina el filtro


    return render(request, 'resumencomputos.html', {'datos':datos})



def CrearListaComputos(request):

    datos_proyectos = Proyectos.objects.all()

    for i in datos_proyectos:

        if i.nombre == "TORRE BLUE":

            dato_proyecto_form = i

            datos_plantas = Plantas.objects.all()

            for i in datos_plantas:

                dato_planta_form = i

                datos_rubros = ListaRubros.objects.all()

                for i in datos_rubros:

                    nombre_rubro = i
                    
                    dato_rubro_form = i

                    datos_tipologias = Tipologias.objects.all()

                    for i in datos_tipologias:

                        if str(nombre_rubro.nombre) == str(i.rubro):

                            dato_tipologia_form = i


                            b = Computos(
                                proyecto = dato_proyecto_form,
                                planta = dato_planta_form, 
                                rubro = dato_rubro_form, 
                                tipologia = dato_tipologia_form, 
                                valor_lleno = 0, 
                                valor_vacio = 0,
                                valor_total = 0, 
                                valor_obra = 0, 
                                )

                            b.save()



    return render(request, 'computos.html',)

    #La idea es agregar un campo por cada cosa



