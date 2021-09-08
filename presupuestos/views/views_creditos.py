
from django.shortcuts import render, redirect
from proyectos.models import Proyectos
from presupuestos.models import  Presupuestos
from presupuestos.functions.functions_saldo import Creditocapitulo
import numpy as np
from presupuestos.functions.functions_credito import ajustar_analisis, ajustar_capitulo, ajustar_todo,get_capitulos_analisis


def creditos(request, id_proyecto):

    proyecto = Proyectos.objects.get(id = id_proyecto)

    if request.method=='POST':

        # Variables para trabajar 
        
        datos=request.POST.dict()
   
        cantidad_sobrante=float(datos['sobrante'])

        if 'modificar-analisis' in datos:

            ajustar_analisis(proyecto, cantidad_sobrante, datos['analisis'], datos['modificar-analisis'])
            return redirect('Creditos de proyectos',proyecto.id)
            #-> Ajusta el analisis siempre

        if 'modificar-capitulo' in datos:
        
            ajustar_capitulo(proyecto,cantidad_sobrante,datos['capitulo'], datos['modificar-capitulo'])
            
            return redirect('Creditos de proyectos',proyecto.id)
            #-> Ajusta el capitulo siempre

        if 'crear' in datos:
            nombre_na=datos['nombre-analisis']
            codigo_na=datos['codigo-analisis']
            unidad_na=datos['unidad-analisis']
            codigo_articulo=datos['crear']
            #nombre_nc=datos['nombre-capitulo']

            if datos['capitulo']=='':
                nuevo=True
                nombre_capitulo=(datos['nombre-capitulo'],nuevo)
            else:
                nuevo=False
                nombre_capitulo=(datos['capitulo'],nuevo)

            #nombre del nuevo analisis  codigo del nuevo a  unidad del nuevo a   nuevo nombre del capitulo
            ajustar_todo(proyecto,cantidad_sobrante,nombre_capitulo,nombre_na,codigo_na,unidad_na,codigo_articulo)

            return redirect('Creditos de proyectos',proyecto.id)
            #-> Crea un analisis dentro un capitulo para ajustar

    aux = Creditocapitulo(id_proyecto)

    datos=get_capitulos_analisis(proyecto,aux)

    context = {}
    context['explosion'] = datos[0]
    context['explosion_no'] = datos[1]
    context['proyecto'] = proyecto
    context['valor_saldo'] = sum(np.array([ data[4] for data in datos[0] if data[4] > 0]))
    context['valor_credito'] = sum(np.array([ data[4] for data in datos[0] if data[4] < 0])) + sum(np.array([ data[4] for data in datos[1] if data[4] < 0])) 

    #### Guardamos el valor del credito en la base de presupuestos

    try:

        Cred_act = Presupuestos.objects.get(proyecto = proyecto)
        Cred_act.credito = context['valor_credito']
        Cred_act.save()

    except:
        
        pass

    return render(request, 'presupuestos/creditos.html', context)
