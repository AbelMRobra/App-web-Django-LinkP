from django.db import models
from proyectos.models import Proyectos
from ventas.models import VentasRealizadas
from presupuestos.models import Constantes

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
    venta = models.ForeignKey(VentasRealizadas, on_delete=models.CASCADE, verbose_name = "Venta Realizada")

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
    
    class Meta:
        verbose_name="Cuota"
        verbose_name_plural="Cuotas"

class Pago(models.Model):

    class Metodo(models.TextChoices):
        EFECTIVO = "EFECTIVO"
        CHEQUE = "CHEQUE"
        TRANSFERENCIA = "TRANSFERENCIA"
        DEPOSITO = "DEPOSITO"

    cuota = models.ForeignKey(Cuota, on_delete=models.CASCADE, verbose_name = "Cuota")
    fecha = models.DateField(verbose_name = "Fecha de venta")
    pago = models.FloatField(verbose_name="Pago en moneda dura")
    pago_pesos = models.FloatField(verbose_name="Pago en pesos")
    documento_1 = models.CharField(max_length=100, verbose_name = "Documento 1", blank=True, null=True)
    documento_2 = models.CharField(max_length=100, verbose_name = "Documento 2", blank=True, null=True)
    metodo = models.CharField(choices=Metodo.choices, max_length=20, verbose_name="Metodo", blank=True, null=True)

    class Meta:
        verbose_name="Pago"
        verbose_name_plural="Pagos"

    def __str__(self):
        return self.documento_1

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