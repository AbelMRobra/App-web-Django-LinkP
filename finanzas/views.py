from django.shortcuts import render
from presupuestos.models import Proyectos, Presupuestos

# Create your views here.


def almacenero(request):

    proyectos = Proyectos.objects.order_by("nombre")

    datos = 0

    if request.method == 'POST':

        #Trae el proyecto elegido

        proyecto_elegido = request.POST.items()

        #Crea los datos del pricing

        datos = []

        for i in proyecto_elegido:

            if i[0] == "proyecto":
                proyecto = Proyectos.objects.get(id = i[1])
                presupuesto = Presupuestos.objects.get(proyecto = proyecto)
                datos.append(proyecto)
                datos.append(presupuesto)

        proyectos = 0

        

    datos = {"proyectos":proyectos,
    'datos':datos}

    return render(request, 'almacenero.html', {"datos":datos} )