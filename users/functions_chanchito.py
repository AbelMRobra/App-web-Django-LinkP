from rrhh.models import datosusuario, RegistroContable
from finanzas.models import Arqueo
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd

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

    for usuario in list:

        usuario = datosusuario.objects.get(identificacion = usuario)

        consulta_usuario = consulta_principal.filter(usuario = usuario)

        ingresos_mensuales = []

        for fecha in  fechas_totales:

            if fecha.month == 12:
                fecha_final = date(fecha.year + 1, 1, 1)
            else:
                fecha_final = date(fecha.year, fecha.month + 1, 1)

            fecha_inicial_auxiliar = fecha - timedelta(days=1)

            comercial_shajor = sum(np.array(consulta_usuario.filter(categoria = "INGRESO SUELDOS COMERCIAL", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").values_list("importe", flat=True)))
            sigma_shajor =  sum(np.array(consulta_usuario.filter(categoria = "INGRESOS SIGMA", nota__contains = "SHAJOR", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").values_list("importe", flat=True)))
            sigma_blanco = sum(np.array(consulta_usuario.filter(categoria = "INGRESOS SIGMA", nota__contains = "BANCO", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").exclude(nota__contains = "SHAJOR").values_list("importe", flat=True)))
            azlepi_shajor =  sum(np.array(consulta_usuario.filter(categoria = "INGRESOS AZLEPI", nota__contains = "SHAJOR", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").values_list("importe", flat=True)))
            azlepi_blanco = sum(np.array(consulta_usuario.filter(categoria = "INGRESOS AZLEPI", nota__contains = "BANCO", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").exclude(nota__contains = "SHAJOR").values_list("importe", flat=True)))
            total = comercial_shajor + sigma_shajor + sigma_blanco + azlepi_shajor + azlepi_blanco

            ingresos_mensuales.append((comercial_shajor, sigma_shajor, sigma_blanco, azlepi_shajor, azlepi_blanco, total))

        context['datos'][usuario.identificacion] = ingresos_mensuales

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

    consulta_principal = RegistroContable.objects.filter(usuario = user)

    cajas_usuario = list(set(consulta_principal.values_list("caja", flat=True).order_by("-fecha").distinct()))

    total_cajas = []

    for caja in cajas_usuario:

        con_caja = consulta_principal.filter(caja = caja)
        
        nombre = caja
        ingresos = sum(np.array(con_caja.filter(estado = "INGRESOS").values_list("importe", flat=True)))
        gastos = sum(np.array(con_caja.filter(estado = "GASTOS").values_list("importe", flat=True)))
        balance = ingresos - gastos
        automatico = sum(np.array(con_caja.filter(nota__contains = "AUTO-").values_list("importe", flat=True)))
        usuarios = con_caja.values_list('creador', flat = True).distinct()

        ingresos_usd = sum(np.array(con_caja.filter(estado = "INGRESOS").exclude(importe_usd = None).values_list("importe_usd", flat=True)))
        gastos_usd = sum(np.array(con_caja.filter(estado = "GASTOS").exclude(importe_usd = None).values_list("importe_usd", flat=True)))
        balance_usd = ingresos_usd - gastos_usd

        try:

            porcentaje = len(con_caja.filter(caja = caja).exclude(importe_usd = None))/len(con_caja.filter(caja = caja))*100

        except:

            porcentaje = 100

        aux = 0
        usuarios_participan = [(datosusuario.objects.get(identificacion = u), aux + 15) for u in usuarios]
        
        total_cajas.append((nombre, ingresos, gastos, balance, usuarios_participan, automatico, ingresos_usd, gastos_usd, balance_usd, porcentaje))

    return total_cajas

def cajasAdministras(user):

    con_general = RegistroContable.objects.all()
    consulta_principal = RegistroContable.objects.filter(creador = user)
    cajas_administradas = list(set(consulta_principal.exclude(usuario = user).values_list("caja", flat=True).order_by("-fecha").distinct()))
    usuarios_cajas = list(set(consulta_principal.exclude(usuario = user).values_list("usuario", flat=True).order_by("-fecha").distinct()))
    cajas_administras = []

    for usuario in usuarios_cajas:
        user_adm = datosusuario.objects.get(id = usuario)
        
        for caja in cajas_administradas:
            if len(consulta_principal.filter(usuario = user_adm, caja = caja).exclude(usuario = user)):
                usuarios_participan = []
                nombre = caja
                ingresos = sum(np.array(con_general.filter(usuario = user_adm, estado = "INGRESOS", caja = caja).values_list("importe", flat=True)))
                gastos = sum(np.array(con_general.filter(usuario = user_adm, estado = "GASTOS", caja = caja).values_list("importe", flat=True)))
                balance = ingresos - gastos
                automatico = sum(np.array(con_general.filter(usuario = user_adm, nota__contains = "AUTO-", caja = caja).values_list("importe", flat=True)))
                usuarios_v = con_general.filter(usuario = user_adm, caja = caja).values_list('creador', flat = True).distinct()
                
                ingresos_usd = sum(np.array(con_general.filter(usuario = user_adm, estado = "INGRESOS", caja = caja).exclude(importe_usd = None).values_list("importe_usd", flat=True)))
                gastos_usd = sum(np.array(con_general.filter(usuario = user_adm, estado = "GASTOS", caja = caja).exclude(importe_usd = None).values_list("importe_usd", flat=True)))
                balance_usd = ingresos_usd - gastos_usd

                porcentaje = len(consulta_principal.filter(usuario = user_adm, caja = caja).exclude(importe_usd = None))/len(consulta_principal.filter(usuario = user_adm, caja = caja))*100

                aux = 0
                for u in usuarios_v:
                    user_aux = datosusuario.objects.get(identificacion = u)
                    usuarios_participan.append((user_aux, aux))
                    aux += 15

                cajas_administras.append((nombre, ingresos, gastos, balance, user_adm, usuarios_participan, automatico, ingresos_usd, gastos_usd, balance_usd, porcentaje))

    return cajas_administras

def recalculoDolarCaja(caja, user_caja):

    con_principal = RegistroContable.objects.filter(caja = caja, usuario__identificacion = user_caja, importe_usd = None).order_by("-fecha")

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


        
