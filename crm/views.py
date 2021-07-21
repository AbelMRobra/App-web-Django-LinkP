from django.shortcuts import render, redirect
from django.template import context
from operator import itemgetter, attrgetter
from .models import Consulta ,get_medios, Tipologia
from ventas.models import Clientescontacto, VentasRealizadas
from .models import Proyectos
from rrhh.models import datosusuario
from django.db import IntegrityError
from .forms import FormCrearConsulta
from django.views.generic import CreateView,UpdateView,DetailView
from django.urls import reverse_lazy
from .functions import generarcolores

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

    meses = {
        'Enero':0,
        'Febrero':0,
        'Marzo':0,
        'Abril':0,
        'Mayo':0,
        'Junio':0,
        'Julio':0,
        'Agosto':0,
        'Septiembre':0,
        'Octubre':0,
        'Noviembre':0,
        'Diciembre':0

    }


    n = 0
    for i in meses.keys():
        consultas_mes = len(Consulta.objects.filter(fecha__month = n))
        meses[i] = consultas_mes
        n+=1

    list_medio_contacto = Consulta.objects.values_list("medio_contacto", flat = True).distinct()
    medios = []
    for m in list_medio_contacto:
        cant = len(Consulta.objects.filter(medio_contacto = m))
        medios.append((m, cant))

    clientes = len(Clientescontacto.objects.all())
    consultas = len(Consulta.objects.all())
    ventas = len(VentasRealizadas.objects.all().exclude(cliente = None))

    #OBTENCION DE COLORES
    colores_template=generarcolores(len(medios))

    medios = sorted(medios, key=itemgetter(1), reverse=True)
    return render(request, "crm_estadisticas.html", {'medios':medios, 'meses':meses, 'ventas':ventas, 'clientes':clientes, 'consultas':consultas,'colores':colores_template})
def modificarcliente(request,**kwargs):

    id_cliente=kwargs['id']
    mensaje=""
    proyectos = Proyectos.objects.order_by("fecha_f").exclude(fecha_i = None)
    cliente=Clientescontacto.objects.get(pk=id_cliente)
    consultas = Consulta.objects.filter(cliente = cliente).order_by("-fecha")
    ventas = VentasRealizadas.objects.filter(cliente = cliente).order_by("-fecha")
    medios = get_medios()
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

    return render(request,"modificarcliente.html",{'proyectos':proyectos, 'medios':medios, 'mensaje':mensaje, 'cliente': cliente, 'consultas':consultas, 'ventas':ventas, "tipologias":Tipologia.objects.all()})

class crearconsulta(CreateView):
    
    form_class=FormCrearConsulta
    template_name='crearconsulta.html'
    success_url=reverse_lazy('crearconsulta')

    def get_context_data(self):

        #context = super(crearconsulta, self).get_context_data(**kwargs)
        context = {}
        context['medios']=get_medios()
        context['clientes']=Clientescontacto.objects.filter(activo=True)
        context['proyectos']=Proyectos.objects.all()
        context["tipologias"]=Tipologia.objects.all()
        context['consultas']=Consulta.objects.all()
       
        return context

    def post(self, request, *args, **kwargs):
        
        form = FormCrearConsulta(request.POST)
        
        try:
            proyecto = Proyectos.objects.get(pk=int(request.POST["proyecto"]))
            proyecto_no_est = None
        
        except:
            proyecto = None
            proyecto_no_est=request.POST["proyecto_no_est"]

        id_cliente=request.POST['cliente'].split("-")[0]
        cliente=Clientescontacto.objects.get(pk=int(id_cliente))


        try:
            archivo=request.FILES['adjunto_propuesta']
        except:
            archivo=None
       

        consulta=Consulta.objects.create(
            proyecto = proyecto,
            proyecto_no_est = proyecto_no_est,
            usuario = datosusuario.objects.get(identificacion=request.user),
            adjunto_propuesta = archivo,
            cliente=cliente,
            fecha=request.POST.get('fecha'),
            medio_contacto=request.POST.get('medio_contacto'),
        )


        datos_post = request.POST.getlist("tipologia2")
        
        for dato in datos_post:

            tip=Tipologia.objects.get(pk=int(dato))
            consulta.tipologia2.add(tip)
            consulta.save()
    
        try: 
            perfil_cliente=request.POST.get('perfilcliente')
            
            if perfil_cliente:
                return redirect('modificarcliente',cliente.id)
        except:

            pass

        context = self.get_context_data()     
        return render(request, 'crearconsulta.html', context)


def eliminarconsulta(request):
    if request.method=='POST':
        id_consulta=request.POST.get('eliminar')
        consulta=Consulta.objects.get(pk=id_consulta)
        consulta.delete()
    
        return redirect('crearconsulta')