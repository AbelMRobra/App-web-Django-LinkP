from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [ 
    url(r'^documentacion$', login_required(views.documentacion), name = 'Documentacion'),
    url(r'^editaritem/(?P<id_item>\d+)/$', login_required(views.editaritem), name = 'Editar Item'), 
    url(r'^eliminaritem/(?P<id_item>\d+)/$', login_required(views.eliminaritem), name = 'Borrar Item'), 
    url(r'^agregaritem/(?P<id_etapa>\d+)/$', login_required(views.agregaritem), name = 'Agregar Item'), 
    url(r'^gantt/(?P<id_proyecto>\d+)/$', login_required(views.ganttet), name = 'Gantt ET'), 
    url(r'^mensajeitem/(?P<id_item>\d+)/$', login_required(views.mensajesitem), name = 'Mensaje item'),
    url(r'^subitem/(?P<id_item>\d+)/$', login_required(views.subitem), name = 'Sub item'), 
    url(r'^agregarsubitem/(?P<id_item>\d+)/$', login_required(views.agregarsubitem), name = 'Agregar Subitem'), 

]