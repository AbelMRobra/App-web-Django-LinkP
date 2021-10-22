from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA FIANANZAS -----------------------------------------
    url(r'^notasdepedido/(?P<id_proyecto>\d+)/(?P<tipo>\d+)/$', login_required(views.notasdepedido), name = 'Notas de pedido'),
    url(r'^notadepedido/(?P<id_nota>\d+)/$', login_required(views.notadepedido), name = 'Nota de pedido'),
    url(r'^crearcorres/$', login_required(views.crearcorrespondencia), name = 'Crear correspondencia'),
    
    url(r'^apprrhh/$', login_required(views.apprrhh), name = 'App de rrhh'),
    url(r'^editarcorres/(?P<id_nota>\d+)/$', login_required(views.editarcorrespondencia), name = 'Editar correspondencia'),
    
    #----------------URL PARA USERS -----------------------------------------
    url(r'^datospersonal/$', login_required(views.personal_principal), name = 'Datos personal'),
    url(r'^perfilpersonal/(?P<id_persona>\d+)/$', login_required(views.personal_perfil), name = 'Perfil personal'),
    url(r'^nuevousuario$', views.crear_usuarios, name = 'Crear usuario'),  
    url(r'^resetearcontraseña$', views.resetear_contraseña, name = 'Resetear contrasena'),   
    url(r'^permisos$', views.informacion_permisos, name = 'Permisos'),   


    #----------------URL ARCHIVOS -----------------------------------------
    url(r'^archivosrrh/$', login_required(views.archivosrrhh), name = 'Archivos RRHH'),

]