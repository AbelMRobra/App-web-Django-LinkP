from django.shortcuts import render, redirect
from django.http import HttpResponse
from .filters import ArticulosFilter
from .form import ConsForm, ArticulosForm
from proyectos.models import Proyectos
from computos.models import Computos
from compras.models import Compras
from .models import Articulos, Constantes, DatosProyectos, Prametros, Desde, Analisis, CompoAnalisis, Modelopresupuesto, Capitulos
import sqlite3



# ----------------------------------------------------- VISTAS PARA PANEL PRESUPUESTOS - EXPLOSION ----------------------------------------------
def explosion(request, id_proyecto):

    proyecto = Proyectos.objects.get(id = id_proyecto)
    articulos = Articulos.objects.all()
    analisis = Analisis.objects.all()
    modelo = Modelopresupuesto.objects.all()
    compo = CompoAnalisis.objects.all()
    computo = Computos.objects.all()

    crudo = []

    # AQUI VEMOS LA CANTIDAD DE ANALISIS Y LO SUMAMOS A UN CRUDO

    for i in analisis:

        nombre_analisis = i
        cantidad_analisis = 0

        for d in modelo:

            if d.analisis == i:

                if d.cantidad == None:

                    if "SOLO MANO DE OBRA" in str(d.analisis):

                        for h in computo:
                            if h.proyecto == proyecto and h.tipologia == d.vinculacion:
                                cantidad_analisis = cantidad_analisis + h.valor_vacio  


                    else:

                        for h in computo:
                            if h.proyecto == proyecto and h.tipologia == d.vinculacion:
                                cantidad_analisis = cantidad_analisis + h.valor_lleno                 
                else:                            

                    cantidad_analisis = cantidad_analisis + d.cantidad
        
        crudo.append((i, cantidad_analisis))

    #USANDO LA CANTIDAD DE ANALISIS, VEMOS LA CANTIDAD DE ARTICULOS Y LO SUMAMOS A UN CRUDO

    crudo_articulo = []

    for c in articulos:

        nombre_articulo = c.nombre
        cantidad_articulo = 0
        valor_articulo = c.valor
        
        for j in crudo:

            for t in compo:

                if t.analisis == j[0] and t.articulo == c:

                    cantidad_articulo = cantidad_articulo + t.cantidad*j[1]

        saldo_articulo = cantidad_articulo*valor_articulo

        crudo_articulo.append((nombre_articulo, cantidad_articulo, valor_articulo, saldo_articulo))

    datos = []

    for u in crudo_articulo:
        if u[1] != 0:
            datos.append(u)

    compras = Compras.objects.all()

    datos_viejos = datos
    datos = []

    for i in datos_viejos:
        comprado = 0
        for c in compras:
            if c.proyecto == proyecto and c.articulo.nombre == i[0]:
                comprado = comprado + c.cantidad
        
        cantidad_saldo = i[1] - comprado

        saldo = cantidad_saldo * i[2]
        
        datos.append((i[0], i[1], i[2], comprado, cantidad_saldo, saldo ))

          #Aqui empieza el filtro

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        datos_viejos = datos

        datos = []   

        for i in palabra_buscar:

            if i[0] == "palabra":
        
                palabra_buscar = i[1]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                buscador = (str(i[0]))

                if palabra.lower() in buscador.lower():

                    datos.append(i)


    #Aqui termina el filtro

    datos = {"datos":datos,
    "proyecto":proyecto}


    return render(request, 'presupuestos/explosion.html', {"datos":datos})



