import datetime
import numpy as np
from django.shortcuts import render, redirect
from django.db.models import Q

from proyectos.models import Proyectos
from presupuestos.models import Modelopresupuesto, PresupuestosAlmacenados, Presupuestos
from rrhh.models import datosusuario
from finanzas.models import Almacenero
from compras.models import Compras
from registro.models import RegistroValorProyecto

from funciones_generales import f_bots
from presupuestos.funciones.f_presupuestos import *


def presupuesto_principal(request):

    if request.method=='POST':

        id_proyecto=request.POST.get('proyecto')

        return redirect('presupuesto_proyecto',id_proyecto)

    proyectos = Proyectos.objects.order_by("nombre")

    proyectos = [proyecto for proyecto in proyectos if Modelopresupuesto.objects.filter(proyecto = proyecto).count() > 0]

    return render(request, 'presupuestos/presupuesto_principal.html', {'proyectos':proyectos})


def presupuestos_panel_control(request,id):

    context = {}
    
    proyecto = Proyectos.objects.get(pk=id)
    
    presupuestos_alm=PresupuestosAlmacenados.objects.all()

    #### --> PROCESOS DE RECALCULOS Y NOTIFICACIONES

    if request.method == "POST":

        datos_post = request.POST.dict()

        ## Almacena el archivo vigente sin recalcularlo

        if "extrapolado" in datos_post:

            if request.POST["extrapolado"] == "1":

                proyecto.presupuesto = "ACTIVO"
                proyecto.save()

                try:

                    send = f"El proyecto {proyecto.nombre} paso a estar ACTIVO"
                    id = presupuestos_datos_bot()['Telegram_grupo_presupuesto_id']
                    token = presupuestos_datos_bot()['Telegram_grupo_presupuesto_token']

                    f_bots.bot_telegram(send, id, token)

                except:

                    context["mensaje"] = [False, "Error inesperado al notificar"]

            else:

                proyecto.presupuesto = "EXTRAPOLADO"
                proyecto.save()

                try:

                    send = f"El proyecto {proyecto.nombre} paso a estar EXTRAPOLADO"
                    id = presupuestos_datos_bot()['Telegram_grupo_presupuesto_id']
                    token = presupuestos_datos_bot()['Telegram_grupo_presupuesto_token']

                    f_bots.bot_telegram(send, id, token)

                except:

                    context["mensaje"] = [False, "Error inesperado al notificar"]

        if "base" in datos_post:

            if request.POST["base"] == "1":

                proyecto.presupuesto = "EXTRAPOLADO"
                proyecto.save()

                try:

                    send = f"El proyecto {proyecto.nombre} paso a estar EXTRAPOLADO"
                    id = presupuestos_datos_bot()['Telegram_grupo_presupuesto_id']
                    token = presupuestos_datos_bot()['Telegram_grupo_presupuesto_token']

                    f_bots.bot_telegram(send, id, token)

                except:

                    context["mensaje"] = [False, "Error inesperado al notificar"]

            else:

                proyectos_base = Proyectos.objects.filter(presupuesto = "BASE")

                for proy_base in proyectos_base:
                    proy_base.presupuesto = "EXTRAPOLADO"
                    proy_base.save()

                proyecto.presupuesto = "BASE"
                proyecto.save()

                try:

                    send = f"El proyecto {proyecto.nombre} paso a ser la BASE"
                    id = presupuestos_datos_bot()['Telegram_grupo_presupuesto_id']
                    token = presupuestos_datos_bot()['Telegram_grupo_presupuesto_token']

                    f_bots.bot_telegram(send, id, token)

                except:

                    context["mensaje"] = [False, "Error inesperado al notificar"]



        ## Almacena el archivo vigente sin recalcularlo

        if "almacenar" in datos_post:

            registro_vigente = presupuestos_alm.get(proyecto = proyecto, nombre = "vigente")

            try:

                nuevo_registro = PresupuestosAlmacenados.objects.create(proyecto = proyecto,
                    nombre = str("{}".format(datetime.date.today())), archivo = registro_vigente.archivo)

                context["mensaje"] = [True, "Se guardo una copia con exito"]

            except:

                context["mensaje"] = [False, "Error inesperado al tratar de guardar"]

        ### -> Recalcula el presupuesto y crea un archivo nuevo

        if "recalcular" in datos_post:
            
            try:
                if len(presupuestos_alm.filter(proyecto = proyecto, nombre = "vigente")) > 1:

                    presupuestos_revision_registros(proyecto)

                registro_vigente = presupuestos_alm.get(proyecto = proyecto, nombre = "vigente")
                registro_vigente.nombre = str("{}".format(datetime.date.today()))
                registro_vigente.save()

            except:

                context["mensaje"] = [False, "Error inesperado al tratar de recalcular"]
     

    ## Revisamos si hay un fichero XLS del proyecto
    ## En caso de no encontrar uno, lo creamos y asi queda almacenada una copia con el nombre "VIGENTE"
    ## Actualmente la manera de trabajar es creando este archivo y almacenando copias con nombres de los dias o VIGENTE

    if  presupuestos_alm.filter(proyecto = proyecto, nombre = "vigente").count() == 0:
        

        presupuesto_generar_xls_proyecto(proyecto)
        
        # Utilizamos el BOT de Telegram para notificar al equipo el cambio

        try:

            # Buscaremos el archivo vigente y el anterior

            archivo = presupuestos_alm.get(proyecto = proyecto, nombre = "vigente").archivo
            df = pd.read_excel(archivo)
            repo_nuevo = sum(np.array(df['Monto'].values))

            anterior_archivo = presupuestos_alm.filter(proyecto = proyecto).order_by("-id").exclude(nombre = "vigente")[0].archivo
            df = pd.read_excel(anterior_archivo)
            repo_anterior = sum(np.array(df['Monto'].values))

            var = round((repo_nuevo/repo_anterior-1)*100, 2)

            if var != 0:

                send = "Equipo!, se ha actualizado {} con una variación de {}%. Esta acción surge por el usuario {} ".format(proyecto.nombre, var, request.user.first_name)
            
            else:

                send = "Equipo!, se guardo una copia de {} guardo una copia de {}".format(proyecto.nombre, request.user.first_name)

                              
            id = presupuestos_datos_bot()['Telegram_grupo_presupuesto_id']
            token = presupuestos_datos_bot()['Telegram_grupo_presupuesto_token']

            f_bots.bot_telegram(send, id, token)

        except:

            context["mensaje"] = [False, "Error inesperado al notificar la actualización"]

        ## Hay proyectos que no tienen un esquema de presupuesto, se consideran EXTRAPOLADOS y nacen del valor de otro proyecto 
        ## Estos proyectos se denominan BASE, en caso de sufrir una variación, modificaremos a aquellos que tengan la denominación EXTRAPOLADO 
        ## El siguiente bucle estudia y realiza esa acción

        if proyecto.presupuesto == "BASE" and var != 0:

            proyectos_extrapolados = Proyectos.objects.filter(presupuesto = "EXTRAPOLADO")

            send_success = "Proyectos actualizados con el proyecto base: "
            send_warning = "Proyectos sin actualizar: "

            for proyecto in proyectos_extrapolados:

                try:
                    
                    ### -> Actualizamos primero al presupuesto
                
                    presupuesto_activo = Presupuestos.objects.get(proyecto = proyecto)
                    presupuesto_activo.valor = presupuesto_activo.valor * (1+(var/100))
                    presupuesto_activo.saldo = presupuesto_activo.saldo * (1+(var/100))
                    presupuesto_activo.saldo_mat = presupuesto_activo.saldo_mat * (1+(var/100))
                    presupuesto_activo.saldo_mo =  presupuesto_activo.saldo_mo * (1+(var/100))
                    presupuesto_activo.save()

                    ### -> Actualizamos despues al almacenero

                    almacenero = Almacenero.objects.get(proyecto = proyecto)
                    almacenero.pendiente_iva_ventas = presupuesto_activo.calculo_iva_compras()
                    almacenero.save()

                    ### -> Sumamos el aviso al equipo

                    send_success += "{} con {}% - ".format(proyecto, var)



                except:

                    send_warning += "{} - ".format(proyecto)

            try:

                id = presupuestos_datos_bot()['Telegram_grupo_presupuesto_id']
                token = presupuestos_datos_bot()['Telegram_grupo_presupuesto_token']

                send = "{}, actualizo el proyecto BASE, los extrapolados comenzaran a actualizarse".format(request.user.first_name)
                
                f_bots.bot_telegram(send, id, token)
                f_bots.bot_telegram(send_success, id, token)
                f_bots.bot_telegram(send_warning, id, token)

                send_final = "Finalizo el proceso de actualización exitosamente"

                f_bots.bot_telegram(send_final, id, token)

            except:

                context["mensaje"] = [False, "Error inesperado al notificar la actualización"]

    #### --> CALCULOS DE DATOS NECESARIOS
    
    datos_proyecto = {}
    datos_proyecto['proyecto'] = proyecto

    ## -> Información de abecera

    try:

        context['datos_presupuesto'] = Presupuestos.objects.get(proyecto = proyecto)
        context['presupuestador'] = datosusuario.objects.get(identificacion = context['datos_presupuesto'].presupuestador)

    except:
        
        context['datos_presupuesto'] = False
        context['presupuestador'] = False

    ## -> Para los calculos necesarios utilizaremos las funciones de PANDAS
    # Por lo cual primero transformaremos el archivo vigente en un Data Frame

    archivo_vigente = PresupuestosAlmacenados.objects.filter(proyecto = proyecto, nombre = "vigente")[0].archivo

    df = pd.read_excel(archivo_vigente)

    ## -> Calculo del valor de reposición

    valor_reposicion = sum(np.array(df['Monto'].values))


    ## -> Calculo del valor de saldo


    listado_articulos = df['Articulo'].unique()

    valor_saldo_total = 0
    valor_saldo_proyecto_materiales = 0
    valor_saldo_proyecto_mo = 0

    for articulo in listado_articulos:

        cantidad_solicitada = sum(np.array(df[df['Articulo'] == articulo]['Cantidad Art Totales'].values))

        valor_articulo = Articulos.objects.get(codigo = articulo).valor

        articulos_comprados = sum(np.array(Compras.objects.filter(proyecto = proyecto, articulo__codigo = articulo).values_list("cantidad", flat = True)))
        
        saldo_articulo = (cantidad_solicitada - articulos_comprados)*valor_articulo
        
        ## -> Es importante entender que el saldo podria ser negativo si se compro mas de lo que se necesita
        ## En tal caso el saldo solo seria la parte positiva, ya que lo comprado de mas entraria en concepto de credito

        if saldo_articulo > 0:
            
            valor_saldo_total = valor_saldo_total + saldo_articulo

            ## En el esquema incial, los articulos iniciados con "3" en general son materiales

            if str(articulo)[0] == "3":
                
                valor_saldo_proyecto_materiales += saldo_articulo
           
            else:
                
                valor_saldo_proyecto_mo += saldo_articulo

    ### -> Actualizamos despues al almacenero

    try:

        if proyecto.presupuesto != "EXTRAPOLADO":

            Saldo_act = Presupuestos.objects.get(proyecto = proyecto)
            Saldo_act.valor = valor_reposicion
            Saldo_act.saldo = valor_saldo_total
            Saldo_act.saldo_mat = valor_saldo_proyecto_materiales
            Saldo_act.saldo_mo = valor_saldo_proyecto_mo
            Saldo_act.save()

            almacenero = Almacenero.objects.get(proyecto = proyecto)
            almacenero.pendiente_iva_ventas = presupuesto_activo.calculo_iva_compras()
            almacenero.save()

    except:

        context["mensaje"] = [False, "Error al almacenar datos en el almacenero o presupuesto"]

    ## -> Calculamos el avance para el gradifo tipo PIE


    if valor_reposicion != 0:

        datos_proyecto['avance'] = (1 - (valor_saldo_total/valor_reposicion))*100
        datos_proyecto['pendiente'] = 100 - datos_proyecto['avance']

    else:

        datos_proyecto['avance'] = 0
        datos_proyecto['pendiente'] = 0

    datos_proyecto['proyecto'] = proyecto
    datos_proyecto['valor_reposicion'] = valor_reposicion
    datos_proyecto['valor_saldo'] = valor_saldo_total

    ## -> Crea el historico de valores del proyecto

    valores_proyecto_registrados = RegistroValorProyecto.objects.filter(proyecto = proyecto)

    context['registro_valor_proyecto'] = [(valor_proyecto.fecha, valor_proyecto.precio_proyecto/1000000) for valor_proyecto in valores_proyecto_registrados]

    ## -> Estudia las variaciones del proyecto

    try:
        context['variacion'] = (((valor_reposicion/1000000)/valores_proyecto_registrados[-30][1]) -1)*100
    
    except:
        context['variacion'] = "Sin datos suficientes"
    
    today = datetime.date.today()
    
    ### -> Variación anual
    inicio_year_inicio_month = datetime.date(today.year, 1, 1)
    inicio_year_final_month = datetime.date(today.year, 1, 28)
    
    try:

        datos_bases = RegistroValorProyecto.objects.filter(
            Q(fecha__gte = inicio_year_inicio_month, proyecto = proyecto) & Q(fecha__lte = inicio_year_final_month, proyecto = proyecto)
        ).values_list("precio_proyecto", flat=True)

        valor = (((valor_reposicion)/np.mean(sum(datos_bases))) -1)*100

        variacion_year = [inicio_year_inicio_month, valor]

        context['variacion_year'] = variacion_year

    except:

        context['variacion_year'] = "Sin registros"

    

    ### -> Variación del año pasado
    inicio_yaer_last_inicio_month = datetime.date((today.year - 1), 1, 1)
    inicio_yaer_last_final_month = datetime.date((today.year - 1), 1, 28)

    try:

        datos_bases = RegistroValorProyecto.objects.filter(
            Q(fecha__gte = inicio_yaer_last_inicio_month, proyecto = proyecto) & Q(fecha__lte = inicio_yaer_last_final_month, proyecto = proyecto)
        ).values_list("precio_proyecto", flat=True)

        valor = (((valor_reposicion)/np.mean(sum(datos_bases))) -1)*100

        variacion_year_2 = [inicio_year_inicio_month, valor]

        context['variacion_year_2'] = variacion_year_2

    except:

        context['variacion_year_2'] = "Sin registros"



    context['registro_valor_proyecto'] = context['registro_valor_proyecto'][-60:]

    context['datos_proyecto'] = datos_proyecto


    ###-> Esta parte es para activar una ayuda al presupuestador dentro del panel

    if context['presupuestador']:

        if request.user.username == context['presupuestador']:
            context['que_hacer_general'] = True

        else:
            context['que_hacer_general'] = False


    return render(request, 'presupuestos/presupuesto_proyecto.html', context)