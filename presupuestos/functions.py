import pandas as pd
import numpy as np
from .models import PresupuestosAlmacenados, Analisis, Articulos

def auditor_presupuesto(proyecto,fecha_desde, fecha_hasta):
    #esta linea trae 29 objetos
    
    print('fecha y proyecto ',proyecto,fecha_desde)
    data_almacenada_desde_objects = PresupuestosAlmacenados.objects.filter(nombre = fecha_desde,proyecto=proyecto)
    
    #esta linea da error porque el queryset se encuentra vacio
    data_almacenada_hasta_objects = PresupuestosAlmacenados.objects.filter(nombre = fecha_hasta,proyecto=proyecto)
    
    print(data_almacenada_desde_objects,data_almacenada_hasta_objects)
    if data_almacenada_desde_objects.exists() and data_almacenada_hasta_objects.exists():
        
        data_almacenada_desde=data_almacenada_desde_objects[0]
        data_almacenada_hasta=data_almacenada_hasta_objects[0]

        df_desde = pd.read_excel(data_almacenada_desde.archivo)
        df_hasta = pd.read_excel(data_almacenada_hasta.archivo)

        
        # Estudio de diferencia de cantidades

        valor_proyecto_desde=sum(list(df_desde['Monto'].values))
        valor_proyecto_hasta=sum(list(df_hasta['Monto'].values))

        

        df_desde_Q = df_desde.drop(['Precio', 'Monto'], axis = 1) #se eliminan
        df_hasta_Q = df_hasta.drop(['Precio', 'Monto'], axis = 1) #se eliminan

        
        df_dif_Q = df_hasta_Q.merge(df_desde_Q, how='outer', indicator='union')
        df_dif_Q.drop(df_dif_Q[df_dif_Q['union'] == "both"].index, inplace=True) #se unen
        
        df_dif_Q_desde = df_dif_Q[df_dif_Q['union'] == "left_only"]
        df_dif_Q_hasta = df_dif_Q[df_dif_Q['union'] == "right_only"]

        
        lista_capitulos_afectado = list(set(df_dif_Q["Capitulo"].values)) #set elimina los nombres de ls capitulos repetidos

        data_procesada = []

        cuantif_q = 0
        errores = 0
        
        data_capitulo = []
        print('ANTES DEL FOR')
        print(lista_capitulos_afectado)
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
                    print('entra al segundo try')
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
        print('agrega la data procesada')
        data_procesada.append((data_capitulo, cuantif_q, errores))

        
        
    else:
        data_procesada=None
        mensaje='No se encontraron registros en esa fecha para ese proyecto'      
    mensaje='hola'
    print('data procesada',data_procesada)
    return data_procesada,mensaje


def auditor_presupuesto_p(proyecto,fecha_desde, fecha_hasta):

    cont=0
    data_almacenada_desde_objects = PresupuestosAlmacenados.objects.filter(nombre = '2021-05-18',proyecto=proyecto)
    
    #esta linea da error porque el queryset se encuentra vacio
    data_almacenada_hasta_objects = PresupuestosAlmacenados.objects.filter(nombre = '2021-05-19',proyecto=proyecto)
    
    if data_almacenada_desde_objects.exists() and data_almacenada_hasta_objects.exists():
        
        
        data_almacenada_desde=data_almacenada_desde_objects[0]
        data_almacenada_hasta=data_almacenada_hasta_objects[0]

        df_desde = pd.read_excel(data_almacenada_desde.archivo)

        valor_desde=sum(list(df_desde['Monto'].values))
        df_hasta = pd.read_excel(data_almacenada_hasta.archivo)

        articulos_M2={}
        dif_articulos={}

        for art in df_hasta.index:
            
            #de la columna 'articulos' toma los registros con el codigo de cada fila
            articulos_M2[df_hasta['Articulo'][art]]=df_hasta['Precio'][art]

        df_desde_m2=df_desde
        
        for i in df_desde_m2.index:
        #try:

            dif_articulos[df_desde_m2['Articulo'][i]]=(articulos_M2[df_desde_m2['Articulo'][i]]/df_desde_m2['Monto'][i]-1)*100


            df_desde_m2['Precio'][i]=articulos_M2[df_desde_m2['Articulo'][i]]

            

            df_desde_m2['Monto'][i]=articulos_M2[df_desde_m2['Articulo'][i]]*df_desde_m2['Cantidad Art Totales'][i]
        #except:
            #cont=cont+1
        print(dif_articulos)
        valor_desde_m2=sum(list(df_desde_m2['Monto'].values))

        

        dif_P=valor_desde_m2-valor_desde

        print('DIFERENCIA',dif_P)

       


    
    return None


'''

        for capitulo in lista_capitulos_afectado:
            # Primeros los articulos eliminados
            print('entra al for')
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
                    print('entra al segundo try')
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
        print('agrega la data procesada')
        data_procesada.append((data_capitulo, cuantif_q, errores))

        
        
    else:
        data_procesada=None
        mensaje='No se encontraron registros en esa fecha para ese proyecto'      
    mensaje='hola'
    print('data procesada',data_procesada)
    return data_procesada,mensaje,valor_proyecto_desde,valor_proyecto_hasta'''