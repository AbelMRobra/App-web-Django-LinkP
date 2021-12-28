import numpy as np
from proyectos.models import Proyectos
from computos.models import Computos
from presupuestos.models import Analisis, CompoAnalisis, Modelopresupuesto,Capitulos, Presupuestos


def presupuestos_modificar_estado(proyecto, estado):
    
    if estado == "EXTRAPOLADO":
        proyecto.presupuesto = estado
        proyecto.save()
    elif estado == "ACTIVO" or estado == "BASE":
        proyecto.presupuesto = estado
        proyecto.save()
        presupuesto = Presupuestos.objects.get(proyecto = proyecto)
        presupuesto.proyecto_base = None
        presupuesto.save()
    else:
        pass
    return "Success"

def datos_modelo(id_modelo):

    modelo = Modelopresupuesto.objects.get(id = id_modelo)
    datos = {
        'id': modelo.id,
        'analisis': f'{modelo.analisis.codigo}-{modelo.analisis.nombre}',
 
        'comentario': modelo.comentario,
        'orden': modelo.orden,
        'cantidad': modelo.cantidad
    }
    return datos

def presupuesto_afectados(id_modelo):

    modelo = Modelopresupuesto.objects.get(id = id_modelo)
    modelos = Modelopresupuesto.objects.filter(analisis = modelo.analisis).values_list("proyecto__nombre", flat=True).distinct()
    datos = [{'nombre': nombre} for nombre in modelos]
    return datos

def presupuesto_capitulo(id_proyecto):

    capitulos = Capitulos.objects.all() 
    modelos = Modelopresupuesto.objects.all()
    analisis = Analisis.objects.all()
    compo_analisis = CompoAnalisis.objects.all()

    datos = []

    for capitulo in capitulos:

        valor_capitulo = 0
        modelos_afectados = modelos.filter(capitulo = capitulo)
        datos.append({
            'id': capitulo.id,
            'nombre': capitulo.nombre.lower().capitalize(),
            'valor': valor_capitulo
        })
    return datos


def presupuesto_capitulo_detalle(id_proyecto, id_capitulo):


    modelos = Modelopresupuesto.objects.filter(proyecto__id = id_proyecto, capitulo = id_capitulo).order_by('orden')
    compo_analisis = CompoAnalisis.objects.all()
    datos = []

    for modelo in modelos:

        array_precios = np.array(compo_analisis.filter(analisis = modelo.analisis).values_list("articulo__valor", flat=True))
        array_cantidades = np.array(compo_analisis.filter(analisis = modelo.analisis).values_list("cantidad", flat=True))
        valor_analisis = sum(array_precios*array_cantidades)
        if modelo.comentario:
            comentario = modelo.comentario.lower().capitalize()
        else:
            comentario = "Sin comentario"
        datos.append({
            'id': modelo.id,
            'orden': modelo.orden,
            'nombre': modelo.analisis.nombre.lower().capitalize(),
            'unidad': modelo.analisis.unidad,
            'comentario': comentario,
            'valor': round(valor_analisis, 2),
            'cantidad': modelo.cantidad,
            'valor_analisis': round((modelo.cantidad*valor_analisis), 2)
        })
    return datos


def PresupuestoPorCapitulo(id_proyecto):


    #Modelos que seran necesarios recorrer completos

    proyecto = Proyectos.objects.get(id = id_proyecto)
    capitulo = Capitulos.objects.all()    

    #La lista datos tiene que tener 37 Arrays por cada capitulo

    datos = []
    
    # Vamos a recorrer todos los capitulos y armar una array

    numero_capitulo = 1
    
    for cap in capitulo:

        capitulo = [] 

        modelo = Modelopresupuesto.objects.filter(proyecto = proyecto, capitulo = cap)

        for mod in modelo:

                if mod.cantidad == None:

                    if "SOLO MANO DE OBRA" in str(mod.analisis):

                        computo = Computos.objects.filter(proyecto = proyecto, tipologia = mod.vinculacion)

                        cantidad_computo = 0

                        for comp in computo:

                            cantidad_computo = cantidad_computo + comp.valor_vacio

                        articulos_analisis = CompoAnalisis.objects.filter(analisis = mod.analisis)

                        for compo in articulos_analisis:

                            articulo_cantidad = (compo.articulo, compo.cantidad*cantidad_computo)

                            capitulo.append(articulo_cantidad)


                    else:

                        computo = Computos.objects.filter(proyecto = proyecto, tipologia = mod.vinculacion)

                        cantidad_computo = 0

                        for comp in computo:

                            cantidad_computo = cantidad_computo + comp.valor_lleno

                        articulos_analisis = CompoAnalisis.objects.filter(analisis = mod.analisis)

                        for compo in articulos_analisis:

                            articulo_cantidad = (compo.articulo, compo.cantidad*cantidad_computo)

                            capitulo.append(articulo_cantidad)

    
                else:

                    articulos_analisis = CompoAnalisis.objects.filter(analisis = mod.analisis)

                    for compo in articulos_analisis:

                        articulo_cantidad = (compo.articulo, compo.cantidad*mod.cantidad )

                        capitulo.append(articulo_cantidad)

        datos.append((numero_capitulo, cap, capitulo))

        numero_capitulo += 1


    #Devuelve el numero del capitulo, el nombre y una lista de todos los insumos y la cantidad de cada uno             

    return datos


