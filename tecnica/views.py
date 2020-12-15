from django.shortcuts import render
from proyectos.models import Proyectos
from .models import Etapas, ItemEtapa

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