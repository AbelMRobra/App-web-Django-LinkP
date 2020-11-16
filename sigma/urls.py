from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA CONSTANTES -----------------------------------------
    url(r'^inventario/$', login_required(views.inventario), name = 'Inventario'),
    url(r'^tareas/$', login_required(views.tareas), name = 'tareas'),
    url(r'^creartareas/$', login_required(views.cargartarea), name = 'Crear tareas'),
    url(r'^crearsubtareas/(?P<id_tarea>\d+)/$', login_required(views.cargarsubtarea), name = 'Crear subtareas'),
    url(r'^eliminartarea/(?P<id_tarea>\d+)/$', login_required(views.eliminartarea), name = 'Eliminar tarea'),
    url(r'^eliminarsubtarea/(?P<id_subtarea>\d+)/$', login_required(views.eliminarsubtarea), name = 'Eliminar subtarea'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^partediario/(?P<dni>\d+)/$', views.partesdiarios, name = 'Parte diarios'),
    url(r'^cargarparte/(?P<dni>\d+)/$', views.cargarpartediario, name = 'Cargar parte'),


]