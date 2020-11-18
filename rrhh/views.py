from django.shortcuts import render
from django.shortcuts import redirect
from .models import NotaDePedido, datosusuario
from proyectos.models import Proyectos

# Create your views here.


def crearcorrespondencia(request):

    proyectos = Proyectos.objects.all()

    if request.method == 'POST':

        numero = len(NotaDePedido.objects.filter(tipo = request.POST['corres']))+1

        try:

            b = NotaDePedido(

                proyecto = Proyectos.objects.get(nombre = request.POST['proyecto']),
                numero = numero,
                titulo = request.POST['titulo'],
                creador = str(request.user.username),
                destinatario = request.POST['desti'],
                fecha_requerida = request.POST['fechareq'],
                copia = request.POST['copia'],
                adjuntos = request.FILES['archivo'],
                envio_documentacion = request.POST['envdoc'],
                cambio_proyecto = request.POST['camproy'],
                comunicacion_general = request.POST['comugral'],
                descripcion = request.POST['descripcion'],
                tipo = request.POST['corres'],
            )

            b.save()

        except:

            b = NotaDePedido(

                proyecto = Proyectos.objects.get(nombre = request.POST['proyecto']),
                numero = numero,
                titulo = request.POST['titulo'],
                creador = str(request.user.username),
                destinatario = request.POST['desti'],
                fecha_requerida = request.POST['fechareq'],
                copia = request.POST['copia'],
                envio_documentacion = request.POST['envdoc'],
                cambio_proyecto = request.POST['camproy'],
                comunicacion_general = request.POST['comugral'],
                descripcion = request.POST['descripcion'],
                tipo = request.POST['corres'],
            )

            b.save()

        return redirect('Notas de pedido', id_proyecto = 0, tipo = 0)



    return render(request, 'nuevacorres.html', {'proyectos':proyectos})

def notasdepedido(request, id_proyecto, tipo):

    proyectos = NotaDePedido.objects.values_list("proyecto")

    proyectos = list(set(proyectos))

    lista_proyectos = []

    for p in proyectos:

        lista_proyectos.append(Proyectos.objects.get(id = p[0]))

    datos = 0

    if id_proyecto == "0":


        if tipo == "0":

            datos = NotaDePedido.objects.all()

        elif tipo == "1":

            datos = NotaDePedido.objects.filter(tipo = "NP")

        elif tipo == "2":

            datos = NotaDePedido.objects.filter(tipo = "OS")

    if id_proyecto != "0":


        if tipo == "0":

            datos = NotaDePedido.objects.filter(proyecto__id = id_proyecto)

        elif tipo == "1":

            datos = NotaDePedido.objects.filter(tipo = "NP", proyecto__id = id_proyecto)

        elif tipo == "2":

            datos = NotaDePedido.objects.filter(tipo = "OS", proyecto__id = id_proyecto)




    if request.method == 'POST':



        datos_viejos = datos

        datos = []   

        palabra_buscar = request.POST["palabra"]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                lista_palabra = palabra.split()

                buscar = (str(i.proyecto)+str(i.titulo)+str(i.tipo)+str(i.numero)+str(i.creador)+str(i.destinatario))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)


    return render(request, 'notasdepedido.html', {'datos':datos, "id_proyecto":id_proyecto, "tipo":tipo, "lista_proyectos":lista_proyectos})

def notadepedido(request, id_nota):

    datos = NotaDePedido.objects.get(id = id_nota)

    try:
        creador = datosusuario.objects.get(identificacion=datos.creador)

    except:
        creador = 0

    try:
        destino = datosusuario.objects.get(identificacion=datos.destinatario)

    except:
        destino = 0

    if request.method == 'POST':

        datos_post = request.POST.items()

        if str(datos.visto) == "None":

            datos.visto = str(request.POST["FIRMA"]) + " "

        else:

            datos.visto = str(datos.visto) + str(request.POST["FIRMA"]) + " "

        datos.save()

        return redirect('Notas de pedido', id_proyecto = 0, tipo = 0)


    return render(request, 'notadepedido.html', {'datos':datos, 'creador':creador, 'destino':destino})