# ----------------------------------------------------- VISTAS PARA PANEL PRESUPUESTOS - ANALISIS ----------------------------------------------
def presupuestosanalisis(request, id_proyecto, id_capitulo):

    proyecto = Proyectos.objects.get(id = id_proyecto)
    capitulo = Capitulos.objects.get(id = id_capitulo)
    compo = CompoAnalisis.objects.all()
    computo = Computos.objects.all()
    modelo = Modelopresupuesto.objects.all()

    crudo = []

    valor_capitulo = 0

    for d in modelo:

        if d.capitulo == capitulo and d.proyecto == proyecto:

            if d.cantidad == None:

                if "SOLO MANO DE OBRA" in str(d.analisis):

                    valor_analisis = 0

                    for e in compo:

                        if e.analisis == d.analisis:

                            valor_analisis = valor_analisis + e.articulo.valor*e.cantidad

                    cantidad = 0

                    for h in computo:
                        if h.proyecto == proyecto and h.tipologia == d.vinculacion:
                            cantidad = cantidad + h.valor_vacio  

                    total_parcial = valor_analisis*cantidad/1000
                    crudo.append((d.analisis, valor_analisis, cantidad, total_parcial, 0.0)) 

                    valor_capitulo = valor_capitulo + valor_analisis*cantidad

                else:
                    valor_analisis = 0

                    for e in compo:

                        if e.analisis == d.analisis:

                            valor_analisis = valor_analisis + e.articulo.valor*e.cantidad

                    cantidad = 0

                    for h in computo:
                        if h.proyecto == proyecto and h.tipologia == d.vinculacion:
                            cantidad = cantidad + h.valor_lleno 

                    total_parcial = valor_analisis*cantidad/1000
                    crudo.append((d.analisis, valor_analisis, cantidad, total_parcial, 0.0, d.vinculacion)) 

                    valor_capitulo = valor_capitulo + valor_analisis*cantidad
            else:

                valor_analisis = 0

                for e in compo:

                    if e.analisis == d.analisis:

                        valor_analisis = valor_analisis + e.articulo.valor*e.cantidad
                
                total_parcial = valor_analisis*float(d.cantidad)/1000
                
                crudo.append((d.analisis, valor_analisis, d.cantidad, total_parcial, 0.0, d.vinculacion))
                
                valor_capitulo = valor_capitulo + valor_analisis*float(d.cantidad)

    datos =[]

    for i in crudo:
        i = list(i)
        i[4] = i[3]/valor_capitulo*100000
        i = tuple(i)
        datos.append(i)



    datos = {"datos":datos, "proyecto":proyecto, "capitulo":capitulo}

    return render(request, 'presupuestos/presupuestoanalisis.html', {"datos":datos})


# ----------------------------------------------------- VISTAS PARA PANEL PRESUPUESTOS - CAPITULO ----------------------------------------------
def presupuestoscapitulo(request, id_proyecto):
    proyecto = Proyectos.objects.get(id = id_proyecto)
    capitulo = Capitulos.objects.all()
    compo = CompoAnalisis.objects.all()
    computo = Computos.objects.all()
    modelo = Modelopresupuesto.objects.all()

    crudo = []

    valor_proyecto = 0

    for c in capitulo:

        valor_capitulo = 0

        for d in modelo:

            if d.capitulo == c and d.proyecto == proyecto:

                if d.cantidad == None:

                    if "SOLO MANO DE OBRA" in str(d.analisis):

                        valor_analisis = 0

                        for e in compo:

                            if e.analisis == d.analisis:

                                valor_analisis = valor_analisis + e.articulo.valor*e.cantidad/1000000

                        cantidad = 0

                        for h in computo:
                            if h.proyecto == proyecto and h.tipologia == d.vinculacion:
                                cantidad = cantidad + h.valor_vacio   

                        valor_capitulo = valor_capitulo + valor_analisis*cantidad

                    else:
                        valor_analisis = 0

                        for e in compo:

                            if e.analisis == d.analisis:

                                valor_analisis = valor_analisis + e.articulo.valor*e.cantidad/1000000

                        cantidad = 0

                        for h in computo:
                            if h.proyecto == proyecto and h.tipologia == d.vinculacion:
                                cantidad = cantidad + h.valor_lleno  

                        valor_capitulo = valor_capitulo + valor_analisis*cantidad
    
                else:

                    valor_analisis = 0

                    for e in compo:

                        if e.analisis == d.analisis:

                            valor_analisis = valor_analisis + e.articulo.valor*e.cantidad/1000000

                    valor_capitulo = valor_capitulo + valor_analisis*float(d.cantidad)

        valor_proyecto = valor_proyecto + valor_capitulo
        
        crudo.append((c, valor_capitulo, 0.0))

    datos =[]

    for i in crudo:
        i = list(i)
        i[2] = i[1]/valor_proyecto*100
        i = tuple(i)
        datos.append(i)

    valor_proyecto_completo = valor_proyecto*1000000

    datos = {"datos":datos, "proyecto":proyecto, "valor_proyecto":valor_proyecto,"valor_proyecto_completo":valor_proyecto_completo}

    return render(request, 'presupuestos/presupuestocapitulo.html', {"datos":datos})

