from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import ConsForm
from .models import Constantes
from age.models import Agenda
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

                    cons_valor_nuevo = (value)

            datos_constante = Constantes.objects.all()

            for i in datos_constante:
                if str(i.nombre) == str(nombre):
                    
                    cons_nombre = i.nombre

                    cons_valor = i.valor


                    form.save()

            datos_insumos = Agenda.objects.all()

            for i in datos_insumos:

                if str(i.constante) == str(cons_nombre):
                    valor_actual = i.valor

                    valor_nuevo = valor_actual*(float(cons_valor_nuevo)/cons_valor) 

                    i.valor = valor_nuevo

                    i.save()

        return redirect('Cons_list')
    
    return render(request, 'constantes/cons_create.html', {'form':form})

def cons_delete(request, id_cons):

    cons = Constantes.objects.get(id=id_cons)

    if request.method == 'POST':
        cons.delete()
        return redirect('Cons_list')
    return render(request, 'constantes/cons_delete.html', {'cons':cons})