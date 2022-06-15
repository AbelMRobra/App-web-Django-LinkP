from django.shortcuts import render, redirect
from django.db.models import Count , Sum , F ,Q
from email.mime.text import MIMEText

from statistics import mode
from datetime import date

from funciones_generales.f_mandar_email import mandar_email
from funciones_generales.f_saludo import saludo
from funciones_generales.f_bots import bot_telegram
from rrhh.models import EntregaMoneda, datosusuario, CanjeMonedas, PremiosMonedas, MonedaLink, Logros

from users.funciones.functions_linkcoins import estadisticasLinkcoin, email_canje_rrhh, email_canje_usuario,calculos
from users.models import VariablesGenerales



def perfil_movimientos_linkcoins(request):
    amor = 0
    rey = 0
    otros_datos = 0
    monedas_disponibles_canje = 0
    loged_user=request.user.username
    datos_usuarios=datosusuario.objects.all()
    monedas_entregadas=EntregaMoneda.objects.all()
    monedas=MonedaLink.objects.all()
    canjemonedas=CanjeMonedas.objects.all()

    
    try:
        usuario = datos_usuarios.get(identificacion = loged_user)

    except:

        usuario = 0

    if request.method == 'POST':
        datos = request.POST.dict()
        monedas_usuario = monedas.filter(usuario_portador = usuario)
        monedas_disponibles = [m for m in monedas_usuario if monedas_entregadas.filter(moneda = m).count() == 0]

        if 'regalar' in datos:
            usuario_destino=datos_usuarios.get(id = int(datos["usuario"]))
            mens=datos["mensaje"]
            cantidad=int(datos['cantidad'])
            monedas_para_entregar = [EntregaMoneda(
                                    moneda = monedas_disponibles[c],
                                    usuario_recibe = usuario_destino,
                                    mensaje = mens) for c in range(cantidad)]

            EntregaMoneda.objects.bulk_create(monedas_para_entregar)

            #ESTRUCTURAR MENSAJE PARA ENVIAR EMAIL 

            msg = MIMEText("""
        
            Recibiste {} monedas!,

            "{}"

            - {}

            """.format(cantidad ,mens, loged_user))

            subject = "Recibiste {} monedas!!".format(cantidad)

            try:
                mandar_email(msg, usuario_destino.email , subject)

            except:
                mensaje='No se pudo enviar el email'

            return redirect('Guia')


    info_coins_entregadas, monedas_disponibles, recibidas, amor, monedas_disponibles_canje, list_usuarios, rey, rey_l, rey_2=  calculos(datos_usuarios,monedas,monedas_entregadas,usuario,loged_user,canjemonedas)
    
    try:
        datos = datos_usuarios.get(identificacion = request.user)
        if datos:
            areas = datos_usuarios.values_list("area").exclude(estado = "NO ACTIVO").distinct()
            otros_datos = [(a , datos_usuarios.filter(area = a[0]).order_by("identificacion").exclude(estado = "NO ACTIVO")) for a in areas]

    except:

        datos = 0

    try:
        usuario = datos_usuarios.get(identificacion = loged_user)

    except:
        usuario = 0

    monedas_recibidas = monedas_entregadas.filter(usuario_recibe = usuario).count()
    argentino = monedas_entregadas.filter(moneda__usuario_portador__identificacion = loged_user, mensaje__icontains = "bolud").count()

    try:
        logros = Logros.objects.filter(usuario = datos_usuarios.get(identificacion = loged_user))
    
    except:
        logros = 0  

    conten = {"argentino":argentino, 
    "logros":logros, 
    "rey":rey, 
    "amor":amor, 
    "datos":datos, 
    "otros_datos":otros_datos, 
    "recibidas":recibidas, 
    "monedas_recibidas":monedas_recibidas, 
    "monedas_disponibles":monedas_disponibles, 
    "monedas_disponibles_canje":monedas_disponibles_canje, 
    "list_usuarios":list_usuarios, "info_coins_entregadas":info_coins_entregadas}

    return render(request, "linkcoins/linkcoins_perfil_movimientos.html", conten)

def canjes_realizados(request):
    # Listado de los datos de los premios
    context = {}
    context['mensaje_bievenida'] = saludo().format(request.user.first_name)
    context['data_linkcoins'] = estadisticasLinkcoin()

    if request.method == 'POST':
        datos=request.POST.dict()

        if 'ENTREGADO' in datos:
            canje = CanjeMonedas.objects.get(id = int(datos['ENTREGADO']))
            canje.entregado = "SI"
            canje.save()
            return redirect('Canjes realizados')

    context['data'] = CanjeMonedas.objects.all().order_by("entregado")
    return render(request, "linkcoins/linkcoins_listarcanjes.html", context)

