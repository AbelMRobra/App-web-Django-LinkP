from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import AgendaForm
from .models import Agenda
from .filters import ArticulosFilter
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

# La pagina inicial

def insumos(request):

    return render(request, 'age/insumos.html')

    
def insum_create(request):

    #Si el metodo es POST activa la funciones para guardar los datos del formulario

    if request.method == 'POST':

        #Aqui guardo los datos para ingresar el formulario

        form = AgendaForm(request.POST)

        #Aqui guardo los datos de los inputs

        datos = request.POST.items()

        for key, value in datos:

            if key == 'codigo':

                #Aqui solamente me quedo con el codigo
                codigo = (value)

            if key == 'constante':

                #Aqui solamente me quedo con el codigo
                constante = (value)

            if key == 'valor':

                #Aqui solamente me quedo con el codigo
                valor = (value)

        #Aqui pruebo si el formulario es correcto

        if form.is_valid():
            
            form.save()
        
        #Me conecto a la base de datos y traigo el valor de la constante

        query = 'SELECT valor FROM constantes_constantes WHERE id = (?)'

        parametro = str(constante)

        conn = Conectar_db()

        datos_con = conn.run_db(query, parametro)

        for i in datos_con:
            valor_constante = i

        print(valor_constante[0])

        #Opero para sacar el valor auxiliar 

        valor_aux = (int(valor)/(int(valor_constante[0])))
        

        #Me conecto a la base de datos y subo el valor auxiliar

        query = 'UPDATE age_agenda SET valor_aux = (?) WHERE codigo = (?)'

        parametro = (valor_aux, codigo)

        conn = Conectar_db()

        datos_con = conn.run_db(query, parametro)

        return redirect('Lista de insumos')
        
    else:
        form = AgendaForm()

    f = {'form':form}


    return render(request, 'age/insum_create.html', f )

def insum_list(request):

    agenda_actual = Agenda.objects.all()

    for i in agenda_actual:
        print(i.nombre)
        print(i.valor)

    myfilter = ArticulosFilter(request.GET, queryset=agenda_actual)

    agenda_actual = myfilter.qs

    c = {'agenda':agenda_actual, 'myfilter':myfilter}

    return render(request, 'age/insum_list.html', c )

def insum_edit(request, id_agenda):

    agen = Agenda.objects.get(codigo=id_agenda)

    if request.method == 'GET':
        form = AgendaForm(instance = agen)
    else:
        form = AgendaForm(request.POST, instance = agen)
        if form.is_valid():
            form.save()
        return redirect('Lista de insumos')
    return render(request, 'age/insum_create.html', {'form':form})

def insum_delete(request, id_agenda):

    agen = Agenda.objects.get(codigo=id_agenda)

    if request.method == 'POST':
        agen.delete()
        return redirect('Lista de insumos')
    return render(request, 'age/insum_delete.html', {'agen':agen})






