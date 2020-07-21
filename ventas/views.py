from django.shortcuts import render
from .models import EstudioMercado, PricingResumen
from proyectos.models import Unidades, Proyectos
from finanzas.models import Almacenero
from ventas.models import Pricing, ArchivosAreaVentas, VentasRealizadas
from presupuestos.models import Constantes
from datetime import date
from django.shortcuts import redirect
import datetime
import operator
import numpy as np

# Create your views here.

def radiografia(request):

    busqueda = 1
    datos_pricing = ArchivosAreaVentas.objects.all()
    datos = 0
    fecha = 0

    fechas = []

    for dato in datos_pricing:
        fechas.append((dato.fecha, str(dato.fecha)))

    fechas = list(set(fechas))

    fechas.sort( reverse=True)

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:

            if dato[0] == "fecha":
                datos = ArchivosAreaVentas.objects.get(fecha = dato[1])
                busqueda = 0
                fecha = dato[1]




    datos = {"fechas":fechas,
    "busqueda":busqueda,
    "datos":datos,
    "fecha":fecha}

    return render(request, 'radiografiaclientes.html', {"datos":datos})

def resumenprecio(request):

    busqueda = 1
    datos_pricing = PricingResumen.objects.all()
    datos = 0
    fecha = 0

    fechas = []

    for dato in datos_pricing:
        fechas.append((dato.fecha, str(dato.fecha)))

    fechas = list(set(fechas))

    fechas.sort( reverse=True)

    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        for dato in datos_elegidos:
            if dato[0] == "fecha":
                datos = PricingResumen.objects.filter(fecha = dato[1])
                busqueda = 0
                fecha = dato[1]



    datos = {"fechas":fechas,
    "busqueda":busqueda,
    "datos":datos,
    "fecha":fecha}

    return render(request, 'resumenprecio.html', {"datos":datos})





def estmercado(request):

    datos_estudio = EstudioMercado.objects.all()

    estudios = []
    meses = []
    datos_link = []
    datos_otros = []
    grafico = 0

    for dato in datos_estudio:

        estudios.append(str(dato.fecha))
        meses.append(dato.meses)

    estudios = list(set(estudios))
    meses = list(set(meses))
    meses.sort()

    if request.method == 'POST':

        grafico = 1

        estudio = request.POST.items()

        for dato in estudio:

            if dato[0] == 'csrfmiddlewaretoken':
                print("Basura")

            else:

                for i in datos_estudio:
                    if str(i.fecha) == dato[1]:
                        if i.empresa == "LINK":
                            datos_link.append(i)
                        else:
                            datos_otros.append(i)

    datos = {
        "link":datos_link,
        "otros":datos_otros,
        "meses":meses,
        "estudios":estudios,
        "graficos":grafico,
    }

    return render(request, 'estmercado.html', {"datos":datos})

