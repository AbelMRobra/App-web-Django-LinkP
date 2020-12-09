from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from .views import descargadeventas
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
    url(r'^informeventa$', login_required(views.informeventa), name = 'Informe de venta'),
    url(r'^fechaentrega$', login_required(views.fechaentrega), name = 'Fecha de entrega'),
    url(r'^historialventa$', login_required(views.historialventa), name = 'Historial de venta'),
    url(r'^cajaarea$', login_required(views.cajaarea), name = 'Caja del area'),
    url(r'^invmer$', login_required(views.invmer), name = 'Investigacion de mercado'),
    url(r'^informeredes$', login_required(views.invmer), name = 'Informe redes'),
    url(r'^variacionhormigon$', login_required(views.variacionh), name = 'Variacion H'),
    url(r'^encuestapostventa$', login_required(views.encuestapostventa), name = 'Encuesta de postventa'),
    url(r'^folleto$', login_required(views.folleto), name = 'Folleto'),
    url(r'^evo_usd$', login_required(views.evousd), name = 'Evolucion USD/m2'),
    url(r'^informe_redes$', login_required(views.informe_redes), name = 'Informe redes'),
    url(r'^resumenprecio$', login_required(views.resumenprecio), name = 'Resumen de precio'),
    url(r'^cargarventa$', login_required(views.cargarventa), name = 'Cargar Venta'),
    url(r'^cargar_venta$', login_required(views.cargar_venta), name = 'Cargar una Venta'),
    url(r'^descargarventas/$', login_required(descargadeventas.as_view()), name = 'Descargar ventas'),

]