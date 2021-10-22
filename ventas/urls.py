from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from . import views_flujo
from .views_app import views_pricing, views_atributos, views_postventa, views_cotizador, views_ventas, views_archivos
from .views import DescargaPricing
from .views_app.views_cotizador import PDF_cotizacion
from django.contrib.auth.decorators import login_required

urlpatterns = [

    # ----------> URL principal
    url(r'^comercial_principal/$', login_required(views.comercial_principal), name = 'App comercial'),

    # ----------> URL archivos
    url(r'^archivos_principal/$', login_required(views_archivos.archivos_principal), name = 'Archivos comercial'),

    # ----------> URL pricing
    url(r'^pricing_visor/(?P<id_proyecto>\d+)/$', login_required(views_pricing.pricing_visor), name = 'Pricing'),


    # ----------> URL para APP Ventas
    url(r'^ventas_principal$', login_required(views_ventas.ventas_principal), name = 'Cargar Venta'),
    url(r'^ventas_agregar$', login_required(views_ventas.ventas_agregar), name = 'Venta agregar'),
    url(r'^ventas_editar/(?P<id_venta>\d+)/$', login_required(views_ventas.ventas_editar), name = 'Editar venta'),
    url(r'^ventas_eliminar/(?P<id_venta>\d+)/$', login_required(views_ventas.ventas_eliminar), name = 'Eliminar venta'),
    url(r'^ventas_detalles/(?P<id_venta>\d+)/$', login_required(views_ventas.ventas_detalles), name = 'Detalle venta'),
    url(r'^ventas_descarga_registros/$', login_required(views_ventas.ExcelRegistroVentas.as_view()), name = 'Descargar ventas'),
    path('ventas_cargar_plano/<int:id>' ,login_required(views_ventas.ventas_cargarplano),name="cargarplano"),

    url(r'^apparchivoscomercial/$', login_required(views.apparchivoscomercial), name = 'App archivos comercial'),


    
    # ----------> URL para APP Pricing
    
    url(r'^panelunidades$', login_required(views.panelunidades), name = 'Panel de unidades'),
    url(r'^editarasig/(?P<id_unidad>\d+)/$', login_required(views.editarasignacion), name = 'Editar asignacion'),
    url(r'^cotizador/(?P<id_unidad>\d+)/$', login_required(views_cotizador.cotizador), name = 'Cotizador'),
    path('emailpdfcoti/<int:id_unidad>/<int:id_cliente>/<str:info_coti>', PDF_cotizacion.as_view(), name = "Email del coti"),
    
    url(r'^variacionhormigon$', login_required(views.variacionh), name = 'Variacion H'),
    url(r'^encuestapostventa$', login_required(views.encuestapostventa), name = 'Encuesta de postventa'),
    url(r'^resumenprecio$', login_required(views.resumenprecio), name = 'Resumen de precio'),
    

    url(r'^featuresproject/(?P<id_proj>\d+)/$', login_required(views_atributos.atributos_proyecto_panel), name = 'Features Project'),
    
    ##########################
    
    ###########################
    # URL de descarga
    ###########################    
    
    url(r'^descargapricing/(?P<id_proyecto>\d+)/$', login_required(DescargaPricing.as_view()), name = 'Descargar del pricing'),
    
   
    url(r'^postventaprincipal$', login_required(views_postventa.postventa_panel_principal), name = 'Reclamos Postventa'),
    url(r'^reclamo/(?P<id_reclamo>\d+)/$', login_required(views_postventa.postventa_reclamo_detalle), name = 'Reclamo'),
    url(r'^reportereclamo/$', login_required(views_postventa.postventa_reporte), name = 'Reporte Reclamo'),
    url(r'^editarreclamo/(?P<id_reclamo>\d+)/$', login_required(views_postventa.editarreclamo), name = 'Editar reclamo'),
    url(r'^crearreclamo$', login_required(views_postventa.crearreclamo), name = 'Crear reclamo'),


    path('flujoventas/',login_required(views_flujo.flujoventas),name='Flujo de ventas'),
    

]