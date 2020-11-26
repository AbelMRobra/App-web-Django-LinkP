from django.db import models
from proyectos.models import Proyectos, Unidades

# Create your models here.

class Pricing(models.Model):

    class SioNo(models.TextChoices):
        SI = "SI"
        NO = "NO"
    unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, verbose_name = "Unidades")
    frente = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Frente")
    piso_intermedio = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Piso intermedio")
    cocina_separada = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Cocina Separada")
    local = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Local Comercial")
    menor_50_m2 = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Menor a 50 m2")
    menor_45_m2 = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Menor a 45 m2", blank=True, null=True)
    otros = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Otros", blank=True, null=True)

    class Meta:
        verbose_name="Pricing por unidad"
        verbose_name_plural="Pricing por unidades"

    def __str__(self):
        return '{}'.format(self.unidad)



class PricingResumen(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    fecha = models.DateField(verbose_name = "Fecha que corresponde")
    precio_prom_contado = models.FloatField(verbose_name="Precio promedio contado")
    precio_prom_financiado = models.FloatField(verbose_name="Precio promedio financiado")
    base_precio = models.FloatField(verbose_name="Base de precio", null=True, blank=True)
    anticipo = models.FloatField(verbose_name="Anticipo")
    cuotas_pend = models.IntegerField(verbose_name="Cuotas pendientes") 

    class Meta:
        verbose_name="Resumen de pricing"
        verbose_name_plural="Resumen de pricing"

    def __str__(self):
        return '{}'.format(self.proyecto)

class VentasRealizadas(models.Model):

    class ModoVenda(models.TextChoices):
        VENTA = "VENTA"
        CANJE = "CANJE"

    class TipoUnidad(models.TextChoices):
        DTO = "DTO"
        COCHERA = "COCHERA"

    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA"
        BAJA = "BAJA"


    comprador = models.CharField(max_length=100, verbose_name = "Nombre del comprador")
    fecha = models.DateField(verbose_name = "Fecha de venta")
    tipo_venta = models.CharField(choices=ModoVenda.choices, max_length=20, verbose_name="Tipo de venta", blank=True, null=True)
    unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, verbose_name = "Unidades", blank=True, null=True)
    tipo_unidad = models.CharField(choices=TipoUnidad.choices, max_length=20, verbose_name="Tipo de unidad", blank=True, null=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    asignacion = models.CharField(max_length=100, verbose_name="Asignacion")   
    m2 = models.FloatField(verbose_name="Metros cuadrados")
    precio_venta = models.FloatField(verbose_name="Precio de venta")
    precio_pricing = models.FloatField(verbose_name="Precio pricing", blank=True, null=True)
    precio_desde = models.FloatField(verbose_name="Precio desde", blank=True, null=True)
    anticipo = models.FloatField(verbose_name="Anticipo")
    cuotas_pend = models.IntegerField(verbose_name="Cuotas pendientes")
    observaciones = models.TextField(verbose_name="Observaciones", null=True, blank=True)
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado", blank=True, null=True, default="ACTIVA")

    
    class Meta:
        verbose_name="Venta"
        verbose_name_plural="Ventas"

    def __str__(self):
        return '{}'.format(self.proyecto)

class EstudioMercado(models.Model):
    fecha = models.DateField(verbose_name="Fecha del estudio")
    zona = models.CharField(max_length=100, verbose_name="Zona del estudio")
    empresa = models.CharField(max_length=100, verbose_name="Empresa")
    proyecto = models.CharField(max_length=100, verbose_name="Nombre del proyecto")
    meses = models.IntegerField(verbose_name="Meses a la entrega")
    precio = models.FloatField(verbose_name="Precio")

    class Meta:
        verbose_name="Estudio de mercado"
        verbose_name_plural="Estudios de mercado"

    def __str__(self):
        return self.empresa

class ArchivosAreaVentas(models.Model):
    fecha = models.DateField(verbose_name="Fecha que corresponde")
    radiografia_cliente = models.FileField(verbose_name="Radiografia del cliente", blank=True, null=True)
    informe_redes = models.FileField(verbose_name="Informe de redes", blank=True, null=True)
    encuesta_postventa = models.FileField(verbose_name="Encuesta de postventa", blank=True, null=True)
    caja_area = models.FileField(verbose_name="Caja area", blank=True, null=True)
    invest_mercado = models.FileField(verbose_name="Investigacion de mercado", blank=True, null=True)
    evo_usd = models.FileField(verbose_name="Evolución USD/m2", blank=True, null=True)
    informe_venta = models.FileField(verbose_name="Informe de venta", blank=True, null=True)
    historial_venta = models.FileField(verbose_name="Historial de venta", blank=True, null=True)

    class Meta:
        verbose_name = "Archivos Área Ventas"
        verbose_name_plural = "Archivos Área Ventas"

    def __str__(self):
        return "Archivos del area"


class ArchivoFechaEntrega(models.Model):
    fecha = models.DateField(verbose_name="Fecha de carga", auto_now_add=True)
    archivo = models.FileField(verbose_name="archivo", blank=True, null=True)

    class Meta:
        verbose_name = "Archivos Fecha de entrega"
        verbose_name_plural = "Archivos Fecha de entrega"

    def __str__(self):
        return "Archivos de fecha de entrega"


