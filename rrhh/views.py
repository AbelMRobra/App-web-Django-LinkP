from django.shortcuts import render
from .models import NotaDePedido, datosusuario

# Create your views here.

def notasdepedido(request):

    datos = NotaDePedido.objects.all()

    return render(request, 'notasdepedido.html', {'datos':datos})

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

    return render(request, 'notadepedido.html', {'datos':datos, 'creador':creador, 'destino':destino})