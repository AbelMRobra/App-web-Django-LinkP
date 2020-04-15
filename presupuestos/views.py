from django.shortcuts import render, redirect
from django.http import HttpResponse
from .filters import ArticulosFilter
from .form import ConsForm, ArticulosForm
from .models import Articulos, Constantes, DatosProyectos, Prametros, Desde
import sqlite3


# ----------------------------------------------------- VISTAS PARA PARAMETROS----------------------------------------------

def parametros(request):

    datos = Prametros.objects.all()

    return render(request, 'desde/parametros.html', {'datos': datos})

# ----------------------------------------------------- VISTAS PARA INDICADOR DE PRECIOS----------------------------------------------

def desde(request):

    datos = Desde.objects.all()

    constantes = Constantes.objects.all()

    for i in datos:

        costo = i.presupuesto.valor

        costo = (costo/(1 + i.parametros.tasa_des_p))*(1 + i.parametros.soft)
        
        costo = costo*(1 + i.parametros.imprevitso)

        aumento_tem = i.parametros.tem_iibb*i.parametros.por_temiibb*(1+i.parametros.ganancia)

        aumento_comer = i.parametros.comer*(1+i.parametros.comer)
        

        costo = costo/(1-aumento_tem- aumento_comer)
        
        m2 = (i.parametros.proyecto.m2 - i.parametros.terreno - i.parametros.link)

        valor_costo = costo/m2
        
        valor_final = valor_costo*(1 + i.parametros.ganancia)

        valor_costo_usd = 0

        valor_final_usd = 0

        for c in constantes:
            print(c.nombre)

            if str(c.nombre) == 'USD_BLUE':

                valor_costo_usd = valor_costo/c.valor

                valor_final_usd = valor_final/c.valor

                
        print(valor_costo_usd)

        i.valor_costo = valor_costo
        i.valor_costo_usd = valor_costo_usd
        i.valor_final = valor_final
        i.valor_final_usd = valor_final_usd

        i.save()

    return render(request, 'desde/desde.html', {'datos':datos})

# ----------------------------------------------------- VISTAS PARA DATOS DE PROYECTOS ----------------------------------------------

def proyectos(request):

    datos = DatosProyectos.objects.all()

    return render(request, 'datos/projects.html', {'datos':datos})


# ----------------------------------------------------- VISTAS PARA CONSTANTES ----------------------------------------------

# VISTA --> Crear constante

def cons_create(request):

    if request.method == 'POST':
        form = ConsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('Cons_list')
        
    else:
        form = ConsForm()

    f = {'form':form}
    return render(request, 'constantes/cons_create.html', f )

# VISTA --> Listar constantes

def cons_list(request):

    cons_actuales = Constantes.objects.all()

    c = {'constantes':cons_actuales}

    return render(request, 'constantes/cons_list.html', c )

# VISTA --> Editar constantes

def cons_edit(request, id_cons):

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

            datos_constante = Constantes.objects.all()

            for i in datos_constante:
                if str(i.nombre) == str(nombre):
                    
                    cons_nombre = i.nombre

                    cons_valor = i.valor

                    print(form)

                    form.save()

            datos_insumos = Articulos.objects.all()

            for i in datos_insumos:

                if str(i.constante) == str(cons_nombre):
                    valor_actual = i.valor

                    valor_nuevo = valor_actual*(float(cons_valor_nuevo)/cons_valor) 

                    i.valor = valor_nuevo

                    i.save()

        return redirect('Cons_list')
    
    return render(request, 'constantes/cons_create.html', {'form':form})

# VISTA --> Eliminar constantes

def cons_delete(request, id_cons):

    cons = Constantes.objects.get(id=id_cons)

    if request.method == 'POST':
        cons.delete()
        return redirect('Cons_list')
    return render(request, 'constantes/cons_delete.html', {'cons':cons})

# ----------------------------------------------------- VISTAS PARA ARTICULOS ----------------------------------------------
    
def insum_create(request):

    #Si el metodo es POST activa la funciones para guardar los datos del formulario

    if request.method == 'POST':

        #Aqui guardo los datos para ingresar el formulario

        form = ArticulosForm(request.POST)

        #Aqui guardo los datos de los inputs

        datos = request.POST.items()

        for key, value in datos:

            if key == 'codigo':

                #Aqui solamente me quedo con el codigo
                codigo = (value)

            if key == 'constante':

                #Aqui solamente me quedo con el codigo
                constante = (value)

            if key == 'valor':

                #Aqui solamente me quedo con el codigo
                valor = (value)

        #Aqui pruebo si el formulario es correcto

        if form.is_valid():
            
            form.save()
        
        #Me conecto a la base de datos y traigo el valor de la constante

        objetos_constante = Constantes.objects.all()

        for i in objetos_constante:

            if float(i.id) == float(constante):

                valor_constante = float(i.valor)

                #Opero para sacar el valor auxiliar 

                valor_aux = (float(valor)/valor_constante)

                objetos_insumos = Articulos.objects.all()

                for i in objetos_insumos:

                    if int(i.codigo) == int(codigo):

                        i.valor_aux = valor_aux

                        print(i.valor_aux)

                        i.save()

                        return redirect('Lista de insumos')
         
    else:
        form = ArticulosForm()

    f = {'form':form}


    return render(request, 'articulos/insum_create.html', f )

# VISTA --> LISTADO DE ARTICULOS

def insum_list(request):

    art_actuales = Articulos.objects.all()

    myfilter = ArticulosFilter(request.GET, queryset=art_actuales)

    art_actuales = myfilter.qs

    c = {'articulos':art_actuales, 'myfilter':myfilter}

    return render(request, 'articulos/insum_list.html', c )

# VISTA -- > EDITAR ARTICULOS "TODAVIA NO LO VI"

def insum_edit(request, id_articulos):

    art = Articulos.objects.get(codigo=id_articulos)

    if request.method == 'GET':
        form = ArticulosForm(instance = art)
    else:
        form = ArticulosForm(request.POST, instance = art)
        if form.is_valid():
            form.save()
        return redirect('Lista de insumos')

    return render(request, 'articulos/insum_create.html', {'form':form})

def insum_delete(request, id_articulos):

    art = Articulos.objects.get(codigo=id_articulos)

    if request.method == 'POST':
        art.delete()
        return redirect('Lista de insumos')

    return render(request, 'articulos/insum_delete.html', {'art':art})




