from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from . import views_flujo
from .views_app import views_pricing, views_atributos, views_postventa, views_cotizador
from .views import descargadeventas, DescargaPricing
from .views_app.views_cotizador import PDF_cotizacion
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^appcomercial/$', login_required(views.appcomercial), name = 'App comercial'),
    url(r'^apparchivoscomercial/$', login_required(views.apparchivoscomercial), name = 'App archivos comercial'),
    url(r'^dosier/$', login_required(views.dosier), name = 'Dosier'),
    
    url(r'^estmerc$', login_required(views.estmercado), name = 'Estudio de mercado'),
    url(r'^panelunidades$', login_required(views.panelunidades), name = 'Panel de unidades'),
    url(r'^editarasig/(?P<id_unidad>\d+)/$', login_required(views.editarasignacion), name = 'Editar asignacion'),
    url(r'^cotizador/(?P<id_unidad>\d+)/$', login_required(views_cotizador.cotizador), name = 'Cotizador'),
    path('emailpdfcoti/<int:id_unidad>/<int:id_cliente>/<str:info_coti>', PDF_cotizacion.as_view(), name = "Email del coti"),
    url(r'^editarventa/(?P<id_venta>\d+)/$', login_required(views.editarventa), name = 'Editar venta'),
    url(r'^detalleventa/(?P<id_venta>\d+)/$', login_required(views.detalleventa), name = 'Detalle venta'),
    url(r'^eliminarventa/(?P<id_venta>\d+)/$', login_required(views.eliminarventa), name = 'Eliminar venta'),
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
    url(r'^featuresproject/(?P<id_proj>\d+)/$', login_required(views_atributos.atributos_proyecto_panel), name = 'Features Project'),
    path('cargarplano/<int:id>' ,login_required(views.cargarplano),name="cargarplano"),
    ##########################
    # URL de pricing
     url(r'^pricing/(?P<id_proyecto>\d+)/$', login_required(views_pricing.pricing_visor), name = 'Pricing'),
     url(r'^panelpricing$', login_required(views_pricing.pricing_panel), name = 'Panel de pricing'),
    ###########################
    # URL de descarga
    ###########################    
    url(r'^descargarventas/$', login_required(descargadeventas.as_view()), name = 'Descargar ventas'),
    url(r'^descargapricing/(?P<id_proyecto>\d+)/$', login_required(DescargaPricing.as_view()), name = 'Descargar del pricing'),
    
   
    url(r'^postventaprincipal$', login_required(views_postventa.postventa_panel_principal), name = 'Reclamos Postventa'),
    url(r'^reclamo/(?P<id_reclamo>\d+)/$', login_required(views_postventa.postventa_reclamo_detalle), name = 'Reclamo'),
    url(r'^reportereclamo/$', login_required(views_postventa.postventa_reporte), name = 'Reporte Reclamo'),
    url(r'^editarreclamo/(?P<id_reclamo>\d+)/$', login_required(views_postventa.editarreclamo), name = 'Editar reclamo'),
    url(r'^crearreclamo$', login_required(views_postventa.crearreclamo), name = 'Crear reclamo'),


    path('flujoventas/',login_required(views_flujo.flujoventas),name='Flujo de ventas'),
    

]