from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.CrearListaComputos), name = 'Planilla de computos'),
    url(r'^lista/$', login_required(views.listacomputos), name = 'Lista de computos'),
    url(r'^resumen/$', login_required(views.resumencomputos), name = 'Resumen de computos'),

]