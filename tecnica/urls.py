from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [ 
    url(r'^documentacion$', login_required(views.documentacion), name = 'Documentacion'),
    url(r'^editaritem/(?P<id_item>\d+)/$', login_required(views.editaritem), name = 'Editar Item'), 
    url(r'^gantt/(?P<id_proyecto>\d+)/$', login_required(views.ganttet), name = 'Gantt ET'), 
    url(r'^mensajeitem/(?P<id_item>\d+)/$', login_required(views.mensajesitem), name = 'Mensaje item'), 

]