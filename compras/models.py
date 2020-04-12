from django.db import models
from projects.models import Proyectos
from age.models import Agenda

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

class StockComprasAnticipadas(models.Model):
    obra = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de compra")

    class Meta:

        verbose_name="Stock compra anticipada"
        verbose_name_plural="Stock compras anticipadas"

    def __str__(self):
        return self.name
     

