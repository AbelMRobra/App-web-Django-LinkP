from django.db import models
from proyectos.models import Proyectos
from ventas.models import VentasRealizadas
from presupuestos.models import Constantes

# Create your models here.

class Almacenero(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    cheques_emitidos = models.FloatField(null=True, blank=True, verbose_name="Cheques emitidos")
    gastos_fecha = models.FloatField(null=True, blank=True, verbose_name="Gastos a la fecha")
    pendiente_admin = models.FloatField(null=True, blank=True, verbose_name="Pendiente de administración")
    pendiente_comision = models.FloatField(null=True, blank=True, verbose_name="Pendiente de comisión")
    pendiente_adelantos = models.FloatField(null=True, blank=True, verbose_name="Adelantos realizados")
    pendiente_iva_ventas = models.FloatField(null=True, blank=True, verbose_name="IVA sobre ventas")
    pendiente_iibb_tem = models.FloatField(null=True, blank=True, verbose_name="IIBB + TEM")
    prestamos_proyecto = models.FloatField(null=True, blank=True, verbose_name="Prestamos a proyectos")
    prestamos_otros = models.FloatField(null=True, blank=True, verbose_name="Prestamos a otros")
    cuotas_cobradas = models.FloatField(null=True, blank=True, verbose_name="Cuotas cobradas")
    cuotas_a_cobrar = models.FloatField(null=True, blank=True, verbose_name="Cuotas a cobrar")
    ingreso_ventas = models.FloatField(null=True, blank=True, verbose_name="Ingreso por unidades a vender")
    Prestamos_dados = models.FloatField(null=True, blank=True, verbose_name="Prestamos otorgados")
    unidades_socios = models.FloatField(null=True, blank=True, verbose_name="Unidades de Socios", editable=False)


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
    prestamos_proyecto = models.FloatField(null=True, blank=True, verbose_name="Prestamos a proyectos")
    prestamos_otros = models.FloatField(null=True, blank=True, verbose_name="Prestamos a otros")
    cuotas_cobradas = models.FloatField(null=True, blank=True, verbose_name="Cuotas cobradas")
    cuotas_a_cobrar = models.FloatField(null=True, blank=True, verbose_name="Cuotas a cobrar")
    ingreso_ventas = models.FloatField(null=True, blank=True, verbose_name="Ingreso por unidades a vender")
    Prestamos_dados = models.FloatField(null=True, blank=True, verbose_name="Prestamos otorgados")
    unidades_socios = models.FloatField(null=True, blank=True, verbose_name="Unidades de Socios", editable=False)
    saldo_mat = models.FloatField(null=True, blank=True, verbose_name="Saldo de materiales")
    saldo_mo = models.FloatField(null=True, blank=True, verbose_name="Saldo de mano de obra")
    imprevisto = models.FloatField(null=True, blank=True, verbose_name="Saldo de imprevisto")
    credito = models.FloatField(null=True, blank=True, verbose_name="Credito")
    fdr = models.FloatField(null=True, blank=True, verbose_name="Fondos de reparo")


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
    cuenta_corriente = models.ForeignKey(CuentaCorriente, on_delete=models.CASCADE, verbose_name = "Cuenta corriente")
    fecha = models.DateField(verbose_name = "Fecha de venta")
    precio = models.FloatField(verbose_name="Precio de la cuota en moneda dura")
    constante = models.ForeignKey(Constantes, on_delete=models.CASCADE, verbose_name = "Constante asociada")
    precio_pesos = models.FloatField(verbose_name="Precio en pesos", blank=True, null=True)
    concepto = models.CharField(max_length=100, verbose_name = "Concepto", blank=True, null=True)
    
    class Meta:
        verbose_name="Cuota"
        verbose_name_plural="Cuotas"


class Pago(models.Model):
    cuota = models.ForeignKey(Cuota, on_delete=models.CASCADE, verbose_name = "Cuota")
    fecha = models.DateField(verbose_name = "Fecha de venta")
    pago = models.FloatField(verbose_name="Pago en moneda dura")
    pago_pesos = models.FloatField(verbose_name="Pago en pesos")
    documento_1 = models.CharField(max_length=100, verbose_name = "Documento 1", blank=True, null=True)
    documento_2 = models.CharField(max_length=100, verbose_name = "Documento 2", blank=True, null=True)

    class Meta:
        verbose_name="Pago"
        verbose_name_plural="Pagos"

    def __str__(self):
        return self.fecha

