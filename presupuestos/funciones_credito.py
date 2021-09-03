import numpy as np
from .models import CompoAnalisis, Modelopresupuesto, Analisis, Articulos


def ajustar_analisis(proyecto, cantidad_sobrante, codigo_analisis, codigo_articulo):
    
    # DEFINICION DE VARIABLES INICIALES

    analisis = Analisis.objects.get(codigo=codigo_analisis)
    articulo = Articulos.objects.get(codigo=codigo_articulo)

    composicion_analisis=CompoAnalisis.objects.filter(analisis=analisis ,articulo=articulo)
    
    modelo_presup=Modelopresupuesto.objects.filter(proyecto = proyecto, analisis=analisis).values_list("cantidad", flat=True)

    # -> En este punto tenemos como el articulo esta dentro del analisis
    # -> Como esta ese analisis dentro del proyecto

    # AJUSTE DEL ANALISIS
    
    cantidad_analisis=sum(np.array(modelo_presup))

    necidad_articulo = cantidad_analisis

    if necidad_articulo == 0:

        ajuste = -float(cantidad_sobrante)

    else:

        ajuste = -float(cantidad_sobrante)/necidad_articulo


    if composicion_analisis.count() == 0:
        composicion_nueva = CompoAnalisis(
            articulo = articulo,
            analisis = analisis,
            cantidad = ajuste,
        )

        composicion_nueva.save()

    else:

        composicion_ajustar = CompoAnalisis.objects.get(id = composicion_analisis[0].id)
        composicion_ajustar.cantidad +=ajuste
        composicion_ajustar.save()

    # -> En este punto se ajusto esa cantidad en todo el proyecto

    return f'El {analisis} fue modificado con un ajuste de {ajuste}, cantidad de analisis dentro del proyecto {len(modelo_presup)}'


def ajustar_capitulo():

    pass
def ajustar_todo():

    pass

'''

if request.method=='POST':
        datos=request.POST.dict()
        cantidad_sobrante=float(datos['sobrante'])
        
        #EN ESTE ESCENARIO SE MODIFICA LA CANTIDAD DEL ANALISIS DE CADA ARTICULO -> la cantidad en el modelo composicion
        
        
        #EN ESTE ESCENARIO SE MODIFICA UN CAPITULO COMPLETO , ES DECIR AFECTARA TAMBIEN A LOS ANALISIS CONTENIDOS EN EL 

        if 'modificar-capitulo' in datos:
            codigo=int(datos['modificar-capitulo']) #codigo del articulo
            codigo_capitulo=int(datos['capitulo'])

            #SE OBTIENE LA CANTIDAD NECESARIA
            modelo_presup=Modelopresupuesto.objects.get(capitulo__id=codigo_capitulo)

            #SE OBTIENE LA CANTIDAD DEL ARTICULO EN EL ANALISIS
            compo=CompoAnalisis.objects.get(analisis__codigo=modelo_presup.analisis.codigo)
            cant_compo=compo.cantidad

            #SE CALCULA LA CANTIDAD EXTRA QUE ES EL RESULTADO DE DIVIDIR EL SOBRANTE SOBRE LA CANTIDAD NECESARIA EN EL ANALISIS 
            cant_nec=modelo_presup.cantidad
            cant_extra=cantidad_sobrante/cant_compo

            #SE SUMA LA CANTIDAD EXTRA A LA CANTIDAD NECESARIA EN EL CAPITULO
            modelo_presup.cantidad=cant_nec + cant_extra
            modelo_presup.save()

        if 'crear' in datos:
            codigo_articulo=int(datos['crear'])
            codigo_analisis=int(datos['codigo-analisis'])
            nombre_analisis=datos['nombre-analisis']
            nuevo_capitulo=datos['nombre-capitulo']
            nombre_capitulo=datos['capitulo']
            unidad_analisis=datos['unidad-analisis']

            
                

            art=Articulos.objects.get(codigo=codigo_articulo)

            max_id_an= Analisis.objects.aggregate(max_id=Max('id'))['max_id']

            max_id_compo= CompoAnalisis.objects.aggregate(max_id=Max('id'))['max_id']

            analisis=Analisis(
                id=max_id_an + 1,
                codigo=codigo_analisis,
                nombre=nombre_analisis,
                unidad=unidad_analisis,

            )
            analisis.save()

            compo=CompoAnalisis(
                id=max_id_compo + 1,
                articulo=art,
                analisis=analisis,
                cantidad=cantidad_sobrante, #calcular
                

            )
            if 'nombre-capitulo'!='':

                capitulo=Capitulos(
                    nombre=nuevo_capitulo,
                    descripcion='',

                )
                capitulo.save()

                modelopresup=Modelopresupuesto(
                    proyecto=Proyectos.objects.get(pk=id_proyecto),
                    capitulo=capitulo,
                    analisis=analisis,
                    cantidad= 1,

                )
                modelopresup.save()
            else:
                cap=Modelopresupuesto.objects.get(capitulo__nombre=nombre_capitulo)
'''