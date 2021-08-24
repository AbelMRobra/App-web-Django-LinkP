from rrhh.models import datosusuario, RegistroContable
from datetime import datetime, date, timedelta
import numpy as np

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
            sigma_blanco = sum(np.array(consulta_usuario.filter(categoria = "INGRESOS SIGMA", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").exclude(nota__contains = "SHAJOR").values_list("importe", flat=True)))
            azlepi_shajor =  sum(np.array(consulta_usuario.filter(categoria = "INGRESOS AZLEPI", nota__contains = "SHAJOR", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").values_list("importe", flat=True)))
            azlepi_blanco = sum(np.array(consulta_usuario.filter(categoria = "INGRESOS AZLEPI", fecha__range = (fecha_inicial_auxiliar, fecha_final), estado = "INGRESOS").exclude(nota__contains = "SHAJOR").values_list("importe", flat=True)))
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

        
