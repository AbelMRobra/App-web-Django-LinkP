from django.shortcuts import render,redirect
from .models import Proyectos, Unidades, ProyectosTerceros
from ventas.models import VentasRealizadas
from django.db.models import Sum
# Create your views here.

def adminunidades(request):

    datos = Unidades.objects.filter(proyecto__id = 1)

    total_unidades = len(datos)

    datos_completo = []

    total_propia = 0
    total_balcon = 0
    total_patio = 0
    total_comun = 0
    total_total = 0

    for dato in datos:

        try:
            total_propia = total_propia + dato.sup_propia
            total_balcon = total_balcon + dato.sup_balcon
            total_patio = total_patio + dato.sup_patio
            total_comun = total_comun + dato.sup_comun


            sup_total = dato.sup_balcon + dato.sup_comun + dato.sup_propia + dato.sup_patio

            total_total = total_total + sup_total

            datos_completo.append((dato, sup_total))

        except:

            datos_completo.append((dato, "NO COMPLETO"))

    comun_total = (total_comun/total_total)*100




    return render(request, 'adminunidades.html', {'datos_completo':datos_completo, 'total_propia':total_propia, 'total_balcon':total_balcon, 'total_patio':total_patio, 'total_comun':total_comun, 'total_total':total_total,
     'total_unidades':total_unidades, 'comun_total':comun_total})

def proyectos(request):

    if request.method=='POST':

        try:

            id_proyecto = request.POST['id_proyecto']
            fecha_i=request.POST['fecha_i']
            fecha_i_contrato=request.POST['fecha_i_contrato']
            fecha_f=request.POST['fecha_f']
            fecha_f_contrato=request.POST['fecha_f_contrato']

            proyecto=Proyectos.objects.get(pk=id_proyecto)
                
            if fecha_i!='':
                proyecto.fecha_i= fecha_i
            if fecha_i_contrato!='':
                proyecto.fecha_i_contrato=  fecha_i_contrato
            if fecha_f!='':
                proyecto.fecha_f= fecha_f
            if fecha_f_contrato!='':
                proyecto.fecha_f_contrato= fecha_f_contrato

            proyecto.save()

        except:
            mensaje='Ocurrio un error'

    datos = Proyectos.objects.order_by("fecha_f").exclude(fecha_i = None)

    total_m2 = sum(Proyectos.objects.exclude(fecha_i = None).values_list("m2", flat=True))

    return render(request, 'proyectos.html', {'datos':datos, 'total_m2':total_m2})



def unidades(request):

    unidades = Unidades.objects.all()
    datos = []

    for dato in unidades:

        if dato.sup_balcon == None:
            dato.sup_balcon = 0

        if dato.sup_patio == None:
            dato.sup_patio = 0

        m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio
        datos.append((dato, m2))

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

                lista_palabra = palabra.split()

                

                buscar = (str(i[0].proyecto)+str(i[0].nombre_unidad)+str(i[0].asig)+str(i[0].estado)+str(i[0].piso_unidad)+str(i[0].tipo)+str(i[1]))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)


    #Aqui termina el filtro

    return render(request, 'psuperficie.html', {"datos":datos})



def cargaunidadesproyecto(request,**kwargs):
    id_proyecto=kwargs['id']
    
    if request.method=='POST':
        datos=request.POST.dict()
        
        proyecto=Proyectos.objects.get(pk=id_proyecto)
        try:
            cant_uni=int(datos['contador'])
            nuevas_unidades=[]
            for form in range(0,cant_uni):
                if form==0:  
                    tipo=datos['tipo']
                    if tipo=='DEPARTAMENTO':
                        if 'tipologia' in datos:
                            tipologia=datos['tipologia']
                        else:
                            tipologia='MONO'
                    else:
                        tipologia=datos['tipo']
                    unidad=Unidades(
                        proyecto=proyecto,
                        piso_unidad=datos['nombre_piso'] + ' ' + datos['numero_piso'],
                        nombre_unidad=datos['nomenclatura'], #nomenclatura
                        tipo=tipo,
                        tipologia=tipologia,
                        sup_propia=datos['sup_propia'],
                        sup_balcon=datos['sup_balcon'],
                        sup_patio=datos['sup_patio'],
                        sup_comun=datos['sup_comun'],
                        sup_equiv=datos['sup_equivalente'],
                    )
                    
                else:
                    form=str(form)
                    nm='nombre_piso'+form
                    np='numero_piso'+form
                    nu='nomenclatura'+form
                    
                    supp='sup_propia'+form
                    supb='sup_balcon'+form
                    suppa='sup_patio'+form
                    supc='sup_comun'+form
                    supq='sup_equivalente'+form
                    t='tipo'+form
                    ti='tipologia'+form
                    tipo=datos[t]
                    
                    if tipo=='DEPARTAMENTO':
                        if ti in datos:
                            tipologia=datos[ti]
                        else:
                            tipologia='MONO'
                    else:
                        tipologia=tipo
                    unidad=Unidades(
                        proyecto=proyecto,
                        piso_unidad=datos[nm] + ' ' + datos[np],
                        nombre_unidad=datos[nu], #nomenclatura
                        tipo=tipo,
                        tipologia=tipologia,
                        sup_propia=datos[supp],
                        sup_balcon=datos[supb],
                        sup_patio=datos[suppa],
                        sup_comun=datos[supc],
                        sup_equiv=datos[supq],
                    )
                nuevas_unidades.append(unidad)

            Unidades.objects.bulk_create(nuevas_unidades)
        except:
            mensaje='Ocurrio un error'
        return redirect('Lista unidades proyecto',proyecto.id)
    return render(request, 'carga_unidades_proyecto.html',{'proyecto':id_proyecto})

