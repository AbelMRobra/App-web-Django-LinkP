from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from . import views_sugerencias
from . import views_chanchito
from . import views_linkcoins
from .views import PdfMinutas
from .views_chanchito import DescargarRegistroContable
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.welcome, name = 'Bienvenido'),
    url(r'^guia$', login_required(views.guia), name = 'Guia'),
    url(r'^linkp$', login_required(views.linkp), name = 'Link P'),
    url(r'^canjemoneda$', login_required(views_linkcoins.canjemonedas), name = 'Canje de monedas'),
    url(r'^canjesrealizados$', login_required(views_linkcoins.canjerealizados), name = 'Canjes realizados'),
    url(r'^generador$', login_required(views_linkcoins.generador_linkcoins), name = 'Generador'),
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
    url(r'^sugerencias$', login_required(views_sugerencias.sugerencias), name = 'Sugerencias'),

    # Templates de minutas

    url(r'minutas$', login_required(views.minutas), name = 'Minutas Listas'),
    url(r'minutascrear$', login_required(views.minutascrear), name = 'Minutas Crear'),
    url(r'minutasmodificar/(?P<id_minuta>\d+)/$', login_required(views.minutasmodificar), name = 'Minutas Modificar'),
    url(r'minutasid/(?P<id_minuta>\d+)/$', login_required(views.minutasid), name = 'Minutas Id'),
    url(r'^pdfminutas/(?P<id_minuta>\d+)/$', PdfMinutas.as_view(), name = "PDF Minutas"),


    # Template de registro contable
    url(r'registro_contable_home$', login_required(views_chanchito.registro_contable_home), name = 'Registro Contable Home'),
    url(r'registro_contable_reporte$', login_required(views_chanchito.registro_contable_registro), name = 'Registro Contable Reporte'),
    url(r'registro_contable_cajas$', login_required(views_chanchito.registro_contable_cajas), name = 'Registro Contable Cajas'),
    path("registro_contable_caja/<str:caja>/<str:user_caja>/<int:estado>/<int:mes>/<int:year>/" ,login_required(views_chanchito.registro_contable_caja) ,name='Registro Contable Caja'),
    url(r'registro_contable/(?P<date_i>\d+)/$', login_required(views_chanchito.registro_contable), name = 'Registro Contable'),
    url(r'registro_contable_editar/$', login_required(views_chanchito.editar_registro_contable), name = 'Registro Contable Edicion'),
    url(r'^des_registro$', login_required(DescargarRegistroContable.as_view()), name = 'Descarga registro contable'),
]



