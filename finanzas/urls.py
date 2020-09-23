from django.urls import path, re_path
from django.conf.urls import url
from . import views
from .views import DescargarCuentacorriente
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #----------------URL PARA FIANANZAS -----------------------------------------
    url(r'^almacenero/$', login_required(views.almacenero), name = 'Almacenero'),
    url(r'^consolidado/$', login_required(views.consolidado), name = 'Consolidado'),
    url(r'^unidadesseñadas/$', login_required(views.ingresounidades), name = 'Unidades señadas'),
    url(r'^panelctacte/$', login_required(views.panelctacote), name = 'Panel cuentas corrientes'),
    url(r'^crearcuenta/$', login_required(views.crearcuenta), name = 'Crear cuenta corriente'),
    url(r'^resumen/(?P<id_cliente>\d+)/$', login_required(views.resumenctacte), name = 'Resumen cuenta corriente'),
    url(r'^ctacteproyecto/(?P<id_proyecto>\d+)/$', login_required(views.ctacteproyecto), name = 'Cuenta corriente proyecto'),
    url(r'^ctactecliente/(?P<id_cliente>\d+)/$', login_required(views.ctactecliente), name = 'Cuenta corriente venta'),
    url(r'^agregarcuota/(?P<id_cuenta>\d+)/$', login_required(views.agregar_cuota), name = 'Agregar cuota'),
    url(r'^eliminarcuota/(?P<id_cuota>\d+)/$', login_required(views.eliminar_cuota), name = 'Eliminar cuota'),
    url(r'^totalcuentas/$', login_required(views.totalcuentacte), name = 'Total cuenta'),
    url(r'^editarcuota/(?P<id_cuota>\d+)/$', login_required(views.editar_cuota), name = 'Editar cuota'),
    url(r'^pagos/(?P<id_cuota>\d+)/$', login_required(views.pagos), name = 'Pagos'),
    url(r'^agregarpagos/(?P<id_cuota>\d+)/$', login_required(views.agregar_pagos), name = 'Agregar pagos'),
    url(r'^des_ctacte/(?P<id_cuenta>\d+)/$', login_required(DescargarCuentacorriente.as_view()), name = 'Descargar cuenta'),
    url(r'^eliminarpago/(?P<id_pago>\d+)/$', login_required(views.eliminar_pago), name = 'Eliminar pago'),
    url(r'^resumencredinv/$', login_required(views.resumencredinv), name = 'Resumen de creditos e inversiones'),


]