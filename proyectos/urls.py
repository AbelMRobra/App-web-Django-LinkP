from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.proyectos), name = 'Proyectos'),
    url(r'^unidades$', login_required(views.unidades), name = 'Unidades'),
    url(r'^adminunidades$', login_required(views.adminunidades), name = 'Admin unidades'),
    path('cargaunidadesproyecto/<int:id>',login_required(views.cargaunidadesproyecto),name='Carga unidades proyecto'),
    path('listaunidadesproyecto/<int:id>',login_required(views.listaunidadesproyecto),name='Lista unidades proyecto'),
    # path('panelunidadesproyecto/',login_required(views.panelunidadesproyecto),name='Panel unidades proyecto'),

]