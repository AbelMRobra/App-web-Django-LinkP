from django.shortcuts import render, redirect

from presupuestos.models import *
from presupuestos.form import ConsForm
from presupuestos.funciones.f_presupuestos import bot_telegram

def registro_constante(request):

    datos_constante = Constantes.objects.all()

    datos = []

    registros_constantes=Registrodeconstantes.objects.all()

    for dato in datos_constante:

        registros = []

        try:
            registro_constante = registros_constantes.filter(constante = dato).order_by("fecha")

            if len(registro_constante)>0:

                valor_referencia = registro_constante[0].valor

                for registro in registro_constante:

                    registros.append((registro, registro.valor/valor_referencia))

                datos.append((dato, registros))

        except:

            mensaje = "No hay registros de esta constanre"

    # Aqui armo para un grafico comparativo

    hormigon = registros_constantes.filter(constante__nombre = "Hº VIVIENDA").order_by("fecha")

    hormigon_list = []

    fecha = registros_constantes.values_list('fecha').filter(constante__nombre = "Hº VIVIENDA").order_by("fecha")

    contador = 0

    for h in hormigon:

        if contador == 0:

            hormigon_list.append(0)

            contador = h.valor

        else:

            hormigon_list.append(((h.valor/contador)-1)*100)


    usd = []
    usd_blue = []
    uva = []
    cac = []

    contador == 0

    valor_usd = 0
    valor_blue = 0
    valor_uva = 0
    valor_cac = 0


    for f in fecha:

        if contador == 0:

            usd.append(0)
            usd_blue.append(0)
            uva.append(0)
            cac.append(0)

            contador = 1

        else:

            try:

                
               
                if len(registros_constantes.filter(constante__nombre = "USD", fecha = f[0])) >0:

                    if valor_usd == 0:

                        valor_usd = registros_constantes.filter(constante__nombre = "USD", fecha = f[0])[0].valor

                    usd.append((((registros_constantes.filter(constante__nombre = "USD", fecha = f[0])[0].valor)/valor_usd) -1)*100 )
                
                else:

                    usd.append("")
            except:

                usd.append(valor_usd)
            

                
            try:

                            
                if len(registros_constantes.filter(constante__nombre = "USD_BLUE", fecha = f[0])) >0:

                    if valor_blue == 0:

                        valor_blue = registros_constantes.filter(constante__nombre = "USD_BLUE", fecha = f[0])[0].valor

                    usd_blue.append((((registros_constantes.filter(constante__nombre = "USD_BLUE", fecha = f[0])[0].valor)/valor_blue) -1)*100 )
                
                else:

                    usd_blue.append("")
            
            except:

                usd_blue.append(valor_blue)
            
            try:
                
                if len(registros_constantes.filter(constante__nombre = "UVA", fecha = f[0])) >0:

                    if valor_uva == 0:

                        valor_uva = registros_constantes.filter(constante__nombre = "UVA", fecha = f[0])[0].valor

                    uva.append((((registros_constantes.filter(constante__nombre = "UVA", fecha = f[0])[0].valor)/valor_uva) -1)*100 )
                
                else:

                    uva.append("")
            
            except:

                uva.append(valor_uva)


            try:
                
                if len(registros_constantes.filter(constante__nombre = "CAC_GENERAL", fecha = f[0])) >0:

                    if valor_cac == 0:

                        valor_cac = registros_constantes.filter(constante__nombre = "CAC_GENERAL", fecha = f[0])[0].valor

                    cac.append((((registros_constantes.filter(constante__nombre = "CAC_GENERAL", fecha = f[0])[0].valor)/valor_cac) -1)*100 )
                
                else:

                    cac.append("")
            except:

                cac.append(valor_cac)

    return render(request, 'constantes/cons_historico.html', {'datos':datos, 'fecha':fecha, 'hormigon':hormigon_list, 'usd':usd, 'usd_blue':usd_blue, 'uva':uva, 'cac':cac})


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