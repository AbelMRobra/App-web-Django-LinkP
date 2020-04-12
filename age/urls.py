from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.insumos), name = 'Agenda'),
    url(r'^insum_list/$', login_required(views.insum_list), name = 'Lista de insumos'),
    url(r'^insumcreate/$', login_required(views.insum_create), name = 'Crear insumo'),
    url(r'^editar/(?P<id_agenda>\d+)/$', login_required(views.insum_edit), name = 'Editar_insumo'),
    url(r'^eliminar/(?P<id_agenda>\d+)/$', login_required(views.insum_delete), name = 'Eliminar_insumo')
]