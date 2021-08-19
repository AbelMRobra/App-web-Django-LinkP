from django.urls import path, re_path
from django.conf.urls import url
from . import views
from . import views_ctacte_informes
from .views import DescargarCuentacorriente, DescargarTotalCuentas, PdfPrueba, DescargarResumen, DescargarControlUnidades
from django.contrib.auth.decorators import login_required




urlpatterns = [
    #----------------URL PARA FIANANZAS -----------------------------------------

    url(r'^almacenero/$', login_required(views.almacenero), name = 'Almacenero'),
    url(r'^principalfinanzas/$', login_required(views.principalfinanzas), name = 'Principal Finanzas'),
    url(r'^precioreferencia/$', login_required(views.precioreferencia), name = 'Precio referencia'),
    url(r'^prueba/$', login_required(views.prueba), name = 'Prueba'),

    path("pagosrentaanticipada/<int:id>/<int:id_proy>" ,login_required(views.pagosRentaAnticipada) ,name='pagosrentaanticipada'),
    path("totalizadorrentaanticipadatotal",login_required(views.totalizador_renta_anticipada_total),name='totalizadorrentaanticipadatotal'),
    path("totalizadortentaanticipada/<int:id>" ,login_required(views.totalizadorRentaAnticipada) ,name='Totalizador Renta Anticipada'),

    #----------------URL CUENTAS CORRIENTES -----------------------------------------
    url(r'^appfinanzas/$', login_required(views.appfinanzas), name = 'App Finanzas'),
    url(r'^panelctacte/$', login_required(views.panelctacote), name = 'Panel cuentas corrientes'),
    url(r'^crearcuenta/(?P<id_proyecto>\d+)/$', login_required(views.crearcuenta), name = 'Crear cuenta corriente'),
    url(r'^mandarmail/(?P<id_cuenta>\d+)/$', login_required(views.mandarmail), name = 'Mandar email'),
    url(r'^deudores/(?P<id_proyecto>\d+)$', login_required(views.deudores), name = 'Deudores'),
    url(r'^resumen/(?P<id_cliente>\d+)/$', login_required(views.resumenctacte), name = 'Resumen cuenta corriente'),
    url(r'^ctacteproyecto/(?P<id_proyecto>\d+)/$', login_required(views.ctacteproyecto), name = 'Cuenta corriente proyecto'),
    url(r'^ctactecliente/(?P<id_cliente>\d+)/$', login_required(views.ctactecliente), name = 'Cuenta corriente venta'),
    url(r'^ctacteclienteboleto/(?P<id_cliente>\d+)/$', login_required(views.estructura_boleto), name = 'Cuenta corriente venta boleto'),
    url(r'^boleto/(?P<id_cuenta>\d+)/(?P<id_cuota>\d+)/$', login_required(views.boleto), name = 'Boleto en cuota'),
    url(r'^totalcuentas/(?P<id_proyecto>\d+)/$', login_required(views_ctacte_informes.totalcuentacte), name = 'Total cuenta'),
    url(r'^resumencuentas/$', login_required(views_ctacte_informes.cuentacte_resumen), name = 'Resumen de cuentas'),
    url(r'^editarcuota/(?P<id_cuota>\d+)/$', login_required(views.editar_cuota), name = 'Editar cuota'),
    url(r'^agregarcuota/(?P<id_cuenta>\d+)/$', login_required(views.agregar_cuota), name = 'Agregar cuota'),
    url(r'^eliminarcuota/(?P<id_cuota>\d+)/$', login_required(views.eliminar_cuota), name = 'Eliminar cuota'),
    url(r'^pagos/(?P<id_cuota>\d+)/$', login_required(views.pagos), name = 'Pagos'),
    url(r'^agregarpagos/(?P<id_cuota>\d+)/$', login_required(views.agregar_pagos), name = 'Agregar pagos'),
    url(r'^eliminarpago/(?P<id_pago>\d+)/$', login_required(views.eliminar_pago), name = 'Eliminar pago'),
    url(r'^editarpago/(?P<id_pago>\d+)/$', login_required(views.editar_pagos), name = 'Editar pagos'),
    url(r'^des_ctacte/(?P<id_cuenta>\d+)/$', login_required(DescargarCuentacorriente.as_view()), name = 'Descargar cuenta'),
    url(r'^des_resumenproyec/(?P<id_proyecto>\d+)/$', login_required(DescargarResumen.as_view()), name = 'Descargar resumen proyecto'),
    url(r'^des_resumenctacte/$', login_required(DescargarTotalCuentas.as_view()), name = 'Descargar resumen total de cuenta'),
    url(r'^des_ingresounidades/$', login_required(DescargarControlUnidades.as_view()), name = 'Descargar ingreso unidades'),
    url(r'^reportepdf/(?P<id_cuenta>\d+)/$', PdfPrueba.as_view(), name = "Reporte de pdf de cuentas corrientes"),
    url(r'^calculadora/$', login_required(views.calculadora), name = 'Calculadora'),

    url(r'^superavalorcta/(?P<id_cuota>\d+)/$', login_required(views.superarvalorcta), name = 'Cta cliente valor superado'),

    #----------------URL ADMINISTRACION -----------------------------------------

    url(r'^movimientoadmin/$', login_required(views.movimientoadmin), name = 'Movimiento administración'),
    url(r'^subirmovimiento/$', login_required(views.subirmovimiento), name = 'Subir movimiento'),
    url(r'^borrarmovimiento/(?P<id_mov>\d+)$', login_required(views.borrarmovimiento), name = 'Borrar movimiento'),
    url(r'^retirodesocios/$', login_required(views.retirodesocios), name = 'Retiro de socios'),
    url(r'^arqueo/(?P<id_arqueo>\d+)$', login_required(views.arqueo_diario), name = 'Arqueo diario'),
    url(r'^arqueos/$', login_required(views.arqueos), name = 'Arqueos diario'),
    url(r'^historicoalmacenero/$', login_required(views.registro_almacenero), name = 'Historico almacenero'),
    url(r'^consolidado/$', login_required(views.consolidado), name = 'Consolidado'),
    url(r'^indicelink/(?P<id_moneda>\d+)/(?P<id_time>\d+)$', login_required(views.indicelink), name = 'Indice Link'),
    url(r'^estudioindicelink/(?P<fecha1>\d+)/(?P<fecha2>\d+)/$', login_required(views.estudioindice), name = 'Estudio indice Link'),
    url(r'^indicelinkmoneda/(?P<id_moneda>\d+)$', login_required(views.indicelinkmoneda), name = 'Indice Link moneda'),
    url(r'^honorarios/$', login_required(views.honorarios), name = 'Honorarios'),
    url(r'^modhonorarios/$', login_required(views.modhonorarios), name = 'Modificar Honorarios'),
    url(r'^pagostotal/(?P<id_proyecto>\d+)$', login_required(views.consultapagos), name = 'Panel de pagos total'),  
    url(r'^unidadesseñadas/(?P<estado>\d+)/(?P<proyecto>\d+)$', login_required(views.ingresounidades), name = 'Unidades señadas'),   
    url(r'^eliminarcuentacorriente/(?P<id_cuenta>\d+)/$', login_required(views.EliminarCuentaCorriente), name = 'Eliminar cuenta corriente'),
    url(r'^resumencredinv/$', login_required(views.resumencredinv), name = 'Resumen de creditos e inversiones'),


]