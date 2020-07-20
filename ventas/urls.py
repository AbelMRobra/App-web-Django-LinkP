from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^estmerc$', login_required(views.estmercado), name = 'Estudio de mercado'),
    url(r'^panelunidades$', login_required(views.panelunidades), name = 'Panel de unidades'),
    url(r'^pricing/(?P<id_proyecto>\d+)/$', login_required(views.pricing), name = 'Pricing'),
    url(r'^editarasig/(?P<id_unidad>\d+)/$', login_required(views.editarasignacion), name = 'Editar asignacion'),
    url(r'^cotizador/(?P<id_unidad>\d+)/$', login_required(views.cotizador), name = 'Cotizador'),
    url(r'^editarventa/(?P<id_venta>\d+)/$', login_required(views.editarventa), name = 'Editar venta'),
    url(r'^detalleventa/(?P<id_venta>\d+)/$', login_required(views.detalleventa), name = 'Detalle venta'),
    url(r'^eliminarventa/(?P<id_venta>\d+)/$', login_required(views.eliminarventa), name = 'Eliminar venta'),
    url(r'^panelpricing$', login_required(views.panelpricing), name = 'Panel de pricing'),
    url(r'^radiografia$', login_required(views.radiografia), name = 'Radiografia del cliente'),
    url(r'^resumenprecio$', login_required(views.resumenprecio), name = 'Resumen de precio'),
    url(r'^cargarventa$', login_required(views.cargarventa), name = 'Cargar Venta'),
    url(r'^cargar_venta$', login_required(views.cargar_venta), name = 'Cargar una Venta'),

]