def listaunidadesproyecto(request,**kwargs):
    id_proyecto=kwargs['id']
    proyecto=Proyectos.objects.get(pk=id_proyecto)
    unidades=Unidades.objects.filter(proyecto=id_proyecto)

    total_sup_comun=unidades.aggregate(sup_total=Sum('sup_comun'))['sup_total']
    total_sup_balcon=unidades.aggregate(sup_total=Sum('sup_balcon'))['sup_total']
    total_sup_patio=unidades.aggregate(sup_total=Sum('sup_patio'))['sup_total']
    total_sup_propia=unidades.aggregate(sup_total=Sum('sup_propia'))['sup_total']
    total_sup_equiv=unidades.aggregate(sup_total=Sum('sup_equiv'))['sup_total']

    
    total_sup_total=0
    for u in unidades:
        venta=VentasRealizadas.objects.filter(unidad__id=u.id)
        if venta.exists():
            #no tiene permiso
            permiso=0
        else:
            #tiene permiso
            permiso=1
        u.permiso=permiso

        if u.sup_equiv>0:
            total=u.sup_equiv
        else:
            total=u.sup_propia + u.sup_balcon + u.sup_comun + u.sup_patio

        u.sup_total=total
        total_sup_total=total_sup_total+total

    sup_totales={
        'total_sup_comun':total_sup_comun,
        'total_sup_balcon':total_sup_balcon,
        'total_sup_patio':total_sup_patio,
        'total_sup_propia':total_sup_propia,
        'total_sup_total':total_sup_total,
        'total_sup_equiv':total_sup_equiv,
    }
    if request.method=='POST':
        datos=request.POST.dict()
        
        if 'borrar' in datos:
            id_unidad=datos['borrar']
            unidad=Unidades.objects.get(pk=id_unidad)
            unidad.delete()
            return redirect('Lista unidades proyecto',id_proyecto)

        elif 'borrado-masivo' in datos:
            unidades=[]
            for d in datos.keys():
                if 'unidad' in d:
                    
                    unidad=Unidades.objects.get(pk=int(datos[d]))
                    unidad.delete()

            return redirect('Lista unidades proyecto',id_proyecto)

        elif 'editar' in datos:
            id_unidad=datos['editar']
            unidad=Unidades.objects.filter(pk=int(id_unidad))
            tipo=datos['tipo']
            if tipo=='DEPARTAMENTO':
                if 'tipologia' in datos:
                    tipologia=datos['tipologia']
                else:
                    tipologia='MONO'
            else:
                tipologia=datos['tipo']
            unidad.update(
                proyecto=proyecto,
                piso_unidad=datos['nombre_piso'] + ' ' + datos['numero_piso'],
                nombre_unidad=datos['nomenclatura'], #nomenclatura
                tipo=tipo,
                tipologia=tipologia,
                sup_propia=datos['sup_propia'],
                sup_balcon=datos['sup_balcon'],
                sup_patio=datos['sup_patio'],
                sup_comun=datos['sup_comun'],
                sup_equiv=datos['sup_equivalente'],

            )
            return redirect('Lista unidades proyecto',id_proyecto)
    return render(request, 'listado_unidades_proyecto.html',{'unidades':unidades,'proyecto':proyecto,'sup_totales':sup_totales})
