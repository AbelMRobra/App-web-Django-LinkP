from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^estmerc$', views.estmercado, name = 'Estudio de mercado'),
    url(r'^panelunidades$', views.panelunidades, name = 'Panel de unidades'),
    url(r'^pricing/(?P<id_proyecto>\d+)/$', views.pricing, name = 'Pricing'),
    url(r'^editarasig/(?P<id_unidad>\d+)/$', views.editarasignacion, name = 'Editar asignacion'),
    url(r'^cotizador/(?P<id_unidad>\d+)/$', views.cotizador, name = 'Cotizador'),
    url(r'^editarventa/(?P<id_venta>\d+)/$', views.editarventa, name = 'Editar venta'),
    url(r'^detalleventa/(?P<id_venta>\d+)/$', views.detalleventa, name = 'Detalle venta'),
    url(r'^eliminarventa/(?P<id_venta>\d+)/$', views.eliminarventa, name = 'Eliminar venta'),
    url(r'^panelpricing$', views.panelpricing, name = 'Panel de pricing'),
    url(r'^radiografia$', views.radiografia, name = 'Radiografia del cliente'),
    url(r'^resumenprecio$', views.resumenprecio, name = 'Resumen de precio'),
    url(r'^cargarventa$', views.cargarventa, name = 'Cargar Venta'),
    url(r'^cargar_venta$', views.cargar_venta, name = 'Cargar una Venta'),

]