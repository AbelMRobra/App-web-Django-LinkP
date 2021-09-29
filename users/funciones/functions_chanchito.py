from rrhh.models import datosusuario, RegistroContable, Cajas
from finanzas.models import Arqueo
from presupuestos.models import Registrodeconstantes
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd

def agregar_objeto_caja():

    registros = RegistroContable.objects.filter(caja_vinculada = None)

    for registro in registros:
        
        if Cajas.objects.filter(usuario = registro.usuario, nombre = registro.caja).count() == 1:
            caja_vinculada = Cajas.objects.get(usuario = registro.usuario, nombre = registro.caja)
            registro.caja_vinculada = caja_vinculada
            registro.save()

        else:
            new_caja = Cajas(
                usuario = registro.usuario,
                nombre = registro.caja,
            )

            new_caja.save()
            new_caja.usuarios_visibles.add(registro.usuario)

            new_caja.save()

def calcularResumenIngresos(usuario):

    # Resolver parte de ingresos

    if usuario.identificacion == "PL":
        list = ["PL"]
    elif usuario.identificacion == "SP":
        list = ["SP"]
    elif usuario.identificacion == "ALM" or usuario.identificacion == "CA" or usuario.identificacion == "AR":
        list = ["SP", "PL"]
    else:
        list = []

    context = {}

    consulta_principal = RegistroContable.objects.all()

    fecha_inicial = date(2021, 1, 1)

    fechas_totales = []

    while fecha_inicial < date.today():
        
        fechas_totales.append(fecha_inicial)

        if fecha_inicial.month == 12:
            fecha_inicial = date(fecha_inicial.year + 1, 1, 1)
        else:
            fecha_inicial = date(fecha_inicial.year, fecha_inicial.month + 1, 1)

    
    context['fechas_totales'] = fechas_totales

    context['datos'] = {}
    context['datos_h'] = {}

    for usuario in list:

        usuario = datosusuario.objects.get(identificacion = usuario)

        consulta_usuario = consulta_principal.filter(usuario = usuario)

        ingresos_mensuales = []
        ingresos_mensuales_h = []

        for fecha in  fechas_totales:

            if fecha.month == 12:
                fecha_final = date(fecha.year + 1, 1, 1)
            else:
                fecha_final = date(fecha.year, fecha.month + 1, 1)

            fecha_inicial_auxiliar = fecha
            fecha_final = fecha_final - timedelta(days=1)

            comercial_shajor = sum(np.array(consulta_usuario.filter(categoria = "INGRESO SUELDOS COMERCIAL", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").values_list("importe", flat=True)))
            sigma_shajor =  sum(np.array(consulta_usuario.filter(categoria = "INGRESOS SIGMA", nota__contains = "SHAJOR", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").values_list("importe", flat=True)))
            sigma_blanco = sum(np.array(consulta_usuario.filter(categoria = "INGRESOS SIGMA", nota__contains = "BANCO", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").exclude(nota__contains = "SHAJOR").values_list("importe", flat=True)))
            azlepi_shajor =  sum(np.array(consulta_usuario.filter(categoria = "INGRESOS AZLEPI", nota__contains = "SHAJOR", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").values_list("importe", flat=True)))
            azlepi_blanco = sum(np.array(consulta_usuario.filter(categoria = "INGRESOS AZLEPI", nota__contains = "BANCO", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").exclude(nota__contains = "SHAJOR").values_list("importe", flat=True)))
            total = comercial_shajor + sigma_shajor + sigma_blanco + azlepi_shajor + azlepi_blanco

            ingresos_mensuales.append((comercial_shajor, sigma_shajor, sigma_blanco, azlepi_shajor, azlepi_blanco, total))

            try:
                valor_h = Registrodeconstantes.objects.get(constante__id = 7, fecha = fecha).valor
            except:
                valor_h = 1

            ingresos_mensuales_h.append(np.array([comercial_shajor, sigma_shajor, sigma_blanco, azlepi_shajor, azlepi_blanco, total])/valor_h)

        context['datos'][usuario.identificacion] = ingresos_mensuales
        context['datos_h'][usuario.identificacion] = ingresos_mensuales_h
        context['con_sigma_shajor'] = consulta_usuario.filter(categoria = "INGRESOS SIGMA", nota__contains = "SHAJOR", estado = "INGRESOS").order_by("fecha")

    return context

def cajasDerivadas(usuario, palabra, caja):

    consulta_principal = RegistroContable.objects.filter(usuario = usuario)

    # Primero creamos los registros de retiros personales
    
    consulta_filtrada = consulta_principal.filter(nota__contains = palabra)

    for consulta in consulta_filtrada:

        if "AUTO" in consulta.nota:

            id_registro = int(consulta.nota.split("-")[1])
            if len(consulta_principal.filter(id = id_registro)) == 0:
                consulta.delete()

        else:

            nueva_nota = "AUTO-"+str(consulta.id)+"-"+str(consulta.nota)

            if len(consulta_filtrada.filter(nota = nueva_nota)) == 0:

                nuevo_registro = RegistroContable(

                    usuario = usuario,
                    creador = consulta.creador,
                    fecha = consulta.fecha,
                    estado = "INGRESOS",
                    caja = caja,
                    cuenta = consulta.cuenta,
                    categoria = consulta.categoria,
                    importe = consulta.importe,
                    nota = nueva_nota,

                )

                nuevo_registro.save()

def cajasActivas(user):

    cajas_usuario = Cajas.objects.filter(usuario = user)
    con_principal = RegistroContable.objects.filter(caja_vinculada__usuario = user)

    total_cajas = []

    for caja in cajas_usuario:

        ingresos = sum(np.array(con_principal.filter(caja_vinculada = caja, estado = "INGRESOS").values_list("importe", flat=True)))
        gastos = sum(np.array(con_principal.filter(caja_vinculada = caja, estado = "GASTOS").values_list("importe", flat=True)))
        balance = ingresos - gastos
        

        ingresos_usd = sum(np.array(con_principal.filter(caja_vinculada = caja, estado = "INGRESOS").exclude(importe_usd = None).values_list("importe_usd", flat=True)))
        gastos_usd = sum(np.array(con_principal.filter(caja_vinculada = caja, estado = "GASTOS").exclude(importe_usd = None).values_list("importe_usd", flat=True)))
        balance_usd = ingresos_usd - gastos_usd

        try:

            porcentaje = len(con_principal.filter(caja_vinculada = caja).exclude(importe_usd = None))/len(con_principal.filter(caja_vinculada = caja))*100

        except:

            porcentaje = 100

        aux = 0
        # usuarios_participan = [(datosusuario.objects.get(identificacion = u), aux + 15) for u in usuarios]
        
        total_cajas.append((caja, ingresos, gastos, balance, ingresos_usd, gastos_usd, balance_usd, porcentaje))

    return total_cajas

def cajasAdministras(user):

    con_registros = RegistroContable.objects.all().exclude(usuario = user)
    cajas_participas = con_registros.filter(creador = user).values_list("caja_vinculada__id", flat=True).distinct()

    cajas_administras = []

    for caja in cajas_participas:

        caja =  Cajas.objects.get(id = caja)
        
        ingresos = sum(np.array(con_registros.filter(caja_vinculada = caja, estado = "INGRESOS").values_list("importe", flat=True)))
        gastos = sum(np.array(con_registros.filter(caja_vinculada = caja, estado = "GASTOS").values_list("importe", flat=True)))
        balance = ingresos - gastos
        

        ingresos_usd = sum(np.array(con_registros.filter(caja_vinculada = caja, estado = "INGRESOS").exclude(importe_usd = None).values_list("importe_usd", flat=True)))
        gastos_usd = sum(np.array(con_registros.filter(caja_vinculada = caja, estado = "GASTOS").exclude(importe_usd = None).values_list("importe_usd", flat=True)))
        balance_usd = ingresos_usd - gastos_usd

        try:

            porcentaje = len(con_registros.filter(caja_vinculada = caja).exclude(importe_usd = None))/len(con_registros.filter(caja_vinculada = caja))*100

        except:

            porcentaje = 100

        aux = 0
        # usuarios_participan = [(datosusuario.objects.get(identificacion = u), aux + 15) for u in usuarios]
        
        cajas_administras.append((caja, ingresos, gastos, balance, ingresos_usd, gastos_usd, balance_usd, porcentaje))
    
    return cajas_administras

def recalculoDolarCaja(caja, user_caja):

    con_principal = RegistroContable.objects.filter(caja_vinculada = caja, usuario__identificacion = user_caja, importe_usd = None).order_by("-fecha")

    n = 0

    for consulta in con_principal:
        try:
            arqueo = Arqueo.objects.filter(fecha = consulta.fecha)[0]
            data_frame = pd.read_excel(arqueo.arqueo)
            cambio_usd = data_frame['CAMBIO USD'][0]
            consulta.importe_usd = consulta.importe/float(cambio_usd)
            consulta.save()
            n += 1
        except:
            pass
    
    if n > 0:

        mensaje = f"Se actualizaron {n} registros"

        return mensaje

    else:

        return 0


        
