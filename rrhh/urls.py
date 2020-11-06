from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA FIANANZAS -----------------------------------------
    url(r'^notasdepedido/$', login_required(views.notasdepedido), name = 'Notas de pedido'),
    url(r'^notadepedido/(?P<id_nota>\d+)/$', login_required(views.notadepedido), name = 'Nota de pedido'),


]