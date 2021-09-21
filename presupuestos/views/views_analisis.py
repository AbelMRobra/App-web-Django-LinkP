from django.shortcuts import render
from django.db.models import Max
from presupuestos.models import *
import numpy as np

def analisis_crear(request):

    articulos = Articulos.objects.all()

    mensaje = ""

    datos = {'articulos':articulos, "mensaje":mensaje}

    if request.method == 'POST':

        datos=request.POST.dict()
        compos=[]
        if 'crear-analisis' in datos:
            cant_compos=int(datos['contador']) + 1
            codigo_analisis=datos['codigo']
            nombre_analisis=datos['nombre']
            unidad_analisis=datos['unidad']

            if Analisis.objects.filter(codigo = codigo_analisis).count() > 0:
                mensaje = "Este codigo ya se encuentra en la base"
                datos = {'articulos':articulos, "mensaje":mensaje}

            else:

                ultimo_analisis=Analisis.objects.aggregate(max_id=Max('id'))
                id_ultimo=ultimo_analisis['max_id']
                if id_ultimo is None:
                    id_ultimo=0
                id_an=int(id_ultimo)+1

                analisis_=Analisis(
                    id=id_an,
                    codigo=codigo_analisis,
                    nombre=nombre_analisis,
                    unidad=unidad_analisis,
                )
                analisis_.save()

                aux=CompoAnalisis.objects.aggregate(max_id=Max('id'))
                id_compo_ultimo=aux['max_id']
                if id_compo_ultimo is None:
                    id_compo_ultimo=0
                id_compo=id_compo_ultimo + 1
                if analisis_:
                    for i in range(cant_compos):
                        
                        if i > 1 :
                            k_cant='cantidad'+str(i)
                            cant=datos[k_cant]
                            k_articulo='articulo'+str(i)
                            art=datos[k_articulo]
                            articulo=Articulos.objects.get(nombre=art)
                            compo=CompoAnalisis(id=id_compo,analisis=analisis_,articulo=articulo, cantidad=cant,)
                            compos.append(compo)
                            id_compo += 1
                    

                        elif i==0:
                            cant=datos['cantidad']
                            art=datos['articulo']

                            articulo=Articulos.objects.get(nombre=art)
                            compo=CompoAnalisis(id=id_compo,analisis=analisis_,articulo=articulo, cantidad=cant,)
                            compos.append(compo)
                            id_compo += 1
                            

                    CompoAnalisis.objects.bulk_create(compos)

                    datos = {'articulos':articulos, "mensaje":mensaje}


    return render(request, 'analisis/analisis_crear.html', {'datos':datos})


def analisis_individual_ver(request, id_analisis):

    analisis = Analisis.objects.get(codigo = id_analisis)
    composi = CompoAnalisis.objects.filter(analisis = analisis)
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

    
    return render(request, 'analisis/analisis_ver.html', {"datos":datos})


def analisis_lista(request):

    analisis = Analisis.objects.all()

 
    con_compo=CompoAnalisis.objects.all()
 
    datos = [(i, sum(np.array(con_compo.filter(analisis = i).values_list('articulo__valor',flat=True))
    
                * np.array(con_compo.filter(analisis = i).values_list('cantidad',flat=True)))) for i in analisis]
    
    
    return render(request, 'analisis/analisis_lista.html', {"datos":datos})



def analisis_modificar(request, id_analisis):

    analisis = Analisis.objects.get(codigo = id_analisis)
    articulos = Articulos.objects.all()
    compo = CompoAnalisis.objects.all()

    datos = []

    datos=[(i.articulo, i.cantidad, i.id) for i in compo if i.analisis == analisis]

    datos = {"analisis":analisis,
    "articulos":articulos,
    "datos":datos}

    return render(request, 'analisis/analisis_modificar.html', {"datos":datos})

def analisis_panel(request):

    analisis = Analisis.objects.all()

    con_compo=CompoAnalisis.objects.all()

  
    datos = [(i, sum(np.array(con_compo.filter(analisis = i).values_list('articulo__valor',flat=True))
    
                * np.array(con_compo.filter(analisis = i).values_list('cantidad',flat=True)))) for i in analisis]
    

    return render(request, 'analisis/analisis_panel.html', {"datos":datos})


