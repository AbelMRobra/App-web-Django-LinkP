from django.shortcuts import render
from .models import Inventario
import datetime

# Create your views here.

def inventario(request):

    datos = Inventario.objects.all()

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
    "total":total_inventario}


    return render(request, 'inventario.html', {"datos":datos})