def panelunidades(request):

    datos = Unidades.objects.all()

    proyectos = []

    datos_unidades = 0

    mensaje = 0

    otros_datos = 0


    for dato in datos:
        proyectos.append(dato.proyecto)

    proyectos = list(set(proyectos))


    if request.method == 'POST':

        #Trae los datos elegidos
        datos_elegidos = request.POST.items()

        list_proyectos = []
        aisgnacion = []
        disponibilidad = []

        for dato in datos_elegidos:

            if "Asig" in str(dato[0]):
                aisgnacion.append(dato[1])

            elif "Disp" in str(dato[0]):
                disponibilidad.append(dato[1])

            elif str(dato[0]) == "csrfmiddlewaretoken":
                print("basura")

            else:
                list_proyectos.append(dato[0])

        if len(list_proyectos)==0 or len(aisgnacion)==0 or len(disponibilidad)==0:
            mensaje = 1

        else:
            mensaje = 2
            otros_datos = []
            datos_tabla_unidad = []
            m2_totales = 0
            monto_total = 0
            cocheras = 0

            for proy in list_proyectos:
                for asig in aisgnacion:
                    for disp in disponibilidad:
                        
                        datos_unidades = Unidades.objects.filter(proyecto__nombre = proy, asig = asig, estado=disp)
                        
                        for dato in datos_unidades:
                            if dato.sup_equiv > 0:

                                m2 = dato.sup_equiv

                            else:

                                m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio
                            
                            try:
                                param_uni = Pricing.objects.get(unidad = dato)
                                desde = dato.proyecto.desde

                                if dato.tipo == "COCHERA":
                                    desde = dato.proyecto.desde*dato.proyecto.descuento_cochera

                                if param_uni.frente == "SI":
                                    desde = desde*dato.proyecto.recargo_frente

                                if param_uni.piso_intermedio == "SI":
                                    desde =desde*dato.proyecto.recargo_piso_intermedio

                                if param_uni.cocina_separada == "SI":
                                    desde = desde*dato.proyecto.recargo_cocina_separada

                                if param_uni.local == "SI":
                                    desde = desde*dato.proyecto.recargo_local

                                if param_uni.menor_45_m2 == "SI":
                                    desde = desde*dato.proyecto.recargo_menor_45

                                if param_uni.menor_50_m2 == "SI":
                                    desde = desde*dato.proyecto.recargo_menor_50

                                if param_uni.otros == "SI":
                                    desde = desde*dato.proyecto.recargo_otros 

                                desde = desde*m2 
                                monto_total = monto_total + desde 

                                m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio


                            except:
                                
                                desde = "NO DEFINIDO"



                            datos_tabla_unidad.append((dato, m2, desde, dato.id))
                            
                            m2_totales = m2_totales + m2
                            
                            if dato.tipo == "COCHERA":
                                cocheras += 1
                            


            cantidad = len(datos_tabla_unidad)

            departamentos = cantidad - cocheras

            otros_datos.append((m2_totales, cantidad, departamentos, cocheras, monto_total))

            datos_unidades = datos_tabla_unidad

            datos_unidades.sort(key=lambda datos_unidades: datos_unidades[3], reverse=False)


    datos = {"proyectos":proyectos, "datos":datos, "mensaje":mensaje, "datos_unidades":datos_unidades, "otros_datos":otros_datos}

    return render(request, 'panelunidades.html', {"datos":datos})

def editarasignacion(request, id_unidad):

    id_unidad = id_unidad

    datos = Unidades.objects.get(id = id_unidad)

    if request.method == 'POST':

        valor_elegido = request.POST.items()

        for valor in valor_elegido:
            
            if valor[0] == "asignacion":

                if valor[1] == "1":
                    datos.asig = "PROYECTO"

                    datos.save()

                if valor[1] == "2":
                    datos.asig = "TERRENO"

                    datos.save()

                if valor[1] == "3":
                    datos.asig = "HON. LINK"

                    datos.save()

                if valor[1] == "4":

                    datos.asig = "SOCIOS"

                    datos.save()


                return redirect ('Panel de unidades')

    return render(request, 'editarasig.html', {"datos":datos} )

