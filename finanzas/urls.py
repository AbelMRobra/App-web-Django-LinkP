from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA FIANANZAS -----------------------------------------
    url(r'^almacenero/$', login_required(views.almacenero), name = 'Almacenero'),
    url(r'^consolidado/$', login_required(views.consolidado), name = 'Consolidado'),
    url(r'^unidadesseñadas/$', login_required(views.ingresounidades), name = 'Unidades señadas'),
    url(r'^panelctacte/$', login_required(views.panelctacote), name = 'Panel cuentas corrientes'),
    url(r'^crearcuenta/$', login_required(views.crearcuenta), name = 'Crear cuenta corriente'),
    url(r'^ctacteproyecto/(?P<id_proyecto>\d+)/$', login_required(views.ctacteproyecto), name = 'Cuenta corriente proyecto'),
    url(r'^ctactecliente/(?P<id_cliente>\d+)/$', login_required(views.ctactecliente), name = 'Cuenta corriente venta'),


]