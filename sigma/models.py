from django.db import models
from presupuestos.models import Articulos

# Create your models here.

class Inventario(models.Model):
    num_inv = models.CharField(max_length=200, verbose_name="Numero Inventario")
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, verbose_name="Articulo")
    fecha_compra = models.DateField(auto_now_add=True)
    amortizacion = models.IntegerField(verbose_name="Amortización (años)")

    class Meta:
        verbose_name="Inventario"
        verbose_name_plural="Inventario"

    def __str__(self):
        return self.num_inv