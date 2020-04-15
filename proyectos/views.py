from django.shortcuts import render
from .models import Proyectos

# Create your views here.

def proyectos(request):

    datos = Proyectos.objects.all()

    return render(request, 'proyectos.html', {'datos':datos})