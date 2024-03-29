from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from rrhh.views_rrhh import views_reportes_excel
from users.views import views , views_sugerencias ,views_chanchito ,views_linkcoins
from users.viewsets import viewsets_linkcoins

router = routers.DefaultRouter()
router.register(r'api_linkcoins', viewsets_linkcoins.LinkcoinsViewset)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    url(r'^$', views.welcome, name = 'Bienvenido'),
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
    url(r'^pdfminutas/(?P<id_minuta>\d+)/$', views.PdfMinutas.as_view(), name = "PDF Minutas"),


    # Template de registro contable
    url(r'^registro_contable_gastos$', login_required(views_chanchito.registro_contable_gastos), name = 'Control Gastos'),
    url(r'registro_contable_home$', login_required(views_chanchito.registro_contable_home), name = 'Registro Contable Home'),
    url(r'registro_contable_reporte$', login_required(views_chanchito.registro_contable_registro), name = 'Registro Contable Reporte'),
    url(r'registro_contable_cajas$', login_required(views_chanchito.registro_contable_cajas), name = 'Registro Contable Cajas'),
    path("registro_contable_caja/<int:caja>/<int:estado>/<int:mes>/<int:year>/" ,login_required(views_chanchito.registro_contable_caja) ,name='Registro Contable Caja'),
    url(r'registro_contable/(?P<date_i>\d+)/$', login_required(views_chanchito.registro_contable), name = 'Registro Contable'),
    url(r'registro_contable_editar/$', login_required(views_chanchito.editar_registro_contable), name = 'Registro Contable Edicion'),
    url(r'^des_registro$', login_required(views_chanchito.DescargarRegistroContable.as_view()), name = 'Descarga registro contable'),

    #linkcoins
    url(r'^movimientoslinkcoins$', login_required(views_linkcoins.perfil_movimientos_linkcoins), name = 'Guia'),
    url(r'^linkp$', login_required(views.linkp), name = 'Link P'),
    url(r'^canjemoneda$', login_required(views_linkcoins.canjear_monedas), name = 'Canje de monedas'),
    url(r'^canjesrealizados$', login_required(views_linkcoins.canjes_realizados), name = 'Canjes realizados'),
    url(r'^generador$', login_required(views_linkcoins.generador_linkcoins), name = 'Generador'),
    url(r'^reporte-linkcoins$', login_required(views_reportes_excel.ExcelReporteLinkcoins.as_view()), name = 'Reporte Linkcoins Excel'),

]



