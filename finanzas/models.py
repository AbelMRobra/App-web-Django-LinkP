import numpy as np
from django.db import models
from proyectos.models import Proyectos
from ventas.models import VentasRealizadas
from presupuestos.models import Constantes
from rrhh.models import datosusuario

# Create your models here.

class Almacenero(models.Model):

    class Estado(models.TextChoices):
        SI = "SI"
        NO = "NO"

    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    cheques_emitidos = models.FloatField(null=True, blank=True, verbose_name="Cheques emitidos")
    gastos_fecha = models.FloatField(null=True, blank=True, verbose_name="Gastos a la fecha")
    pendiente_admin = models.FloatField(null=True, blank=True, verbose_name="Pendiente de administración")
    pendiente_comision = models.FloatField(null=True, blank=True, verbose_name="Pendiente de comisión")
    pendiente_adelantos = models.FloatField(null=True, blank=True, verbose_name="Adelantos realizados")
    pendiente_iva_ventas = models.FloatField(null=True, blank=True, verbose_name="IVA sobre ventas")
    pendiente_iibb_tem = models.FloatField(null=True, blank=True, verbose_name="IIBB + TEM")
    pendiente_iibb_tem_link = models.FloatField(null=True, blank=True, verbose_name="Cuotas a cobrar de LINK") #Esto en teoria se completa con Ctas Ctes, ahora a mano
    prestamos_proyecto = models.FloatField(null=True, blank=True, verbose_name="Prestamos a proyectos")
    prestamos_otros = models.FloatField(null=True, blank=True, verbose_name="Prestamos a otros")
    cuotas_cobradas = models.FloatField(null=True, blank=True, verbose_name="Cuotas cobradas")
    cuotas_a_cobrar = models.FloatField(null=True, blank=True, verbose_name="Cuotas a cobrar")
    ingreso_ventas = models.FloatField(null=True, blank=True, verbose_name="Ingreso por unidades a vender")
    ingreso_ventas_link = models.FloatField(null=True, blank=True, verbose_name="Ingreso por unidades a vender de LINK") #Esto solo es para el calculo de IIBB
    Prestamos_dados = models.FloatField(null=True, blank=True, verbose_name="Prestamos otorgados")
    unidades_socios = models.FloatField(null=True, blank=True, verbose_name="Unidades de Socios", editable=False)
    tenencia = models.FloatField(null=True, blank=True, verbose_name="Resultado por tenencia", default=0)
    financiacion = models.FloatField(null=True, blank=True, verbose_name="Recargo por financiacion", default=0)
    inmuebles = models.FloatField(null=True, blank=True, verbose_name="Inmuebles", default=0)
    auto_cta = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Cuenta corriente automatica", default="NO")


    class Meta:
        verbose_name="Almacenero"
        verbose_name_plural="Almaceneros"

    def __str__(self):
        return '{}'.format(self.proyecto)

