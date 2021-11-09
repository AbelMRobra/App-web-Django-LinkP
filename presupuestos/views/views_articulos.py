from django.shortcuts import render, redirect
from presupuestos.models import Articulos, Constantes
from presupuestos.filters import ArticulosFilter
from presupuestos.form import ArticulosForm

def articulos_listado_maestro(request):

    datos = Articulos.objects.all()

    context = {'datos':datos}

    return render(request, 'articulos/insum_list.html', context )

def articulos_listado_general(request):

    art_actuales = Articulos.objects.all()

    myfilter = ArticulosFilter(request.GET, queryset=art_actuales)

    art_actuales = myfilter.qs

    c = {'articulos':art_actuales, 'myfilter':myfilter}

    return render(request, 'articulos/insum_panel.html', c )
  
def articulos_crear(request):

    context = {}

    if request.method == 'POST':

        try:

            form = ArticulosForm(request.POST)
            datos = request.POST.items()

            for key, value in datos:

                if key == 'codigo':
                    codigo = (value)

                if key == 'constante':
                    constante = (value)

                if key == 'valor':
                    valor = (value)

            if form.is_valid():
                form.save()
            
            objetos_constante = Constantes.objects.all()

            for i in objetos_constante:

                if float(i.id) == float(constante):
                    valor_constante = float(i.valor)
                    valor_aux = (float(valor)/valor_constante)
                    objetos_insumos = Articulos.objects.all()

                    for i in objetos_insumos:

                        if int(i.codigo) == int(codigo):
                            i.valor_aux = valor_aux
                            i.save()
                            
                            context['mensaje'] = [1, "Articulo creado correctamente!"] 
        except:
            context['mensaje'] = [0, "Error en los datos"]  
    
    else:
        
        form = ArticulosForm()

    context['form'] = form

    return render(request, 'articulos/insum_create.html', context)

def articulos_editar(request, id_articulos):

    context = {}
    context['mensaje'] = 'no'

    art = Articulos.objects.get(codigo=id_articulos)

    if request.method == 'GET':
        form = ArticulosForm(instance = art)
    else:
        form = ArticulosForm(request.POST, instance = art)
        if form.is_valid():
            form.save()
            context['mensaje'] = 'ok'
        else:
            context['mensaje'] = 'Hubo un error'


    context['form'] = form

    return render(request, 'articulos/insum_create.html', context)

def articulos_eliminar(request, id_articulos):

    art = Articulos.objects.get(codigo=id_articulos)

    if request.method == 'POST':
        art.delete()
        return redirect('Panel de cambios')

    return render(request, 'articulos/insum_delete.html', {'art':art})
