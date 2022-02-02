from django.shortcuts import render, redirect
from compras.models import Proveedores, Contratos, Comparativas
from rrhh.models import datosusuario
from ..funciones.comparativas_agregar import *

def comparativas_agregar(request):

    context = {}
    mensaje = 0

    if request.method == "POST":
        validacion = comparativas_agregar_validaciones(request.POST['proveedor'], request.POST['numerooc'])

        if validacion != True:
            context['mensaje_e'] = validacion

        else:
            agregar_comparativa = comparativas_agregar_metodo(request.POST['proveedor'], request.POST['proyecto'], 
                    request.POST['referencia'], request.POST['valor'], request.FILES['imagen'], 
                    request.POST['numerooc'], request.POST['autoriza'], request.POST['publica'], 
                    str(request.user.username), request.POST['tipo_oc'], request.POST['contrato'], request.POST['gerente'])

            if agregar_comparativa[0] == True:
                nueva_comparativa = Comparativas.objects.get(id = agregar_comparativa[1])

                try:
                    nueva_comparativa.adj_oc = request.FILES['oc']
                    nueva_comparativa.save()
                
                except:
                    pass

                return redirect(f'/compras/comparativas/{10}/{0}/{0}#{nueva_comparativa.id}')

            else:
                context['mensaje_e'] = agregar_comparativa[1]

    
    context['mensaje'] = mensaje
    context['proveedores'] = Proveedores.objects.all()
    context['contratos'] = Contratos.objects.all()
    context['gerentes'] = datosusuario.objects.filter(cargo = "GERENTE").exclude(estado = "NO ACTIVO")
        
    return render(request, 'comparativas/comparativa_agregar.html', context)