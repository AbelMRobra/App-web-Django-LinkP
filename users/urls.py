from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.welcome, name = 'Bienvenido'),
    url(r'^guia$', login_required(views.guia), name = 'Guia'),
    url(r'^canjemoneda$', login_required(views.canjemonedas), name = 'Canje de monedas'),
    url(r'^moneda$', views.monedalink, name = 'Moneda Link'),
    url(r'^register$', views.register, name = 'Registro'),
    url(r'^login$', views.login, name = 'Login'),
    url(r'^logout$', views.logout, name = 'Logout'),
    url(r'^inicio$', login_required(views.inicio), name = 'Inicio'),
    url(r'^accounts/login/$', views.welcome, name = 'Redicrección'),
    url(r'^dashboard$', views.dashboard, name = 'Dashboard'),
    url(r'^password$', login_required(views.password), name = 'Password'),
    url(r'^vacaciones$', login_required(views.vacaciones), name = 'Holidays'),
    url(r'^informes$', login_required(views.informes), name = 'Informes'),
    url(r'^informescrear$', login_required(views.informescrear), name = 'Informes crear'),
    url(r'^verinformes/(?P<id_informe>\d+)/$', login_required(views.verinforme), name = 'Ver informes'),
    url(r'^tablerorega/(?P<id_proyecto>\d+)/(?P<id_area>\d+)/(?P<id_estado>\d+)/$', login_required(views.tablerorega), name = 'Tablero Rega'),
    url(r'^tableroregaadd$', login_required(views.tableroregaadd), name = 'Tablero Rega Add'),

    # Templates de anuncis

    url(r'anuncios$', login_required(views.anuncios), name = 'Anuncios'),

    # Templates de minutas

    url(r'minutas$', login_required(views.minutas), name = 'Minutas Listas'),
    url(r'minutascrear$', login_required(views.minutascrear), name = 'Minutas Crear'),
    url(r'minutasmodificar/(?P<id_minuta>\d+)/$', login_required(views.minutasmodificar), name = 'Minutas Modificar'),
    url(r'minutasid/(?P<id_minuta>\d+)/$', login_required(views.minutasid), name = 'Minutas Id'),

]