# ----------------------------------------------------- VISTAS PARA PANEL PRESUPUESTOS----------------------------------------------

def presupuestostotal(request):
    proyecto = Proyectos.objects.all()
    capitulo = Capitulos.objects.all()
    compo = CompoAnalisis.objects.all()
    computo = Computos.objects.all()
    modelo = Modelopresupuesto.objects.all()

    datos = []

    for i in proyecto:

        valor_proyecto = 0

        for c in capitulo:

            valor_capitulo = 0

            for d in modelo:

                if d.capitulo == c and d.proyecto == i:

                    if d.cantidad == None:

                        if "SOLO MANO DE OBRA" in str(d.analisis):

                            valor_analisis = 0

                            for e in compo:

                                if e.analisis == d.analisis:

                                    valor_analisis = valor_analisis + e.articulo.valor*e.cantidad

                            cantidad = 0

                            for h in computo:
                                if h.proyecto == i and h.tipologia == d.vinculacion:
                                    cantidad = cantidad + h.valor_vacio   

                            valor_capitulo = valor_capitulo + valor_analisis*cantidad

                        else:
                            valor_analisis = 0

                            for e in compo:

                                if e.analisis == d.analisis:

                                    valor_analisis = valor_analisis + e.articulo.valor*e.cantidad

                            cantidad = 0

                            for h in computo:
                                if h.proyecto == i and h.tipologia == d.vinculacion:
                                    cantidad = cantidad + h.valor_lleno  

                            valor_capitulo = valor_capitulo + valor_analisis*cantidad

                    else:

                        valor_analisis = 0

                        for e in compo:

                            if e.analisis == d.analisis:

                                valor_analisis = valor_analisis + e.articulo.valor*e.cantidad

                        valor_capitulo = valor_capitulo + valor_analisis*float(d.cantidad)

        
            valor_proyecto = valor_proyecto + valor_capitulo/1000000
        
        datos.append((i, valor_proyecto))
      

    return render(request, 'presupuestos/principalpresupuesto.html', {"datos":datos})



# ----------------------------------------------------- VISTAS PARA VER ANALISIS----------------------------------------------

def ver_analisis(request, id_analisis):

    analisis = Analisis.objects.get(codigo = id_analisis)
    composi = CompoAnalisis.objects.all()
    lista_compo = []

    for i in composi:
        if i.analisis == analisis:
            lista_compo.append(i)

    total = 0

    for c in lista_compo:
        total = total + c.articulo.valor*c.cantidad

    lista_final = []

    for d in lista_compo:
        total_renglon = d.cantidad*d.articulo.valor
        inc = (total_renglon/total)*100
        lista_final.append((d, total_renglon, inc))

    datos = {"analisis":analisis, "lista_final":lista_final, "total":total}

    
    return render(request, 'analisis/veranalisis.html', {"datos":datos})


# ----------------------------------------------------- VISTAS PARA LISTAR ANALISIS----------------------------------------------

def analisis_list(request):

    analisis = Analisis.objects.all()
    composicion = CompoAnalisis.objects.all()
    datos = []

    for i in analisis:

        valor = 0

        for c in composicion:

            if i == c.analisis:
                valor = valor +c.articulo.valor*c.cantidad

        datos.append((i, valor))

        #Aqui empieza el filtro

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        datos_viejos = datos

        datos = []   

        for i in palabra_buscar:

            if i[0] == "palabra":
        
                palabra_buscar = i[1]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                buscador = (str(i[0].nombre)+str(i[0].codigo))

                if palabra.lower() in buscador.lower():

                    datos.append(i)


    #Aqui termina el filtro

    return render(request, 'analisis/listaanalisis.html', {"datos":datos})

# ----------------------------------------------------- VISTAS PARA PANEL DE ANALISIS----------------------------------------------