def generador_linkcoins(request):

    if request.method == 'POST':
        datos=request.POST.dict()

        if 'generar' in datos:
            cant = int(datos['cantidad']) + 1
            mens = datos['mensaje']
    
            destino = datosusuario.objects.get(id = datos['usuario'])
            for i in range(1,cant):

                nueva_moneda = MonedaLink(
                    nombre = str(date.today()) + "LINK" + str(datosusuario.objects.get(id = datos['usuario']).identificacion) + str(i),
                    usuario_portador = datosusuario.objects.get(identificacion = request.user.username),
                    fecha = date.today(),
                    tipo = "REGALO DE LINK"
                )
                nueva_moneda.save()

                entrega = EntregaMoneda(
                    moneda = nueva_moneda,
                    fecha = date.today(),
                    usuario_recibe = destino,
                    mensaje = mens,

                )
                entrega.save()

            
            cant=cant-1
            titulo='Recibiste monedas de Link ! :)'
            msg =MIMEText("""
            La empresa te ha regalado {} monedas ! :) 

            Lee tu mensaje : {}  

                                Saludos ! - Link'
                           
            """.format(cant,mens))

            try:
                mandar_email(msg , destino.email , titulo)
            except:
                mensaje='No se pudo enviar el email'
                
            return redirect('Generador')


    #USUARIOS QUE HAN RECIBIDO MONEDAS GENERADAS POR LINK
 
    datos_monedas_entregadas = EntregaMoneda.objects.filter(Q(moneda__nombre__icontains = "LINK")) \
                    .values(user=F('usuario_recibe__identificacion'),nombre=F('usuario_recibe__nombre'),mens=F('mensaje')) \
                    .distinct().annotate(cant=Count('id'))

    data_generador = [(i , datosusuario.objects.get(identificacion = i['user']).imagenlogo) for i in datos_monedas_entregadas]

    #los usuarios se ordenan por defecto en orden alfabetico 
    #data_generador.sort(key = lambda x: x[0])


    context = {}
    context['data_generador'] = data_generador
    context['mensaje_bievenida'] = saludo().format(request.user.first_name)
    context['list_usuarios'] = datosusuario.objects.all().order_by("identificacion").exclude(estado = "NO ACTIVO")

    return render(request, "linkcoins/linkcoins_generarmonedas.html", context)

def canjear_monedas(request):
    context = {}
    canjes=CanjeMonedas.objects.all()
    premios=PremiosMonedas.objects.all()
    usuario = datosusuario.objects.get(identificacion = request.user)
    variables_sistema = VariablesGenerales.objects.get(id = 1)
    monedas_recibidas = EntregaMoneda.objects.filter(usuario_recibe = usuario).count()
    monedas_canjear = monedas_recibidas - sum(canjes.filter(usuario = usuario).values_list("monedas", flat=True))
    mensaje = ''
    
    if request.method == 'POST':
        datos=request.POST.dict()
        today = date.today()

        if 'premio' in datos:
            premio=datos['premio']
            canje_activo = True
            
            if not variables_sistema.canje_activo:
                canje_activo = False

            if today.day < variables_sistema.linkcoins_inicial:
                canje_activo = False

            if today.day > variables_sistema.linkcoins_final:
                canje_activo = False

            if request.user.username == "PM":
                canje_activo = True

            if canje_activo:
                premio_solicitado = premios.get(id = int(premio))

                if monedas_canjear >= premio_solicitado.cantidad:
                    canje = CanjeMonedas(
                        usuario = usuario,
                        fecha = date.today(),
                        premio = str(premio_solicitado.nombre),
                        monedas = int(premio_solicitado.cantidad),
                    )
                    canje.save()

                    send = f"Buenas!, el usuario {usuario} ha canjeado {canje.monedas} por el premio: {canje.premio}"
                    id = "-755393879"
                    token = "1880193427:AAH-Ej5ColiocfDZrDxUpvsJi5QHWsASRxA"
                    bot_telegram(send, id, token)
                    context['canje_realizado'] = True 

                else:
                    mensaje = "No tienes suficientes monedas para canjear el premio seleccionado"
        
            else:
                mensaje = f"Actualmente no puede realizar el canje, recuerde que las fechas son desde el {variables_sistema.linkcoins_inicial} al {variables_sistema.linkcoins_final}"
  
        if  'id' in datos:
            if datos['id'] != "0":
                premio = premios.get(id = int(datos['id']))
                premio.nombre = datos['nombre']
                premio.cantidad = datos['cantidad']
                premio.save()

            else:
                variables_sistema.linkcoins_inicial = datos['desde']
                variables_sistema.linkcoins_final = datos['hasta']
                
                if "canje_activo" in datos:
                    variables_sistema.canje_activo = True
                else:
                    variables_sistema.canje_activo = False

                variables_sistema.save()

                if datos['nombre'] != "" and datos['cantidad'] > 0:
                    nuevo_canje = PremiosMonedas.objects.create(
                        nombre = datos['nombre'],
                        cantidad = int(datos['cantidad']),
                    )

        if 'borrar' in datos:
            premio=datos['borrar']
            premio = premios.get(id = int(premio))
            premio.delete()

    premios = premios.order_by("nombre")
    monedas = MonedaLink.objects.filter(usuario_portador = usuario)
    monedas_recibidas = EntregaMoneda.objects.filter(usuario_recibe = usuario).count()
    monedas_canjear = monedas_recibidas - sum(canjes.filter(usuario = usuario).values_list("monedas", flat=True))
    monedas_disponibles = sum([1 for m in monedas if EntregaMoneda.objects.filter(moneda = m).count() == 0])
    dato_monedas = {'monedas_recibidas':monedas_recibidas, 'monedas_disponibles':monedas_disponibles, 'monedas':monedas, 'monedas_canjear':monedas_canjear}
    context['premios'] = premios
    context['dato_monedas'] = dato_monedas
    context['mensaje'] = mensaje
    context['canje_activo'] = variables_sistema.canje_activo
    context['canje_desde'] = variables_sistema.linkcoins_inicial
    context['canje_hasta'] = variables_sistema.linkcoins_final
    return render(request, "linkcoins/linkcoins_canjearmonedas.html", context)