def pricing(request, id_proyecto):


    #Aqui empieza para cambiar el precio base

    if request.method == 'GET':

        nuevo_precio = request.GET.items()

        for precio in nuevo_precio:

            datos_modificar = Proyectos.objects.get(id = id_proyecto)
            
            datos_modificar.desde = precio[1]

            datos_modificar.save()


    proyecto = Proyectos.objects.get(id = id_proyecto)


    datos = Unidades.objects.filter(proyecto = proyecto)

    mensaje = 0
    otros_datos = 0
    anticipo = 0.4
    fecha_entrega =  datetime.datetime.strptime(str(proyecto.fecha_f), '%Y-%m-%d')

    ahora = datetime.datetime.utcnow()

    y = fecha_entrega.year - ahora.year
    n = fecha_entrega.month - ahora.month
    meses = y*12 + n

    financiado = 0
    financiado_m2 = 0
    fin_ant = 0
    valor_cuotas = 0

    mensaje = 2
    otros_datos = []
    datos_tabla_unidad = []
    m2_totales = 0
    cocheras = 0
    ingreso_ventas = 0
    unidades_socios = 0

    #Datos resumenes de arriba

    sumatoria_contado = 0
    sumatoria_financiado = 0
    
    for dato in datos:

        if dato.sup_equiv > 0:

            m2 = dato.sup_equiv

        else:

            m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio

        try:
            venta = VentasRealizadas.objects.get(unidad = dato.id)

            venta.m2 = m2

            venta.asignacion = dato.asig

            venta.save()
        
        except:

            print("Esta unidad no esta vendida")
        
        try:
            param_uni = Pricing.objects.get(unidad = dato)
            desde = dato.proyecto.desde

            if dato.tipo == "COCHERA":
                desde = dato.proyecto.desde*dato.proyecto.descuento_cochera

            if param_uni.frente == "SI":
                desde = desde*dato.proyecto.recargo_frente

            if param_uni.piso_intermedio == "SI":
                desde =desde*dato.proyecto.recargo_piso_intermedio

            if param_uni.cocina_separada == "SI":
                desde = desde*dato.proyecto.recargo_cocina_separada

            if param_uni.local == "SI":
                desde = desde*dato.proyecto.recargo_local

            if param_uni.menor_45_m2 == "SI":
                desde = desde*dato.proyecto.recargo_menor_45

            if param_uni.menor_50_m2 == "SI":
                desde = desde*dato.proyecto.recargo_menor_50

            if param_uni.otros == "SI":
                desde = desde*dato.proyecto.recargo_otros 

            #Aqui calculamos el contado/financiado
            
            contado = desde*m2           

            values = [0]

            for m in range((meses)):
                values.append(1)

            anticipo = 0.4

            valor_auxiliar = np.npv(rate=(dato.proyecto.tasa_f/100), values=values)

            incremento = (meses/(1-anticipo)/(((anticipo/(1-anticipo))*meses)+valor_auxiliar))


            financiado = contado*incremento

            financiado_m2 = financiado/m2
            
            fin_ant = financiado*anticipo

            valor_cuotas = (financiado - fin_ant)/meses

            #Aqui actualizamos los datos del almacenero

            if (dato.estado == "DISPONIBLE" and dato.asig == "PROYECTO") or (dato.asig == "SOCIOS") or (dato.estado == "SEÑADA" and dato.asig == "PROYECTO")  :
                
                ingreso_ventas = ingreso_ventas + contado

                if dato.asig == "SOCIOS":

                    unidades_socios = unidades_socios + contado

        except:

            desde = "NO DEFINIDO"
            contado = "NO DEFINIDO"

        venta = 0


        try:
  
            venta= VentasRealizadas.objects.filter(unidad = dato.id)

            contador = 0

            for v in venta:
                contador += 1

            if contador == 0:
                venta = 0
    

        except:
            venta = 0


        #Aqui sumamos los datos

        m2 = dato.sup_propia + dato.sup_balcon + dato.sup_comun + dato.sup_patio
        
        datos_tabla_unidad.append((dato, m2, desde, dato.id, contado, financiado, financiado_m2, fin_ant, valor_cuotas, venta))
        
        #Aqui vamos armando los m2 totales y los m2 de cocheras

        m2_totales = m2_totales + m2
        try:
            sumatoria_contado = sumatoria_contado + contado
            sumatoria_financiado = sumatoria_financiado + financiado
        except:
            print("Unidades sin pricing")
        
        if dato.tipo == "COCHERA":
            cocheras += 1
                            

    almacenero = Almacenero.objects.get(proyecto = proyecto)

    #Aqui resto el 6% 

    almacenero.ingreso_ventas = ingreso_ventas - ingreso_ventas*0.06
    almacenero.save()
    almacenero.unidades_socios = unidades_socios - unidades_socios*0.06
    print(unidades_socios)
    almacenero.save()

    cantidad = len(datos_tabla_unidad)

    departamentos = cantidad - cocheras

    #Aqui calculo promedio contado y promedio financiado

    promedio_contado = sumatoria_contado/m2_totales
    promedio_financiado = sumatoria_financiado/m2_totales

    otros_datos.append((m2_totales, cantidad, departamentos, cocheras, promedio_contado, promedio_financiado))

    datos_unidades = datos_tabla_unidad
    
    #Aqui empieza el filtro

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        datos_viejos = datos_unidades

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

                buscar = (str(i[0].tipo)+str(i[0].asig)+str(i[0].piso_unidad)+str(i[0].nombre_unidad)+str(i[0].estado)+str(i[0].tipologia))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)

        datos_unidades = datos
    
    #Aqui termina el filtro

    anticipo = anticipo*100




    datos_unidades.sort(key=lambda datos_unidades: datos_unidades[3], reverse=False)


    datos = {"proyecto":proyecto, "datos":datos, "mensaje":mensaje, "datos_unidades":datos_unidades, "otros_datos":otros_datos, "anticipo":anticipo, "meses":meses}

    return render(request, 'pricing.html', {"datos":datos})

def panelpricing(request):

    proyectos = Unidades.objects.all()


    datos  = []

    for proyecto in proyectos:
        datos.append(proyecto.proyecto.nombre)

    datos = list(set(datos))

    if request.method == 'POST':

        palabra_buscar = request.POST.items()

        contador = 1

        for dato in palabra_buscar:

            if contador == 1:
                contador += 1
            
            
            if dato[0] == "proyecto":


                proyecto = Proyectos.objects.get(nombre = dato[1])

                id_proyecto = proyecto.id
                
                return redirect( 'Pricing', id_proyecto = id_proyecto )


    return render(request, 'panelpricing.html', {"datos":datos})

