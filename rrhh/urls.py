from django.urls import path, re_path
from django.conf.urls import url
from . import views
from .views_rrhh import views_perfil_usuario
from django.contrib.auth.decorators import login_required

urlpatterns = [

    #----------------URL PARA PERFIL DE USUARIO -----------------------------------------
    url(r'^perfil_usuario_principal/$', login_required(views_perfil_usuario.perfil_usuario_principal), name = 'Datos personal'),
    url(r'^perfil_usuario_perfil/(?P<id_persona>\d+)/$', login_required(views_perfil_usuario.perfil_usuario_perfil), name = 'Perfil personal'),
    url(r'^perfil_usuario_resetear_password$', views_perfil_usuario.perfil_usuario_resetear_password, name = 'Resetear contrasena'),   
    url(r'^perfil_usuario_resetear_permisos$', views_perfil_usuario.informacion_permisos, name = 'Permisos'), 
    url(r'^user_crear$', views_perfil_usuario.users_crear, name = 'Crear usuario'),  

    #----------------URL PARA FIANANZAS -----------------------------------------
    url(r'^notasdepedido/(?P<id_proyecto>\d+)/(?P<tipo>\d+)/$', login_required(views.notasdepedido), name = 'Notas de pedido'),
    url(r'^notadepedido/(?P<id_nota>\d+)/$', login_required(views.notadepedido), name = 'Nota de pedido'),
    url(r'^crearcorres/$', login_required(views.crearcorrespondencia), name = 'Crear correspondencia'),
    
    url(r'^apprrhh/$', login_required(views.apprrhh), name = 'App de rrhh'),
    url(r'^editarcorres/(?P<id_nota>\d+)/$', login_required(views.editarcorrespondencia), name = 'Editar correspondencia'),
    
    

    #----------------URL ARCHIVOS -----------------------------------------
    url(r'^archivosrrh/$', login_required(views.archivosrrhh), name = 'Archivos RRHH'),

]