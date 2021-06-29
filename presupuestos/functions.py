import pandas as pd
import numpy as np
from .models import PresupuestosAlmacenados, Analisis, Articulos

def auditor_presupuesto(fecha_desde, fecha_hasta):
    data_almacenada_desde = PresupuestosAlmacenados.objects.filter(nombre = fecha_desde)[0]
    data_almacenada_hasta = PresupuestosAlmacenados.objects.filter(nombre = fecha_hasta)[0]
    df_desde = pd.read_excel(data_almacenada_desde.archivo)
    df_hasta = pd.read_excel(data_almacenada_hasta.archivo)

    # Estudio de diferencia de cantidades

    df_desde_Q = df_desde.drop(['Precio', 'Monto'], axis = 1)
    df_hasta_Q = df_hasta.drop(['Precio', 'Monto'], axis = 1)
    df_dif_Q = df_hasta_Q.merge(df_desde_Q, how='outer', indicator='union')
    df_dif_Q.drop(df_dif_Q[df_dif_Q['union'] == "both"].index, inplace=True)

    df_dif_Q_desde = df_dif_Q[df_dif_Q['union'] == "left_only"]
    df_dif_Q_hasta = df_dif_Q[df_dif_Q['union'] == "right_only"]

    lista_capitulos_afectado = list(set(df_dif_Q["Capitulo"].values))

    data_procesada = []

    cuantif_q = 0
    errores = 0

    data_capitulo = []

    for capitulo in lista_capitulos_afectado:
        # Primeros los articulos eliminados

        cuantif_q_cap = 0
        errores_cap = 0

        df_dif_Q_desde_aux = df_dif_Q_desde[df_dif_Q_desde['Capitulo'] == capitulo]

        articulos_eliminados = []

        for i in df_dif_Q_desde_aux.index:
            try:
                analisis = Analisis.objects.get(codigo = df_dif_Q_desde_aux['Analisis'][i])
            except:
                analisis = "¿¿"+str(df_dif_Q_desde_aux['Analisis'][i])+"??"
                errores += 1
                errores_cap += 1
            try:
                articulo = Articulos.objects.get(codigo = df_dif_Q_desde_aux['Articulo'][i])
            except:
                articulo = "¿¿"+str(df_dif_Q_desde_aux['Articulo'][i])+"??"

            cantidad = df_dif_Q_desde_aux['Cantidad Art Totales'][i]
            try:
                modif = cantidad*articulo.valor
                cuantif_q -= modif
                cuantif_q_cap -= modif
            except:
                modif = "??"
                errores += 1
                errores_cap += 1

            articulos_eliminados.append((analisis, articulo, cantidad, modif))

        df_dif_Q_hasta_aux = df_dif_Q_hasta[df_dif_Q_hasta['Capitulo'] == capitulo]

        articulos_agregados = []

        for i in df_dif_Q_hasta_aux.index:
            try:
                analisis = Analisis.objects.get(codigo = df_dif_Q_hasta_aux['Analisis'][i])
            except:
                analisis = "¿¿"+str(df_dif_Q_hasta_aux['Analisis'][i])+"??"
                errores += 1
                errores_cap += 1
            try:
                articulo = Articulos.objects.get(codigo = df_dif_Q_hasta_aux['Articulo'][i])
            except:
                articulo = "¿¿"+str(df_dif_Q_hasta_aux['Articulo'][i])+"??"
                

            cantidad = df_dif_Q_hasta_aux['Cantidad Art Totales'][i]
            try:
                modif = cantidad*articulo.valor
                cuantif_q += modif
                cuantif_q_cap += modif
            except:
                modif = "??"
                errores += 1
                errores_cap += 1

            articulos_agregados.append((analisis, articulo, cantidad, modif))
        
        data_capitulo.append((capitulo, articulos_agregados, articulos_eliminados, cuantif_q_cap, errores_cap))
        
    data_procesada.append((data_capitulo, cuantif_q, errores))

    return data_procesada

