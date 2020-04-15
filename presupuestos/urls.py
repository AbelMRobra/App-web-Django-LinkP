from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^datos/$', login_required(views.proyectos), name = 'Datos de proyectos'),
    url(r'^desde/$', login_required(views.desde), name = 'Indicador de precios'),
    url(r'^parametros/$', login_required(views.parametros), name = 'Parametros'),
    url(r'^cons_list/$', login_required(views.cons_list), name = 'Cons_list'),
    url(r'^cons_create/$', login_required(views.cons_create), name = 'Cons_create'),    
    url(r'^cons_editar/(?P<id_cons>\d+)/$', login_required(views.cons_edit), name = 'Editar_cons'),
    url(r'^cons_eliminar/(?P<id_cons>\d+)/$', login_required(views.cons_delete), name = 'Eliminar_cons'),
    url(r'^insum_list/$', login_required(views.insum_list), name = 'Lista de insumos'),
    url(r'^insumcreate/$', login_required(views.insum_create), name = 'Crear insumo'),
    url(r'^insum_editar/(?P<id_articulos>\d+)/$', login_required(views.insum_edit), name = 'Editar_insumo'),
    url(r'^insum_eliminar/(?P<id_articulos>\d+)/$', login_required(views.insum_delete), name = 'Eliminar_insumo')

]