from django.urls import path, re_path
from django.conf.urls import url
from . import views
from .views import ReporteExplosion, ReporteExplosionCap
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA CONSTANTES -----------------------------------------
    url(r'^cons_list/$', login_required(views.cons_list), name = 'Cons_list'),
    url(r'^cons_panel/$', login_required(views.cons_panel), name = 'Cons_panel'),
    url(r'^cons_create/$', login_required(views.cons_create), name = 'Cons_create'),
    url(r'^cons_editar/(?P<id_cons>\d+)/$', login_required(views.cons_edit), name = 'Editar_cons'),
    url(r'^cons_eliminar/(?P<id_cons>\d+)/$', login_required(views.cons_delete), name = 'Eliminar_cons'),
    url(r'^registro/$', login_required(views.registroconstante), name = 'Registro'),
    #----------------URL PARA ARTICULOS -----------------------------------------    
    url(r'^insum_list/$', login_required(views.insum_list), name = 'Lista de insumos'),   
    url(r'^insum_panel/$', login_required(views.insum_panel), name = 'Panel de cambios'),
    url(r'^insumcreate/$', login_required(views.insum_create), name = 'Crear insumo'),
    url(r'^insum_editar/(?P<id_articulos>\d+)/$', login_required(views.insum_edit), name = 'Editar_insumo'),
    url(r'^insum_eliminar/(?P<id_articulos>\d+)/$', login_required(views.insum_delete), name = 'Eliminar_insumo'),
    #----------------URL PARA ANALISIS -----------------------------------------  
    url(r'^analisis_list/$', login_required(views.analisis_list), name = 'Lista de analisis'),
    url(r'^panelanalisis/$', login_required(views.panelanalisis), name = 'Panel de analisis'),
    url(r'^crearanalisis/$', login_required(views.crearanalisis), name = 'Crear analisis'),
    url(r'^crearanalisis/(?P<id_analisis>\d+)/$', login_required(views.modificaranalisis), name = 'Modificar analisis'),
    url(r'^ver_analisis/(?P<id_analisis>\d+)/$', login_required(views.ver_analisis), name = 'Composición Analisis'),
    #----------------URL PARA PRESPUESTOS -----------------------------------------  
    url(r'^presupuestos/$', login_required(views.presupuestostotal), name = 'Panel de presupuestos'),
    url(r'^saldocap/(?P<id_proyecto>\d+)/$', login_required(views.saldocapitulo), name = 'Saldo por capitulo'),
    url(r'^debugsa/(?P<id_proyecto>\d+)/$', login_required(views.debugsa), name = 'Debug Saldo'),
    url(r'^explosion/(?P<id_proyecto>\d+)/$', login_required(views.explosion), name = 'Explosión de insumos'),
    url(r'^creditos/(?P<id_proyecto>\d+)/$', login_required(views.creditos), name = 'Creditos de proyectos'),
    url(r'^fdr/(?P<id_proyecto>\d+)/$', login_required(views.fdr), name = 'Fondos de reparo'),
    url(r'^anticipos/(?P<id_proyecto>\d+)/$', login_required(views.anticiposf), name = 'Anticipos'),
    url(r'^des_explosion/(?P<id_proyecto>\d+)/$', login_required(ReporteExplosion.as_view()), name = 'Descarga Exp'),
    url(r'^des_explosion_cap/(?P<id_proyecto>\d+)/$', login_required(ReporteExplosionCap.as_view()), name = 'Descarga Exp Cap'),
    url(r'^presupuestos_cap/(?P<id_proyecto>\d+)/$', login_required(views.presupuestoscapitulo), name = 'Panel de presupuestos por capitulo'),
    url(r'^presuprepabierto/(?P<id_proyecto>\d+)/$', login_required(views.presupuestorepcompleto), name = 'Presupuesto de reposición abierto'),
    url(r'^presupuestos_cap/(?P<id_proyecto>\d+)/(?P<id_capitulo>\d+)/$', login_required(views.presupuestosanalisis), name = 'Panel de presupuestos por analisis'),
    url(r'^art_saldo_cap/(?P<id_proyecto>\d+)/(?P<id_capitulo>\d+)/$', login_required(views.SaldoCapArticulos), name = 'Articulos saldo de presupuesto'),
    
    #----------------OTROS URL -----------------------------------------    
    url(r'^datos/$', login_required(views.proyectos), name = 'Datos de proyectos'),
    url(r'^desde/$', login_required(views.desde), name = 'Indicador de precios'),
    url(r'^informe/$', login_required(views.InformeArea), name = 'Informe de área'),
    url(r'^parametros/$', login_required(views.parametros), name = 'Parametros'),
    
    
    
    

]