def panelanalisis(request):

    analisis = Analisis.objects.all()
    composicion = CompoAnalisis.objects.all()
    datos = []

    for i in analisis:

        valor = 0

        for c in composicion:

            if i == c.analisis:
                valor = valor +c.articulo.valor*c.cantidad

        datos.append((i, valor))

            #Aqui empieza el filtro

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        datos_viejos = datos

        datos = []   

        for i in palabra_buscar:

            if i[0] == "palabra":
        
                palabra_buscar = i[1]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                buscador = (str(i[0].nombre)+str(i[0].codigo))

                if palabra.lower() in buscador.lower():

                    datos.append(i)


    #Aqui termina el filtro

    return render(request, 'analisis/panelanalisis.html', {"datos":datos})
    
# ----------------------------------------------------- VISTAS PARA CREAR ANALISIS ----------------------------------------------

def crearanalisis(request):

    articulos = Articulos.objects.all()

    mensaje = ""

    datos = {'articulos':articulos}

    if request.method == 'POST':

        datos_p = request.POST.items()

        resto = []

        for i in datos_p:

            if i[0] == "codigo":
                
                codigo = i[1]

            elif i[0] == "nombre":
                
                nombre = i[1]

            elif i[0] == "unidad":
                
                unidad = i[1]
            
            else:

                resto.append(i)        

        datos_analisis = Analisis.objects.all()
        id_analisis = []

        for i in datos_analisis:
            id_analisis.append(i.id)
            
        id_num = 1

        while id_num in id_analisis:
            id_num = id_num + 1

        try:

            b = Analisis(
                id = id_num,
                codigo = codigo,
                nombre = nombre,
                unidad = unidad,
                )

            b.save()

        except:

            mensaje = "El analisis cargado tiene un error"

            datos = {'articulos':articulos, 'mensaje':mensaje}

        valor = 1

        for i in resto:

            try:

                if i[0] == "csrfmiddlewaretoken":

                    print("Basura")

                elif valor == 1:

                    valor = 2
    
                    nombre_articulo = i[1]

                elif valor == 2:

                    valor = 1

                    cantidad = i[1]

                    datos_compo = CompoAnalisis.objects.all()
                    
                    id_compo = []

                    for i in datos_compo:
                        id_compo.append(i.id)
                        
                    id_num_compo = 1

                    while id_num_compo in id_compo:
                        print("Si esta")
                        id_num_compo = id_num_compo + 1
            
                    b = CompoAnalisis(
                        id = id_num_compo,
                        articulo = Articulos.objects.get(nombre=nombre_articulo),
                        analisis = Analisis.objects.get(codigo=codigo),
                        cantidad = cantidad,
                    )

                    b.save()
           
            except:

                mensaje = "**Los datos ingresados no son correctos"

                datos = {'articulos':articulos, 'mensaje':mensaje}

        return redirect('Lista de analisis')
    else:

        datos = {'articulos':articulos,}


    return render(request, 'analisis/crearanalisis.html', {'datos':datos})

# ----------------------------------------------------- VISTAS PARA MODIFICAR ANALISIS ----------------------------------------------

def modificaranalisis(request, id_analisis):

    analisis = Analisis.objects.get(codigo = id_analisis)
    articulos = Articulos.objects.all()
    compo = CompoAnalisis.objects.all()

    datos = []

    for i in compo:

        if i.analisis == analisis:

            datos.append((i.articulo, i.cantidad, i.id))
    

    datos = {"analisis":analisis,
    "articulos":articulos,
    "datos":datos}

    return render(request, 'analisis/modificaranalisis.html', {"datos":datos})



# ----------------------------------------------------- VISTAS PARA PARAMETROS----------------------------------------------

def parametros(request):

    datos = Prametros.objects.all()

    return render(request, 'desde/parametros.html', {'datos': datos})

# ----------------------------------------------------- VISTAS PARA INDICADOR DE PRECIOS----------------------------------------------

