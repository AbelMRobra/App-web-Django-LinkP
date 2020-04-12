from django.shortcuts import render
from .models import Proveedores
from .models import StockComprasAnticipadas
from .form import StockAntForm
import sqlite3

# Esta es el objeto para conectar con la base de datos y hacer consultas

class Conectar_db():
    nombre_db = 'db.sqlite3'

    def run_db(self, query, parametros = ()):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            datos = cursor.execute(query, parametros)

            conn.commit()

        return datos

# Create your views here.

def stockant_ingresar(request):

    if request.method == 'POST':

        datos = request.POST.items()

        for i in datos:
            print(i)


    else:

        query = "SELECT nombre FROM age_agenda"

        conn = Conectar_db()

        datos_con = conn.run_db(query,)

        lista_datos = {'key': 0, 'nombre': 'ninguno' }

        valor = 0

        for i in datos_con:

            valor = valor + 1

            lista_datos['key'] = valor

            lista_datos['nombre'] = i[0]

            print(lista_datos)

        datos_enviados = lista_datos

    return render(request, 'stockant_ingresar.html', {'datos_enviados':datos_enviados })

def proveedores(request):

    datos = Proveedores.objects.all()

    return render(request, 'proveedores.html', {'datos':datos})

def stockant(request):

    datos = StockComprasAnticipadas.objects.all()

    return render(request, 'stockant.html', {'datos':datos})
