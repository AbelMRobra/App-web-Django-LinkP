from django.shortcuts import render, redirect
from presupuestos.models import Constantes, Articulos, Presupuestos
from presupuestos.form import ConsForm
from presupuestos.functions.functions_presupuestos import bot_telegram

def constantes_crear(request):

    escenario = 0

    if request.method == 'POST':
        form = ConsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('Cons_panel')
        
    else:
        form = ConsForm()

    context = {'form':form, "escenario": escenario}
    return render(request, 'constantes/cons_create.html', context )

def constantes_panel_maestro(request):

    cons_actuales = Constantes.objects.all()
    context = {'constantes':cons_actuales}
    return render(request, 'constantes/cons_list.html', context )

def constantes_panel(request):

    cons_actuales = Constantes.objects.all()

    context = {'constantes':cons_actuales}

    return render(request, 'constantes/cons_panel.html', context )

def constantes_editar(request, id_cons):

    escenario = 1

    cons = Constantes.objects.get(id=id_cons)

    if request.method == 'GET':
        form = ConsForm(instance = cons)
    else:
        form = ConsForm(request.POST, instance = cons)
        
        if form.is_valid():

            # Rescato el nombre y el valor nuevo de la constante

            datos = request.POST.items() 

            for key, value in datos:

                if key == 'nombre':

                    nombre = (value)
                    
                if key == 'valor':

                    cons_valor_nuevo = (value)

            datos_constante = Constantes.objects.filter(nombre = nombre)

            for i in datos_constante:
                
                if str(i.nombre) == str(nombre):
                    
                    cons_nombre = i.nombre

                    cons_valor = i.valor

                    form.save()

                    if cons_valor != 0:
                        var = round((float(cons_valor_nuevo)/cons_valor-1)*100,2)

                        if var != 0:

                            send = "{} ha modificado la constante {}. Variación: {}%".format(request.user.username, cons_nombre, var)

                            id = "-455382561"

                            token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"

                            bot_telegram(send, id, token)

            datos_insumos = Articulos.objects.filter(constante__nombre = nombre)

            for i in datos_insumos:

                valor_actual = i.valor

                valor_nuevo = valor_actual*(float(cons_valor_nuevo)/cons_valor) 

                i.valor = valor_nuevo

                i.save()

            if nombre == "UVA":

                datos = Presupuestos.objects.all()
                
                for d in datos:
                    valor_nuevo = d.imprevisto*(float(cons_valor_nuevo)/cons_valor) 
                    d.imprevisto = valor_nuevo
                    d.save()

        return redirect('Cons_panel')
    
    return render(request, 'constantes/cons_create.html', {'form':form, "escenario": escenario})

def constantes_eliminar(request, id_cons):

    cons = Constantes.objects.get(id=id_cons)

    if request.method == 'POST':
        cons.delete()
        return redirect('Cons_panel')
    return render(request, 'constantes/cons_delete.html', {'cons':cons})