def cargarventa(request):

    datos = VentasRealizadas.objects.order_by("-fecha")

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

                buscar = (str(i.unidad.proyecto.nombre)+str(i.comprador)+str(i.unidad.piso_unidad)+str(i.unidad.nombre_unidad)+str(i.unidad.tipologia)+str(i.asignacion))

                contador = 0

                for palabra in lista_palabra:

                    contador2 = 0

                    if palabra.lower() in buscar.lower():
  
                        contador += 1

                if contador == len(lista_palabra):

                    datos.append(i)

        datos_unidades = datos
    
    #Aqui termina el filtro



    return render(request, 'cargarventas.html', {'datos':datos})

def cargar_venta(request):

    datos = Unidades.objects.all()

    mensaje = 0

    if request.method == 'POST':

        datos_formulario = request.POST.items()

        comprador = "Nadie"
        precio_venta = 0
        anticipo = 0
        cuotas_pend = 0
        tipo_venta = "Ninguna"
        unidad = 0
        fecha = 0
        proyecto = 0
        observaciones = ""

        for dato in datos_formulario:

            if dato[0] == "unidad":
                unidad = Unidades.objects.get(id = int(dato[1]))
                proyecto = Proyectos.objects.get(id = unidad.proyecto.id)

            if dato[0] == "comprador":
                comprador = dato[1]

            if dato[0] == "anticipo":
                anticipo = dato[1]

            if dato[0] == "precio_venta":
                precio_venta = dato[1]

            if dato[0] == "cuotas":
                cuotas_pend = dato[1]

            if dato[0] == "tipo_venta":
                tipo_venta = dato[1]

            if dato[0] == "fecha":
                fecha = dato[1]

            if dato[0] == "observaciones":
                observaciones = dato[1]


        operaciones = VentasRealizadas.objects.filter(unidad = unidad)

        if len(operaciones) > 0:
            mensaje = "Esta unidad se encuentra asignada"

        else:
        
            b = VentasRealizadas(

                comprador = comprador,
                fecha = fecha,
                tipo_venta = tipo_venta,
                unidad = unidad,
                tipo_unidad = "n",
                proyecto = proyecto,
                m2 = 0,
                asignacion = "n",
                precio_venta = precio_venta,
                anticipo = anticipo,
                cuotas_pend = cuotas_pend,
                observaciones = observaciones,


            )

            b.save()

            unidad.estado = "SEÑADA"
            unidad.save()

            return redirect( 'Cargar Venta' )



    return render(request, 'cargar_venta.html', {'datos':datos, 'mensaje':mensaje})

def editarventa(request, id_venta):

    datos = VentasRealizadas.objects.get(id = id_venta)

    if request.method == 'POST':

        datos_formulario = request.POST.items()

        comprador = "Nadie"
        precio_venta = 0
        anticipo = 0
        cuotas_pend = 0
        tipo_venta = "Ninguna"
        unidad = 0
        fecha = 0
        proyecto = 0
        observaciones = ""

        for dato in datos_formulario:

            if dato[0] == "comprador":
                comprador = dato[1]
                datos.comprador = comprador
                datos.save()

            if dato[0] == "anticipo" and dato[1] != "":
                anticipo = dato[1]
                datos.anticipo = anticipo
                datos.save()

            if dato[0] == "precio_venta" and dato[1] != "":
                precio_venta = dato[1]
                datos.precio_venta = precio_venta
                datos.save()

            if dato[0] == "cuotas" and dato[1] != "":
                cuotas_pend = dato[1]
                datos.cuotas_pend = cuotas_pend
                datos.save()

            if dato[0] == "tipo_venta":
                tipo_venta = dato[1]
                datos.tipo_venta = tipo_venta
                datos.save()

            if dato[0] == "fecha" and dato[1] != "":
                fecha = dato[1]
                datos.fecha = fecha
                datos.save()

            if dato[0] == "observaciones":
                observaciones = dato[1]
                datos.observaciones = observaciones
                datos.save()

        return redirect( 'Cargar Venta' )


    return render(request, 'editar_venta.html', {'datos':datos})

def eliminarventa(request, id_venta):

    datos = VentasRealizadas.objects.get(id = id_venta)

    if request.method == 'POST':

        unidad = Unidades.objects.get(id = datos.unidad.id)

        unidad.estado = "DISPONIBLE"

        unidad.save()

        datos.delete()

        return redirect( 'Cargar Venta' )

    return render(request, 'eliminar_venta.html', {'datos':datos})

