from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import ConsForm
from .models import Constantes
import sqlite3

#Objeto que conecta a la base de datos

class Conectar_db():
    nombre_db = 'db.sqlite3'

    def run_db(self, query, parametros = ()):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            datos = cursor.execute(query, parametros)
            conn.commit()
        return datos
    
# Create your views here.

def cons_create(request):

    if request.method == 'POST':
        form = ConsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('Cons_list')
        
    else:
        form = ConsForm()

    f = {'form':form}
    return render(request, 'constantes/cons_create.html', f )

def cons_list(request):

    cons_actuales = Constantes.objects.all()
    c = {'constantes':cons_actuales}
    return render(request, 'constantes/cons_list.html', c )

def cons_edit(request, id_cons):

    cons = Constantes.objects.get(id=id_cons)

    if request.method == 'GET':
        form = ConsForm(instance = cons)
    else:
        form = ConsForm(request.POST, instance = cons)
        if form.is_valid():

            # Rescato el nombre y el valor nuevo de la constante

            datos = request.POST.items()

            for key, value in datos:

                if key == 'nombre':

                    nombre = (value)
                    
                if key == 'valor':

                    valor_nuevo = (value)

            #Me conecto a la base de datos y traigo el ID de la constante

            query = 'SELECT valor, id FROM constantes_constantes WHERE nombre = (?)'

            parametro = (str(nombre),)

            conn = Conectar_db()

            datos_con = conn.run_db(query, parametro)

            for i in datos_con:

                codigo_id = i[1]
                valor_ant = i[0]

            # Guardo los datos del formulario

            form.save()

            #Me conecto a la base de datos y traigo a todos los articulos que tengan ese codigo

            query = 'SELECT * FROM age_agenda WHERE constante_id = (?)'

            parametro = (codigo_id,)

            conn = Conectar_db()

            consulta = conn.run_db(query, parametro)

            datos_con = []

            for i in consulta:

                datos_con.append(i)

            for i in datos_con:

                codigo = i[0]
                valor_articulo_ant = i[2]

                conn = Conectar_db()

                #constantes para la operación
                
                valor1 = float(valor_articulo_ant)
                valor2 = float(valor_nuevo)
                valor3 = float(valor_ant)
                valor_articulo_nuevo = valor1*(valor2/valor3)

                # Armamos los parametros

                parametro = (valor_articulo_nuevo, codigo) 

                print(parametro)

                #Mandamos la consulta para que cargue los datos

                query = 'UPDATE age_agenda SET valor = (?) WHERE codigo = (?)'

                conn = Conectar_db()
           
                datos_con = conn.run_db(query, parametro)

                print("cargo el valor")

        return redirect('Cons_list')
    
    return render(request, 'constantes/cons_create.html', {'form':form})

def cons_delete(request, id_cons):

    cons = Constantes.objects.get(id=id_cons)

    if request.method == 'POST':
        cons.delete()
        return redirect('Cons_list')
    return render(request, 'constantes/cons_delete.html', {'cons':cons})