class RegistroAlmacenero(models.Model):
    fecha = models.DateField(verbose_name="Fecha de guardado", blank=True, null=True,)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    cheques_emitidos = models.FloatField(null=True, blank=True, verbose_name="Cheques emitidos")
    gastos_fecha = models.FloatField(null=True, blank=True, verbose_name="Gastos a la fecha")
    pendiente_admin = models.FloatField(null=True, blank=True, verbose_name="Pendiente de administración")
    pendiente_comision = models.FloatField(null=True, blank=True, verbose_name="Pendiente de comisión")
    pendiente_adelantos = models.FloatField(null=True, blank=True, verbose_name="Adelantos realizados")
    pendiente_iva_ventas = models.FloatField(null=True, blank=True, verbose_name="IVA sobre ventas")
    pendiente_iibb_tem = models.FloatField(null=True, blank=True, verbose_name="IIBB + TEM")
    pendiente_iibb_tem_link = models.FloatField(null=True, blank=True, verbose_name="Cuotas a cobrar de LINK") #Esto en teoria se completa con Ctas Ctes, ahora a mano
    prestamos_proyecto = models.FloatField(null=True, blank=True, verbose_name="Prestamos a proyectos")
    prestamos_otros = models.FloatField(null=True, blank=True, verbose_name="Prestamos a otros")
    cuotas_cobradas = models.FloatField(null=True, blank=True, verbose_name="Cuotas cobradas")
    cuotas_a_cobrar = models.FloatField(null=True, blank=True, verbose_name="Cuotas a cobrar")
    ingreso_ventas = models.FloatField(null=True, blank=True, verbose_name="Ingreso por unidades a vender")
    ingreso_ventas_link = models.FloatField(null=True, blank=True, verbose_name="Ingreso por unidades a vender de LINK") #Esto solo es para el calculo de IIBB
    Prestamos_dados = models.FloatField(null=True, blank=True, verbose_name="Prestamos otorgados")
    unidades_socios = models.FloatField(null=True, blank=True, verbose_name="Unidades de Socios", editable=False)
    saldo_mat = models.FloatField(null=True, blank=True, verbose_name="Saldo de materiales")
    saldo_mo = models.FloatField(null=True, blank=True, verbose_name="Saldo de mano de obra")
    imprevisto = models.FloatField(null=True, blank=True, verbose_name="Saldo de imprevisto")
    credito = models.FloatField(null=True, blank=True, verbose_name="Credito")
    fdr = models.FloatField(null=True, blank=True, verbose_name="Fondos de reparo")
    retiro_socios = models.FloatField(null=True, blank=True, verbose_name="Retiro socios", default=0)
    retiro_socios_honorarios = models.FloatField(null=True, blank=True, verbose_name="Retiro socios en honorarios", default=0)
    honorarios = models.FloatField(null=True, blank=True, verbose_name="Honorarios", default=0)
    tenencia = models.FloatField(null=True, blank=True, verbose_name="Resultado por tenencia", default=0)
    financiacion = models.FloatField(null=True, blank=True, verbose_name="Recargo por financiacion", default=0)
    inmuebles = models.FloatField(null=True, blank=True, verbose_name="Inmuebles", default=0)

    class Meta:
        verbose_name="RegistroAlmacenero"
        verbose_name_plural="RegistroAlmaceneros"

    def __str__(self):
        return '{}'.format(self.proyecto)

class CuentaCorriente(models.Model):

    class Estado(models.TextChoices):
        activo= "activo"
        baja= "baja"

    venta = models.ForeignKey(VentasRealizadas, on_delete=models.CASCADE, verbose_name = "Venta Realizada")
    flujo = models.TextField(verbose_name="Flujo", blank=True, null=True)
    flujo_m3 = models.TextField(verbose_name="Flujo en M3", blank=True, null=True)
    flujo_boleto = models.TextField(verbose_name="Flujo boleto", blank=True, null=True)
    flujo_boleto_m3 = models.TextField(verbose_name="Flujo boleto M3", blank=True, null=True)
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado", default="activo")
    direccion = models.CharField(max_length=30, verbose_name = "Direccion", blank=True, null=True)
    telefono_fijo = models.CharField(max_length=15, verbose_name = "Telefono fijo", blank=True, null=True)
    telefono_celular = models.CharField(max_length=15, verbose_name = "Telefono celular", blank=True, null=True)

    def pagado_cuenta(self):

        pagado = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago")))

        return pagado

    def pagado_pesos_cuenta(self):

        pagado = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago_pesos")))

        return pagado

    def pagado_m3h_cuenta(self):

        try:
        
            pagado_pesos = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago"))*np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("cuota__constante__valor")))
            pagado_m3h = pagado_pesos/Constantes.objects.get(id = 7).valor


        except:

            pagado_m3h = 0

        return pagado_m3h

    def saldo_pesos(self):

        cuotas_pesos = sum(np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("precio"))*np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("constante__valor")))
        pagado_pesos = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago"))*np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("cuota__constante__valor")))
        saldo_pesos = cuotas_pesos - pagado_pesos

        return saldo_pesos

    def saldo_m3h(self):

        cuotas_pesos = sum(np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("precio"))*np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("constante__valor")))
        pagado_pesos = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago"))*np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("cuota__constante__valor")))
        
        try:

            saldo_m3 = (cuotas_pesos - pagado_pesos)/Constantes.objects.get(id = 7).valor

        except:

            saldo_m3 = 0

        return saldo_m3

    def estado_pesos(self):

        pagado_pesos_historico = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago_pesos")))
        cuotas_pesos = sum(np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("precio"))*np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("constante__valor")))
        pagado_pesos = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago"))*np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("cuota__constante__valor")))
        saldo_pesos = cuotas_pesos - pagado_pesos

        estado_pesos = saldo_pesos + pagado_pesos_historico

        return estado_pesos

    def estado_m3h(self):

        cuotas_pesos = sum(np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("precio"))*np.array(Cuota.objects.filter(cuenta_corriente = self).values_list("constante__valor")))
        pagado_pesos = sum(np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("pago"))*np.array(Pago.objects.filter(cuota__cuenta_corriente = self).values_list("cuota__constante__valor")))

        if pagado_pesos > cuotas_pesos:

            estado_pesos = pagado_pesos

        else:
            
            estado_pesos = cuotas_pesos

        try:
            estado_m3h = estado_pesos/Constantes.objects.get(id = 7).valor

        except:
            estado_m3h = 0

        return estado_m3h


    class Meta:
        verbose_name="Cuenta corriente"
        verbose_name_plural="Cuentas corrientes"

    def __str__(self):
        return self.venta.comprador


