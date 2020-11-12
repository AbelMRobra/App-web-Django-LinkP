from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA CONSTANTES -----------------------------------------
    url(r'^inventario/$', login_required(views.inventario), name = 'Inventario'),
    url(r'^tareas/$', login_required(views.tareas), name = 'tareas'),


]