from django.shortcuts import render
from django.utils.html import escape
from .models import Proyectos
from .models import Certificados
from .filters import CertificadoFilter

# Create your views here.

def certificados(request):

    datos = Certificados.objects.all()

    myfilter = CertificadoFilter(request.GET, queryset=datos)

    datos = myfilter.qs

    datos_enviados = {'datos':datos, 'myfilter':myfilter}

    return render(request, 'certificados.html', datos_enviados )

def projects(request):

    datos = Proyectos.objects.all()

    return render(request, 'projects.html', {'datos':datos})