class Cuota(models.Model):

    class Estado(models.TextChoices):
        BOLETO= "BOLETO"
        NO_BOLETO= "NO BOLETO"

    class Pagada(models.TextChoices):
        SI= "SI"
        NO= "NO"

    cuenta_corriente = models.ForeignKey(CuentaCorriente, on_delete=models.CASCADE, verbose_name = "Cuenta corriente")
    fecha = models.DateField(verbose_name = "Fecha de venta")
    precio = models.FloatField(verbose_name="Precio de la cuota en moneda dura")
    constante = models.ForeignKey(Constantes, on_delete=models.CASCADE, verbose_name = "Constante asociada")
    precio_pesos = models.FloatField(verbose_name="Precio en pesos", blank=True, null=True)
    concepto = models.CharField(max_length=100, verbose_name = "Concepto", blank=True, null=True)
    boleto = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Boleto", default="NO BOLETO")
    pagada = models.CharField(choices=Pagada.choices, max_length=20, verbose_name="Pagada", default="NO")
    porc_boleto = models.FloatField(verbose_name="Porcentaje a aplicar boleto", blank=True, null=True, default = 0)
    
    def pago_moneda_dura(self):

        pago = sum(np.array(Pago.objects.filter(cuota = self).values_list("pago")))

        return pago

    def pago_pesos(self):

        pago = sum(np.array(Pago.objects.filter(cuota = self).values_list("pago_pesos")))

        return pago

    def pago_m3h(self):

        pago = sum(np.array(Pago.objects.filter(cuota = self).values_list("pago"))*np.array(Pago.objects.filter(cuota = self).values_list("cuota__constante__valor")))

        try:
            pago = pago/Constantes.objects.get(id = 7).valor

        except:

            pago = 0

        return pago

    def saldo_moneda_dura(self):

        saldo = self.precio - sum(np.array(Pago.objects.filter(cuota = self).values_list("pago")))

        return saldo

    def saldo_pesos(self):

        saldo = (self.precio - sum(np.array(Pago.objects.filter(cuota = self).values_list("pago"))))*self.constante.valor

        return saldo

    def saldo_m3h(self):

        try:

            valor_cuota = self.precio * self.constante.valor

            pagado = sum(np.array(Pago.objects.filter(cuota = self).values_list("pago"))*np.array(Pago.objects.filter(cuota = self).values_list("cuota__constante__valor")))

            saldo = (valor_cuota - pagado)/Constantes.objects.get(id = 7).valor

        except:

            saldo = 0

        return saldo

    def cotizacion_cuota(self):

        if sum(np.array(Pago.objects.filter(cuota = self).values_list("pago"))) == 0:

            cotizacion = 0

        else:

            cotizacion = sum(np.array(Pago.objects.filter(cuota = self).values_list("pago_pesos")))/sum(np.array(Pago.objects.filter(cuota = self).values_list("pago")))

        return cotizacion

    class Meta:
        verbose_name="Cuota"
        verbose_name_plural="Cuotas"


class Pago(models.Model):

    class Metodo(models.TextChoices):
        EFECTIVO = "EFECTIVO"
        CHEQUE = "CHEQUE"
        TRANSFERENCIA = "TRANSFERENCIA"
        DEPOSITO = "DEPOSITO"
        DOLARES = "DOLARES"

    cuota = models.ForeignKey(Cuota, on_delete=models.CASCADE, verbose_name = "Cuota")
    fecha = models.DateField(verbose_name = "Fecha del pago")
    pago = models.FloatField(verbose_name="Pago en moneda dura")
    pago_pesos = models.FloatField(verbose_name="Pago en pesos")
    documento_1 = models.CharField(max_length=100, verbose_name = "Documento 1", blank=True, null=True)
    documento_2 = models.CharField(max_length=100, verbose_name = "Documento 2", blank=True, null=True)
    metodo = models.CharField(choices=Metodo.choices, max_length=20, verbose_name="Metodo", blank=True, null=True)
    banco = models.CharField(max_length=100, verbose_name = "Banco", blank=True, null=True)

    class Meta:
        verbose_name="Pago"
        verbose_name_plural="Pagos"

    def __str__(self):
        return self.documento_1