def desde(request):

    datos = Desde.objects.all()

    constantes = Constantes.objects.all()

    usd_blue = Constantes.objects.get(nombre = "USD_BLUE")

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

            if str(c.nombre) == 'USD_BLUE':

                valor_costo_usd = valor_costo/c.valor

                valor_final_usd = valor_final/c.valor

        i.valor_costo = valor_costo
        i.valor_costo_usd = valor_costo_usd
        i.valor_final = valor_final
        i.valor_final_usd = valor_final_usd

        i.save()

    

    datos = {'datos':datos, 'usd_blue':usd_blue}

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
        return redirect('Cons_panel')
        
    else:
        form = ConsForm()

    f = {'form':form}
    return render(request, 'constantes/cons_create.html', f )

# ----------------------------------------------------- VISTAS PARA PANEL DE CAMBIOS CONSTANTES ----------------------------------------------

def cons_list(request):

    cons_actuales = Constantes.objects.all()

    c = {'constantes':cons_actuales}

    return render(request, 'constantes/cons_list.html', c )

def cons_panel(request):

    cons_actuales = Constantes.objects.all()

    c = {'constantes':cons_actuales}

    return render(request, 'constantes/cons_panel.html', c )

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

                    form.save()

            datos_insumos = Articulos.objects.all()

            for i in datos_insumos:

                if str(i.constante) == str(cons_nombre):
                    valor_actual = i.valor

                    valor_nuevo = valor_actual*(float(cons_valor_nuevo)/cons_valor) 

                    i.valor = valor_nuevo

                    i.save()

        return redirect('Cons_panel')
    
    return render(request, 'constantes/cons_create.html', {'form':form})

# VISTA --> Eliminar constantes

def cons_delete(request, id_cons):

    cons = Constantes.objects.get(id=id_cons)

    if request.method == 'POST':
        cons.delete()
        return redirect('Cons_panel')
    return render(request, 'constantes/cons_delete.html', {'cons':cons})

# ----------------------------------------------------- VISTAS PARA ARTICULOS ----------------------------------------------
    
def insum_create(request):

    #Si el metodo es POST activa la funciones para guardar los datos del formulario

    mensaje = ""

    if request.method == 'POST':

        try:

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

                            i.save()

                            return redirect('Panel de cambios')
        except:

             mensaje = "Hay un error al cargar, cuidado con los puntos y comas"   
    else:
        form = ArticulosForm()

    f = {'form':form, 'mensaje':mensaje}

    return render(request, 'articulos/insum_create.html', f )

# VISTA --> LISTADO DE ARTICULOS/ PANEL DE CAMBIOS

def insum_panel(request):

    art_actuales = Articulos.objects.all()

    myfilter = ArticulosFilter(request.GET, queryset=art_actuales)

    art_actuales = myfilter.qs

    c = {'articulos':art_actuales, 'myfilter':myfilter}

    return render(request, 'articulos/insum_panel.html', c )

def insum_list(request):

    datos = Articulos.objects.all()

    #Aqui empieza el filtro

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        datos_viejos = datos

        datos = []   

        for i in palabra_buscar:

            if i[0] == "palabra":
        
                palabra_buscar = i[1]

        if str(palabra_buscar) == "":

            datos = datos_viejos

        else:
        
            for i in datos_viejos:

                palabra =(str(palabra_buscar))

                codigo = (str(i.codigo))

                nombre = (str(i.nombre))

                constante = (str(i.constante))

                valor = (str(i.valor))


                if palabra.lower() in codigo.lower() or palabra.lower() in nombre.lower() or palabra.lower() in constante.lower() or palabra.lower() in valor.lower():

                    datos.append(i)


    #Aqui termina el filtro

    c = {'datos':datos}

    return render(request, 'articulos/insum_list.html', c )

# VISTA -- > EDITAR ARTICULOS 

def insum_edit(request, id_articulos):

    art = Articulos.objects.get(codigo=id_articulos)

    if request.method == 'GET':
        form = ArticulosForm(instance = art)
    else:
        form = ArticulosForm(request.POST, instance = art)
        if form.is_valid():
            form.save()
        return redirect('Panel de cambios')

    return render(request, 'articulos/insum_create.html', {'form':form})

def insum_delete(request, id_articulos):

    art = Articulos.objects.get(codigo=id_articulos)

    if request.method == 'POST':
        art.delete()
        return redirect('Panel de cambios')

    return render(request, 'articulos/insum_delete.html', {'art':art})




