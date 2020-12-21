from django.shortcuts import render
from proyectos.models import Proyectos
from .models import Etapas, ItemEtapa, TecnicaMensaje
from rrhh.models import datosusuario

# Create your views here.

def documentacion(request):

    datos_proyectos = Etapas.objects.values_list("proyecto")

    proyectos = []

    for d in datos_proyectos:
        proyectos.append(Proyectos.objects.get(id = d[0]))
    
    proyectos = list(set(proyectos))

    datos = []

    for p in proyectos:

        datos_etapas = Etapas.objects.filter(proyecto = p)

        sub_datos = []

        for e in datos_etapas:

            datos_itemetapas = ItemEtapa.objects.filter(etapa = e)

            sub_datos.append((e, datos_itemetapas))

        datos.append((p, sub_datos))

    return render(request, "documentacion.html", {"datos":datos})

def mensajesitem(request, id_item):

    if request.method == 'POST':

        datos_post = request.POST.items()

        for i in datos_post:

            if i[0] == "mensaje" and i[1] != "" :

                b = TecnicaMensaje(
                        usuario = datosusuario.objects.get(identificacion = request.user),
                        item = ItemEtapa.objects.get(id = id_item),
                        mensaje = i[1],

                        )

                b.save()


    datos = ItemEtapa.objects.get(id = id_item)

    mensajes = TecnicaMensaje.objects.filter(item__id = id_item).order_by("-fecha")

    return render(request, 'mensajeitem.html', {'datos':datos, 'mensajes':mensajes})