class PagoRentaAnticipada(models.Model):
    class Metodo(models.TextChoices):
        EFECTIVO = "EFECTIVO"
        CHEQUE = "CHEQUE"
        TRANSFERENCIA = "TRANSFERENCIA"
        DEPOSITO = "DEPOSITO"
        DOLARES = "DOLARES"

    cuenta_corriente = models.ForeignKey(CuentaCorriente, on_delete=models.CASCADE, verbose_name = "Cuenta corriente")
    fecha = models.DateField(verbose_name = "Fecha del pago")
    pagado = models.BooleanField(default=False)
    monto_pagado=models.FloatField(verbose_name="Monto pagado de renta anticipada" ,default=0.0)
    monto=models.FloatField(verbose_name="Monto fijo de renta anticipada", blank=True, null=True)
    

    class Meta:
            verbose_name="Pago de renta anticipada"
            verbose_name_plural="Pagos de renta anticipada"

    def __str__(self):
        return str(self.cuenta_corriente) 

class ArchivosAdmFin(models.Model):
    fecha = models.DateField(verbose_name = "Fecha de los archivos")
    resumen_credito_inv = models.FileField(verbose_name="Resumen credito inversiones", blank=True, null=True)

    class Meta:
        verbose_name="Archivo ADM/FINAN"
        verbose_name_plural="Archivos ADM/FINAN"

class Arqueo(models.Model):
    fecha = models.DateField(verbose_name = "Fecha del arqueo")
    arqueo = models.FileField(verbose_name="Archivo Excel", blank=True, null=True)

    class Meta:
        verbose_name="Arqueo"
        verbose_name_plural="Arqueos"

class RetirodeSocios(models.Model):
    fecha = models.DateField(verbose_name = "Fecha del retiro")
    retira = models.CharField(verbose_name="Retira", blank=True, null=True, max_length=300)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto", blank=True, null=True)
    monto_pesos = models.FloatField(verbose_name="Monto en pesos", blank=True, null=True)
    comentario = models.CharField(verbose_name="Comentario", blank=True, null=True, max_length=300)

    class Meta:
        verbose_name="Retiro"
        verbose_name_plural="Retiros"

class MovimientoAdmin(models.Model):

    class Estado(models.TextChoices):
        ESPERA = "ESPERA"
        APROBADA = "APROBADA"
        RECHAZADA = "RECHAZADA"


    fecha = models.DateField(verbose_name = "Fecha del archivo")
    archivo = models.FileField(verbose_name = "Archivo")
    comentario = models.CharField(max_length=200, null=True, blank=True, verbose_name = "Comentario")
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado", default="ESPERA")

    class Meta:
        verbose_name="Movimiento de administración"
        verbose_name_plural="Movimientos de administración"

class Honorarios(models.Model):
    fecha = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    cuotas = models.FloatField(verbose_name="Cuotas a cobrar", blank=True, null=True, default=0)
    ventas = models.FloatField(verbose_name="Ventas proyectadas", blank=True, null=True, default=0)
    estructura_gio = models.FloatField(verbose_name="Gastos de estructura y G.I.O", blank=True, null=True, default=0)
    aportes = models.FloatField(verbose_name="Aportes a proyectos", blank=True, null=True, default=0)
    socios = models.FloatField(verbose_name="Socios", blank=True, null=True, default=0)
    comision_venta = models.FloatField(verbose_name="Comisión de venta", blank=True, null=True, default=0)
    deudas = models.FloatField(verbose_name="Deudas", blank=True, null=True, default=0)
    retiro_socios = models.FloatField(verbose_name="Retiro de socios", blank=True, null=True, default=0)
    creditos = models.FloatField(verbose_name="Creditos", blank=True, null=True, default=0)
    caja_actual = models.FloatField(verbose_name="Caja actual", blank=True, null=True, default=0)

    class Meta:
        verbose_name = "Honorario"
        verbose_name_plural = "Honorarios"

    def __str__(self):
        return "Honorarios"

class RegistroEmail(models.Model):

    usuario = models.ForeignKey(datosusuario, on_delete=models.CASCADE)
    fecha= models.DateField()
    destino = models.ForeignKey(CuentaCorriente, on_delete=models.CASCADE)
    estado_cuenta = models.FileField(upload_to='media')

    def __str__(self):

        return '{} {}'.format(self.fecha,self.destino)