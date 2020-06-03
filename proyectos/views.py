from django.shortcuts import render
from .models import Proyectos, Unidades, ProyectosTerceros

# Create your views here.

def proyectos(request):

    datos = Proyectos.objects.all()

    return render(request, 'proyectos.html', {'datos':datos})

def unidades(request):

    unidades = Unidades.objects.all()
    datos = []

    for dato in unidades:

        if dato.sup_balcon == None:
            dato.sup_balcon = 0

        if dato.sup_patio == None:
            dato.sup_patio = 0

        m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio
        datos.append((dato, m2))

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

                

                buscar = (str(i[0].proyecto)+str(i[0].nombre_unidad)+str(i[0].asig)+str(i[0].estado)+str(i[0].piso_unidad)+str(i[0].tipo)+str(i[1]))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)


    #Aqui termina el filtro

    return render(request, 'psuperficie.html', {"datos":datos})