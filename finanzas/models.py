from django.db import models
from proyectos.models import Proyectos
from ventas.models import VentasRealizadas

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

class CuentaCorriente(models.Model):
    venta = models.ForeignKey(VentasRealizadas, on_delete=models.CASCADE, verbose_name = "Venta Realizada")

    class Meta:
        verbose_name="Cuenta corriente"
        verbose_name_plural="Cuentas corrientes"

    def __str__(self):
        return self.venta.comprador
