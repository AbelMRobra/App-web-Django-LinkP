import numpy as np

from django.db.models import Max


from presupuestos.models import CompoAnalisis, Modelopresupuesto, Analisis, Articulos,Capitulos



def get_capitulos_analisis(proyecto,datos):
    #NECESITO ENVIAR AL TEMPLATE LOS ANALISIS Y CAPITULOS RELACIONADOS A CADA ARTICULO PERTENECIENTE AL PROYECTO ACTUAL

    #PARA ELLO OBTENGO TODOS LOS A Y C DISTINTOS DEL PROYECTO 
    analisis_proyecto=Modelopresupuesto.objects.filter(proyecto__nombre=proyecto.nombre).values_list('analisis__nombre').distinct()
    capitulos_proyecto=Modelopresupuesto.objects.filter(proyecto__nombre=proyecto.nombre).values_list('capitulo__nombre').distinct()

    #OBTENGO LOS NOMBRES PARA PODER HACER EL FILTRO EN CADA ARTICULO MAS ABAJO
    nombres_analisis=[m[0] for m in analisis_proyecto]
    nombres_capitulos=[m[0] for m in capitulos_proyecto]

    nuevo_datos=[]

    #DATOS[0] -> explosion de insumos

    #EN ESTE BUCLE AGREGO EN CADA ITERACION(O EN CADA OBJETO) DOS LISTAS LAS CUALES CONTIENEN ANALISIS Y CAPITULOS POR CADA ARTICULOS
    #ITERO SOBRE DATOS[0] PERO CREO OTRO ARRAY(nuevos_datos=[]) IGUAL A DATOS[0] + LOS NUEVOS ARRAYS CON ANALISIS 
    for d in datos[0]:
        aux=None

        #NOMBRE DEL ARTICULO EN ESTA ITERACION
        nombre_art=d[0].nombre

        #SE OBTIENEN LOS ANALISIS RELACIONADOS CON EL ARTICULO. Puede o no tener.
        compos=CompoAnalisis.objects.filter(articulo__nombre__icontains=nombre_art)
        lista_analisis=[]
        lista_capitulos=[]

        #EN EL CASO DE QUE TENGA ANALISIS, SE RECORRERAN FILTRANDO SOLO LOS QUE PERTENEZCAN AL PROYECTO ACTUAL(el que viene por id en la view)
        #AQUI ES DONDE USO LOS NOMBRES DE LOS ANALISIS OBTENIDOS ARRIBA
        if compos.count() > 0:
            for i in compos:
                
                analisis=i.analisis.nombre
                #si el nombre del analisis esta en la lista de analisis del proyecto lo filtra entonces lo agrega al array 
                if analisis in nombres_analisis:
                    obj=Analisis.objects.filter(nombre=analisis)
                    #array de analisis pertencientes al proyecto para este articyulo
                    lista_analisis.append(obj)

                    #Agrego el array al objeto actual (d) pero antes lo convierto en una lista porque es una tupla
                    aux=list(d)
                    aux.append(lista_analisis)

                #si el nombre no esta entre los analisis de este proyecto agrega un array vacio
                else:
                    aux=list(d)
                    aux.append([])    
                
                #obtengo los capitulos a partir de los analisis del articulo
                modelos=Modelopresupuesto.objects.filter(analisis__nombre=analisis,proyecto__nombre=proyecto.nombre)
                lista_capitulos=[Capitulos.objects.get(pk=i.capitulo.id) for i in modelos]
                
                #si el nombre del capitulo pertence a los capitulos del proyecto en cuestion los agrego a la lista
            aux.append(lista_capitulos)

        #EN EL CASO DE QUE NO SE OBTENGAN ANALISIS, SE AGREGA UN ARRAY VACIO
        else:
            aux=list(d)
            aux.append([])
            aux.append([])
        

        #SE AGREGA EL NUEVO OBJETO AL NUEVO ARRAY. aux es equivalente a d , y nuevos_datos es equivalente a datos[0]   
        nuevo_datos.append(aux)

            
        capitulos_proyecto
    #igualo datos[0] a nuevos_datos para no tener que cambiar el resto del codigo
    datos[0]=nuevo_datos
    return datos

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
                                                            #toma el primer compo encontrado
        composicion_ajustar = CompoAnalisis.objects.get(id = composicion_analisis[0].id)
        composicion_ajustar.cantidad +=ajuste   #cantidad + ajuste
        composicion_ajustar.save()

    # -> En este punto se ajusto esa cantidad en todo el proyecto

    return f'El {analisis} fue modificado con un ajuste de {ajuste}, cantidad de analisis dentro del proyecto {len(modelo_presup)}'


def ajustar_capitulo(proyecto,cantidad_sobrante,capitulo,art):
    capitulos = Modelopresupuesto.objects.filter(proyecto=proyecto,capitulo__id=capitulo)
    
    articulo = Articulos.objects.get(id=int(art))

    #indirectamente ya estan relacionados el articulo con el capitulo elegido
    capitulos_cant=Modelopresupuesto.objects.filter(proyecto = proyecto, capitulo=capitulo).values_list("cantidad", flat=True)
    
    cantidad_analisis=sum(np.array(capitulos_cant))
    necidad_articulo = cantidad_analisis

    # AJUSTE DEL ANALISIS
    if necidad_articulo == 0:

        ajuste = -float(cantidad_sobrante)

    else:

        ajuste = -float(cantidad_sobrante)/necidad_articulo

    cap=Modelopresupuesto.objects.get(id=265)
    cap.cantidad += ajuste
    cap.save()

def ajustar_todo(proyecto,cantidad_sobrante,nombre_capitulo,nombre_na,codigo_na,unidad_na,codigo_articulo):

    articulo = Articulos.objects.get(codigo=int(codigo_articulo))
  
    if nombre_capitulo[1]:
        #si el capitulo es nuevo
        nuevo_capitulo=nombre_capitulo[0]

        capitulo=Capitulos(
            nombre=nuevo_capitulo,
            descrip='',
        )
        capitulo.save()

        max_id_a= Analisis.objects.aggregate(max_id=Max('id'))['max_id']
        analisis_=Analisis(
            id=max_id_a + 1,
            codigo=codigo_na,
            nombre=nombre_na,
            unidad=unidad_na,
            
        )
        analisis_.save()

        max_id_compo= CompoAnalisis.objects.aggregate(max_id=Max('id'))['max_id']
        compo=CompoAnalisis(
            id=max_id_compo+1,
            articulo=articulo,
            analisis=analisis_,
            cantidad=cantidad_sobrante,

        )
        compo.save()

        modelo=Modelopresupuesto(
            proyecto=proyecto,
            capitulo=capitulo,
            analisis=analisis_,
            cantidad=1,
        )
        modelo.save()

    else:
        #si el capitulo no es nuevo
        capitulo=nombre_capitulo[0]
        
        capitulos = Modelopresupuesto.objects.filter(proyecto=proyecto,capitulo__id=capitulo)
        
        analisis_=capitulos[0].analisis
        max_id_compo= CompoAnalisis.objects.aggregate(max_id=Max('id'))['max_id']

        nuevo_compo=CompoAnalisis(
            id=max_id_compo+1,
            articulo=articulo,
            analisis=analisis_,
            cantidad=int(cantidad_sobrante),
        )
        nuevo_compo.save()


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