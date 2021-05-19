from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA FIANANZAS -----------------------------------------
    url(r'^notasdepedido/(?P<id_proyecto>\d+)/(?P<tipo>\d+)/$', login_required(views.notasdepedido), name = 'Notas de pedido'),
    url(r'^notadepedido/(?P<id_nota>\d+)/$', login_required(views.notadepedido), name = 'Nota de pedido'),
    url(r'^crearcorres/$', login_required(views.crearcorrespondencia), name = 'Crear correspondencia'),
    url(r'^datospersonal/$', login_required(views.datospersonal), name = 'Datos personal'),
    url(r'^apprrhh/$', login_required(views.apprrhh), name = 'App de rrhh'),
    url(r'^editarcorres/(?P<id_nota>\d+)/$', login_required(views.editarcorrespondencia), name = 'Editar correspondencia'),


]