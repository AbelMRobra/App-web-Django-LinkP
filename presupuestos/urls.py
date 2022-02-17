from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from presupuestos.views import views, views_articulos, views_constantes,views_creditos,views_analisis, views_presupuestos
from presupuestos.viewsets import viewset_presupuesto
from django.contrib.auth.decorators import login_required
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api_presupuesto', viewset_presupuesto.PresupuestosViewset)

urlpatterns = [

    path("", include(router.urls)),

    #----------------URL PARA CONSTANTES -----------------------------------------
    url(r'^conslist/$', login_required(views_constantes.constantes_panel_maestro), name = 'Cons_list'),
    url(r'^conspanel/$', login_required(views_constantes.constantes_panel), name = 'Cons_panel'),
    url(r'^conscreate/$', login_required(views_constantes.constantes_crear), name = 'Cons_create'),
    url(r'^conseditar/(?P<id_cons>\d+)/$', login_required(views_constantes.constantes_editar), name = 'Editar_cons'),
    url(r'^conseliminar/(?P<id_cons>\d+)/$', login_required(views_constantes.constantes_eliminar), name = 'Eliminar_cons'),
    url(r'^registro/$', login_required(views_constantes.registro_constante), name = 'Registro'),
    #----------------URL PARA ARTICULOS -----------------------------------------    
    url(r'^insum_list/$', login_required(views_articulos.articulos_listado_maestro), name = 'Lista de insumos'),   
    url(r'^insum_panel/$', login_required(views_articulos.articulos_listado_general), name = 'Panel de cambios'),
    url(r'^insumcreate/$', login_required(views_articulos.articulos_crear), name = 'Crear insumo'),
    url(r'^insum_editar/(?P<id_articulos>\d+)/$', login_required(views_articulos.articulos_editar), name = 'Editar_insumo'),
    url(r'^insum_eliminar/(?P<id_articulos>\d+)/$', login_required(views_articulos.articulos_eliminar), name = 'Eliminar_insumo'),
    #----------------URL PARA ANALISIS -----------------------------------------  
    url(r'^analisislista/$', login_required(views_analisis.analisis_lista), name = 'Lista de analisis'),
    url(r'^panelanalisis/$', login_required(views_analisis.analisis_panel), name = 'Panel de analisis'),
    url(r'^crearanalisis/$', login_required(views_analisis.analisis_crear), name = 'Crear analisis'),
    url(r'^crearanalisis/(?P<id_analisis>\d+)/$', login_required(views_analisis.analisis_modificar), name = 'Modificar analisis'),
    url(r'^veranalisis/(?P<id_analisis>\d+)/$', login_required(views_analisis.analisis_individual_ver), name = 'Composición Analisis'),
    
    #----------------URL PARA PRESPUESTOS -----------------------------------------  
    
    path('presupuesto_principal',login_required(views_presupuestos.presupuesto_principal),name="Panel de presupuestos"),
    
    path('presupuesto_panel_control/<int:id>/',login_required(views_presupuestos.presupuestos_panel_control),name="presupuesto_proyecto"),
    url(r'^presupuestos/auditor/$', login_required(views.presupuesto_auditor), name = 'Auditor de P'),

    url(r'^saldocap/(?P<id_proyecto>\d+)/$', login_required(views.saldocapitulo), name = 'Saldo por capitulo'),
    url(r'^debugsa/(?P<id_proyecto>\d+)/$', login_required(views.debugsa), name = 'Debug Saldo'),
    url(r'^explosion/(?P<id_proyecto>\d+)/$', login_required(views.explosion), name = 'Explosión de insumos'),
    url(r'^creditos/(?P<id_proyecto>\d+)/$', login_required(views_creditos.creditos), name = 'Creditos de proyectos'),
    url(r'^fdr/(?P<id_proyecto>\d+)/$', login_required(views.fdr), name = 'Fondos de reparo'),
    url(r'^anticipos/(?P<id_proyecto>\d+)/$', login_required(views.anticiposf), name = 'Anticipos'),
    url(r'^des_explosion/(?P<id_proyecto>\d+)/$', login_required(views.ReporteExplosion.as_view()), name = 'Descarga Exp'),
    url(r'^des_explosion_cap/(?P<id_proyecto>\d+)/$', login_required(views.ReporteExplosionCap.as_view()), name = 'Descarga Exp Cap'),
    url(r'^ex_presupuesto_reposicion/(?P<id_proyecto>\d+)/$', login_required(views.PresupuestoReposicion.as_view()), name = 'Descarga presupuesto reposición'),
    url(r'^presupuestos_cap/(?P<id_proyecto>\d+)/$', login_required(views.presupuestoscapitulo), name = 'Panel de presupuestos por capitulo'),
    url(r'^presuprepabierto/(?P<id_proyecto>\d+)/$', login_required(views.presupuestorepcompleto), name = 'Presupuesto de reposición abierto'),
    url(r'^presupuestos_cap/(?P<id_proyecto>\d+)/(?P<id_capitulo>\d+)/$', login_required(views.presupuestosanalisis), name = 'Panel de presupuestos por analisis'),
    url(r'^art_saldo_cap/(?P<id_proyecto>\d+)/(?P<id_capitulo>\d+)/$', login_required(views.SaldoCapArticulos), name = 'Articulos saldo de presupuesto'),
    
    #----------------OTROS URL -----------------------------------------    
    url(r'^datos/$', login_required(views.proyectos), name = 'Datos de proyectos'),
    url(r'^desde/$', login_required(views.desde), name = 'Indicador de precios'),
    url(r'^informe/$', login_required(views.InformeArea), name = 'Informe de presupuesto'),
    url(r'^parametros/$', login_required(views.parametros), name = 'Parametros'),

    #----------------URL SERVICIOS -----------------------------------------
    url(r'^api/articulos/search$', views.ArticulosListApiView.as_view(), name = 'Articulo Buscar'),
    
    
    
    

]