from django.shortcuts import render, redirect

from .models import Consulta ,get_medios
from ventas.models import Clientescontacto, VentasRealizadas
from .models import Proyectos
from rrhh.models import datosusuario
from django.db import IntegrityError
from .forms import FormCrearConsulta
from django.views.generic import CreateView,UpdateView,DetailView
from django.urls import reverse_lazy

# Create your views here.


def clientes(request):
    clientes=Clientescontacto.objects.filter(activo=True)
    mensaje=''

    if request.method=='POST':
        datos={}
        for dato in request.POST:
            datos[dato]=request.POST[dato]
        try:
            if 'agregar' in datos:
            
                cliente=Clientescontacto(
                    nombre=datos['nombre'],
                    apellido=datos['apellido'],
                    email=datos['email'],
                    telefono=datos['telefono'],
                )
                cliente.save()
                return redirect('clientes')

        except:
            mensaje='No se pudo crear el cliente,recuerde que no se puede agregar dos clientes con el mismo email'
    
        if 'eliminar' in datos:
        
            id_cliente=int(datos['eliminar'])
            cliente=Clientescontacto.objects.get(pk=id_cliente)
            cliente.activo=False
            cliente.save()
            return redirect('clientes')
        
            mensaje='No se pudo eliminar el cliente'

    
    return render(request,"clientes.html",{'mensaje':mensaje,'clientes':clientes})

    
def estadisticas(request):
    return render(request, "crm_estadisticas.html")

def modificarcliente(request,**kwargs):

    
    id_cliente=kwargs['id']
    mensaje=""

    cliente=Clientescontacto.objects.get(pk=id_cliente)
    consultas = Consulta.objects.filter(cliente = cliente).order_by("-fecha")
    ventas = VentasRealizadas.objects.filter(cliente = cliente)
    if request.method=='POST':
        datos={}
        try:
            for dato in request.POST:
                datos[dato]=request.POST[dato]
            
            if cliente:
            
                cliente.nombre=datos['nombre']
                cliente.apellido=datos['apellido']
                cliente.email=datos['email']
                cliente.telefono=datos['telefono']
                cliente.save()
                return redirect('modificarcliente', cliente.id)
        except:
            mensaje='No se pudo actualizar el cliente, recuerde que dos clientes no pueden tener el mismo email'

    return render(request,"modificarcliente.html",{'mensaje':mensaje, 'cliente': cliente, 'consultas':consultas})

class crearconsulta(CreateView):
    
    form_class=FormCrearConsulta
    template_name='crearconsulta.html'
    success_url=reverse_lazy('crearconsulta')

    def get_context_data(self, **kwargs):
        context = super(crearconsulta, self).get_context_data(**kwargs)
        medios=get_medios()
        
        context['medios']=medios
        context['clientes']=Clientescontacto.objects.filter(activo=True)
        context['proyectos']=Proyectos.objects.all()

        context['consultas']=Consulta.objects.all()
       
        return context

    def post(self, request, *args, **kwargs):
        form = FormCrearConsulta(request.POST)
       
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.usuario=datosusuario.objects.get(identificacion=request.user)
            consulta.save()
            form.save_m2m()
            return redirect('crearconsulta')
        return render(request, 'crearconsulta.html', {"consultas": Consulta.objects.all()})


def eliminarconsulta(request):
    if request.method=='POST':
        id_consulta=request.POST.get('eliminar')
        consulta=Consulta.objects.get(pk=id_consulta)
        consulta.delete()
    
        return redirect('crearconsulta')