def detalleventa(request, id_venta):

    datos = VentasRealizadas.objects.get(id = id_venta)

    return render(request, 'detallesventa.html', {'datos':datos})

def cotizador(request, id_unidad):

    datos = Unidades.objects.get(id = id_unidad)

    hormigon = Constantes.objects.get(id = 7)

    m2 = 0

    desde = 0

    if datos.sup_equiv > 0:

        m2 = datos.sup_equiv

    else:

        m2 = datos.sup_propia + datos.sup_balcon + datos.sup_comun + datos.sup_patio


    try:
        param_uni = Pricing.objects.get(unidad = datos)
        desde = datos.proyecto.desde

        if datos.tipo == "COCHERA":
            desde = datos.proyecto.desde*datos.proyecto.descuento_cochera

        if param_uni.frente == "SI":
            desde = desde*datos.proyecto.recargo_frente

        if param_uni.piso_intermedio == "SI":
            desde =desde*datos.proyecto.recargo_piso_intermedio

        if param_uni.cocina_separada == "SI":
            desde = desde*datos.proyecto.recargo_cocina_separada

        if param_uni.local == "SI":
            desde = desde*datos.proyecto.recargo_local

        if param_uni.menor_45_m2 == "SI":
            desde = desde*datos.proyecto.recargo_menor_45

        if param_uni.menor_50_m2 == "SI":
            desde = desde*datos.proyecto.recargo_menor_50

        if param_uni.otros == "SI":
            desde = desde*datos.proyecto.recargo_otros 

    except:

        pass

    precio_contado = desde*m2

    resultados = []

    if request.method == 'POST':

        datos_formulario = request.POST.items()

        for dato in datos_formulario:
            
            if dato[0] == "anticipo":
                
                anticipo = dato[1]

                anticipo_h = float(anticipo)/hormigon.valor

                resultados.append(anticipo)
                resultados.append(anticipo_h)

            if dato[0] == "cuotas_esp":
                cuota_esp = dato[1]
            if dato[0] == "aporte":
                aporte = dato[1]
            if dato[0] == "cuotas_p":
                cuotas_p = dato[1]

        total_cuotas = float(cuota_esp) + float(cuotas_p)*1.65 + float(aporte)

        cuotas_espera = []
        cuotas_pose = []
        aporte_va = []

        for i in range(1):
            cuotas_espera.append(0)
            cuotas_pose.append(0)
            aporte_va.append(0)

        for i in range(int(cuota_esp)):
            cuotas_espera.append(1)
            cuotas_pose.append(0)
            aporte_va.append(0)

        if int(aporte) > 0:
            aporte_va.pop()
            aporte_va.append(int(aporte))

        for d in range(int(cuotas_p)):
            cuotas_pose.append(1.65)

        valor_auxiliar_espera = np.npv(rate=(datos.proyecto.tasa_f/100), values=cuotas_espera)

        valor_auxiliar_pose = np.npv(rate=(datos.proyecto.tasa_f/100), values=cuotas_pose)

        valor_auxiliar_aporte = np.npv(rate=(datos.proyecto.tasa_f/100), values=aporte_va)


        factor = valor_auxiliar_aporte + valor_auxiliar_espera + valor_auxiliar_pose

        incremento = (total_cuotas/factor) - 1

        print(incremento)

        precio_finan = ((precio_contado - float(anticipo))*(1 + incremento)) + float(anticipo)

        print(precio_finan)
        
        importe_cuota_esp = (precio_finan-float(anticipo))/total_cuotas
        importe_aporte = importe_cuota_esp*float(aporte)
        importe_cuota_p = importe_cuota_esp*1.65
        importe_cuota_p_h = importe_cuota_p/hormigon.valor
        importe_aporte_h = importe_aporte/hormigon.valor
        importe_cuota_esp_h = importe_cuota_esp/hormigon.valor


        resultados.append(precio_finan)
        resultados.append(cuota_esp)
        resultados.append(importe_aporte)
        resultados.append(cuotas_p)
        resultados.append(importe_cuota_esp)
        resultados.append(aporte)
        resultados.append(importe_cuota_p)
        resultados.append(importe_cuota_p_h)
        resultados.append(importe_cuota_esp_h)
        resultados.append(importe_aporte_h)

    return render(request, 'cotizador.html', {'datos':datos, 'resultados':resultados, 'precio_contado':precio_contado, 'm2':m2})






