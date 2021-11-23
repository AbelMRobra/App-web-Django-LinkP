from django.urls import path, re_path
from django.conf.urls import url
from django.conf.urls import include
from rest_framework import routers
from compras.viewsets import viewsets_proveedores
from . import views
from .views import Reegistrodecompras, CompOCestado
from .views_compras import views_api, views_generales, views_proveedores, views_circuito_compras
from django.contrib.auth.decorators import login_required


router = routers.DefaultRouter()
router.register(r'api_proveedores', viewsets_proveedores.ProveedoresViewset)


urlpatterns = [ 

    path("", include(router.urls)),

    # templates de compras

    url(r'^principalcompras$', login_required(views_generales.principalcompras), name = 'Principal compras'),
    url(r'^proveedores$', login_required(views_proveedores.proveedores), name = 'Proveedores'),

    # URL -> Circuito de compras
    url(r'^comparativa_agregar$', login_required(views_circuito_compras.comparativas_agregar), name = 'Cargar O.C para autorizar'), 
    url(r'^comparativas/(?P<id_comp>\d+)$', login_required(views.editarcomparativas), name = 'Editar comparativas'),
    path('comparativas_oc_sp/<str:estado>/<str:creador>', login_required(views.ocautorizargerente1), name = "Comparativas G1"),
    path('comparativas_op_sp/<str:estado>/<str:creador>', login_required(views.panelvisto), name = 'OC autorizadas'),
  
    url(r'^cargacompras$', login_required(views.cargacompras), name = 'Carga compras'),
    url(r'^compras/(?P<id_proyecto>\d+)/$', login_required(views.compras), name = 'Compras'),
    #url(r'^modificarpreciocompra/(?P<id_proyecto>\d+)/$', login_required(views.modificar_precio_articulo_compra), name = 'modificar_precio_compra'),
    
    url(r'^comparativas/(?P<estado>\d+)/(?P<creador>\d+)/(?P<autoriza>\d+)$', login_required(views.comparativas), name = 'Comparativas'),
    
    url(r'^mensajecomparativas/(?P<id_comparativa>\d+)/$', login_required(views.mensajescomparativas), name = 'Mensajes en comparativas'),
    

    ## -----------------> Templates para el panel de autorización de OC/OP - Exclusivo del socio gerente 1
    url(r'^ocautorizadas/$', login_required(views.principalautorizacion), name = 'Principal OC-OP'),
    
    
    ## -----------------> Templates para otra cosa
    url(r'^listaretiros$', login_required(views.listaretiros), name = 'Lista de retiros'),
    url(r'^listacomprasretiros$', login_required(views.comprasdisponibles), name = 'Compras para retirar'),
    url(r'^cargaretiro/(?P<nombre>\d+)/$', login_required(views.cargaretiro), name = 'Carga de retiros'),
    url(r'^certificados$', login_required(views.certificados), name = 'Certificados'),
    url(r'^informe$', login_required(views.informe), name = 'Informe de área'),
    url(r'^stockprov$', login_required(views.stockproveedores), name = 'Stock Proveedores'),
    url(r'^descargacom$', login_required(views.descargacomparativas), name = 'Descarga Comparativas'),
    url(r'^analisiscompras$', login_required(views.analisiscompras), name = 'Analisis Compras'),
    url(r'^registrodecompras/$', login_required(Reegistrodecompras.as_view()), name = 'Descargar compras'),
    url(r'^descargarestado/(?P<fechai>\d+)/(?P<fechaf>\d+)/$', login_required(CompOCestado.as_view()), name = 'Descargar estado'),
    url(r'^informecompras/$', login_required(views.informecompras), name = 'Informe compras'),
    url(r'^detalleinforme/(?P<fecha_i>\d+)/(?P<fecha_f>\d+)/(?P<proyecto>\d+)/$', login_required(views.detalleinforme), name = 'Detalle de informe'),
    url(r'^contratos/$', login_required(views.contratos), name = 'Contratos'),
    url(r'^contratosdescripcion/(?P<id_contrato>\d+)/$', login_required(views.contratosdescripcion), name = 'Contratos descripcion'),

    ## URL Apis

    url(r'^apicompras/$', views_api.manualJson, name = 'Json Manual'),

]