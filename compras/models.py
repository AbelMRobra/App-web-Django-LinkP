from django.db import models
from proyectos.models import Proyectos
from presupuestos.models import Articulos

# Create your models here.

class Proveedores(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    descrip = models.TextField(verbose_name="Descripción")
    phone = models.IntegerField(verbose_name="Telefono")
    update = models.DateField(auto_now=True, verbose_name="Actualización")

    class Meta:

        verbose_name="Proveedor"
        verbose_name_plural="Proveedores"
        

    def __str__(self):
        return self.name


class Contratos(models.Model):
    np = models.CharField(max_length=200, verbose_name="Nota de pedido")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del contrato")
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name="Nombre del contratista")

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
    
    def __str__(self):
        return self.nombre


class Compras(models.Model):

    class estados(models.TextChoices):

            ANTICIPADA = "ANT"
            NORMAL = "NORMAL"

    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name="Proyectos", blank=True, null=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name="Proveedor")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la compra")
    tipo = models.CharField(choices=estados.choices, max_length=20, verbose_name="Tipo", blank=True, null=True)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, verbose_name="Articulo")
    cantidad = models.FloatField(verbose_name="Cantidad")
    precio = models.FloatField(blank=True, null=True, verbose_name="Precio")
    precio_presup = models.FloatField(blank=True, null=True, verbose_name="Precio de presupuesto")
    fecha_c = models.DateField(auto_now_add=True, verbose_name="Fecha de compra")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    documento = models.CharField(max_length=200, verbose_name="Documento de referencia", blank=True, null=True)

    class Meta:
        verbose_name="Compra"
        verbose_name_plural="Compras"

    def __str__(self):
        return self.nombre

class Retiros(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE, verbose_name="Compra")
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, verbose_name="Articulo")
    cantidad = models.FloatField(verbose_name = "Cantidad")
    fecha_c = models.DateField(auto_now_add=True, verbose_name="Fecha de retiro")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    documento = models.CharField(max_length=200, verbose_name="Documento de referencia")

    class Meta:
        verbose_name="Retiro"
        verbose_name_plural="Retiros"

    def __str__(self):
        return '{}'.format(self.compra)

class StockComprasAnticipadas(models.Model):
    obra = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de compra")

    class Meta:

        verbose_name="Stock compra anticipada"
        verbose_name_plural="Stock compras anticipadas"

    def __str__(self):
        return self.name
     
# Modelo para pasar certificados

class Certificados(models.Model):
    proyecto = models.ForeignKey(Proyectos, null=False, blank=True, on_delete=models.CASCADE, verbose_name = "Proyecto")
    contrato = models.ForeignKey(Contratos, null=False, blank=True, on_delete=models.CASCADE, verbose_name= "Nombre del Contrato")
    num_cer =  models.IntegerField(verbose_name="Numero de certificado")
    descrip = models.CharField(max_length=200, verbose_name="Descripción")
    adj = models.FileField(null=True, verbose_name = "Adjunto", upload_to="projects/cert")

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return self.descrip

