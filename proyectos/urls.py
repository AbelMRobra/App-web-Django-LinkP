from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.proyectos), name = 'Proyectos'),
    url(r'^unidades$', login_required(views.unidades), name = 'Unidades'),
    url(r'^adminunidades$', login_required(views.adminunidades), name = 'Admin unidades')

]