from django.urls import path, re_path
from django.conf.urls import url
from . import views
from .views import Reegistrodecompras, CompOCestado
from django.contrib.auth.decorators import login_required

urlpatterns = [  
    url(r'^proveedores$', login_required(views.proveedores), name = 'Proveedores'),
    url(r'^cargacompras$', login_required(views.cargacompras), name = 'Carga compras'),
    url(r'^compras$', login_required(views.compras), name = 'Compras'),
    url(r'^comparativas$', login_required(views.comparativas), name = 'Comparativas'),
    url(r'^ocautorizadas$', login_required(views.panelvisto), name = 'OC autorizadas'),
    url(r'^comparativaspl/(?P<estado>\d+)/$', login_required(views.comparativas_pl), name = 'Panel de comparativas'),
    url(r'^listaretiros$', login_required(views.listaretiros), name = 'Lista de retiros'),
    url(r'^listacomprasretiros$', login_required(views.comprasdisponibles), name = 'Compras para retirar'),
    url(r'^cargaretiro/(?P<nombre>\d+)/$', login_required(views.cargaretiro), name = 'Carga de retiros'),
    url(r'^certificados$', login_required(views.certificados), name = 'Certificados'),
    url(r'^informe$', login_required(views.informe), name = 'Informe de área'),
    url(r'^stockprov$', login_required(views.stockproveedores), name = 'Stock Proveedores'),
    url(r'^analisiscompras$', login_required(views.analisiscompras), name = 'Analisis Compras'),
    url(r'^registrodecompras/$', login_required(Reegistrodecompras.as_view()), name = 'Descargar compras'),
    url(r'^descargarestado/$', login_required(CompOCestado.as_view()), name = 'Descargar estado'),
    url(r'^informecompras/$', login_required(views.informecompras), name = 'Informe compras'),

]