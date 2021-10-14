import numpy as np

from django.shortcuts import render, redirect
from finanzas.models import CuentaCorriente, Cuota, Pago
from presupuestos.models import Constantes
from proyectos.models import Proyectos
from finanzas.funciones.funciones_ctacte import *


def ctacte_proyecto(request, id_proyecto):

    context = {}

    context["proyecto"] = Proyectos.objects.get(id = id_proyecto)

    context["datos"] = CuentaCorriente.objects.filter(venta__proyecto = context["proyecto"])

    return render(request, 'ctacte/ctacte_proyecto.html', context)

def ctacte_cliente(request, id_cliente):

    ctacte_revision_cuotas(id_cliente)

    context = {}

    try:

        frozen = Constantes.objects.get(cuenta_corriente = id_cliente)
        context["frozen"] = frozen.valor
    
    except:

        frozen = 0
        context["frozen"] = frozen

    if request.method == 'POST':

        datos_post = request.POST.dict()

        if 'frozen' in datos_post:
        
            try:
  
                if len(Constantes.objects.filter(cuenta_corriente = id_cliente)):
                    frozen.valor = request.POST['valor']
                    frozen.save()
                
                else:
                    frozen = Constantes(
                        nombre = "FROZEN-{}".format(id_cliente),
                        valor =request.POST['valor'],
                        descrip = "Constante para cuenta corrientes",
                        cuenta_corriente = id_cliente
                    )

                    frozen.save()

                context["mensaje"] = [1, "Se establecio el valor de cuota congelada"]

            except:

                context["mensaje"] = [0, "Error inesperado"]

        if 'baja-cuenta' in datos_post:
     
            ids=request.POST['baja-cuenta']
            
            lista_ids=ids.split('-')
            
            id_cuenta=lista_ids[0]
            
            id_proyecto=lista_ids[1]
            
            cuenta=CuentaCorriente.objects.get(pk=int(id_cuenta))
            
            if cuenta.estado=='activo':
                cuenta.estado='baja'
                cuenta.save()
                return redirect('Cuenta corriente proyecto',id_proyecto)

            else:
                cuenta.estado='activo'
                cuenta.save()
                return redirect('Cuenta corriente proyecto',id_proyecto)


        if 'revison_cuenta' in datos_post:

            datos_iterar = request.POST.items()

            try:
            
                list_cuotas_id = Cuota.objects.filter(cuenta_corriente__id = id_cliente, constante = frozen).values_list("id", flat = True)
                list_cuotas_id = list(set(list_cuotas_id))
                
                for d in datos_iterar:

                    if "cuota" in d[0]:
                        cuota = Cuota.objects.get(id = d[1])
                        cuota.constante = frozen
                        cuota.save()
                        
                        try:

                            list_cuotas_id.remove(int(d[1]))
                        except:

                            pass

                for nf in list_cuotas_id:
                    
                    cuota = Cuota.objects.get(id = nf)
                    cuota.constante = Constantes.objects.get(id = 7)
                    cuota.save()

                context["mensaje"] = [1, "Se congelaron cuotas correctamente"]

            except:

                context["mensaje"] = [0, "Error inesperado"]

        

    ctacte = CuentaCorriente.objects.get(id = id_cliente)
    context["ctacte"] = ctacte
    context["cuotas"] = Cuota.objects.filter(cuenta_corriente = ctacte).order_by("fecha")

    return render(request, 'ctacte/ctacte_cliente.html', context)

def ctacte_cuota_eliminar(request, id_cuota):

    context = {}

    context["cuota"] = Cuota.objects.get(id = id_cuota)

    if request.method == 'POST':

        context["cuota"].delete()

        return redirect('Cuenta corriente venta', id_cliente = context["cuota"].cuenta_corriente.id)

    return render(request, 'ctacte/ctacte_cuota_eliminar.html', context)
    
def ctacte_cuota_editar(request, id_cuota):

    context = {}

    cuota = Cuota.objects.get(id = id_cuota)

    context['cuota'] = cuota

    if request.method == 'POST':
        
        cuota.fecha = request.POST['fecha']
        cuota.concepto = request.POST['concepto']
        cuota.precio = float(request.POST['precio'])

        if request.POST['tipo_venta'] == "HORM":

            cuota.constante = Constantes.objects.get(nombre = "Hº VIVIENDA")

        else:
            cuota.constante = Constantes.objects.get(nombre = "USD")


        cuota.save()

        return redirect('Cuenta corriente venta', id_cliente = cuota.cuenta_corriente.id)

    return render(request, 'ctacte/ctacte_cuota_editar.html', context)

