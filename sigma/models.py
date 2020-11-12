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


class Tarea(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la tarea")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción de la tarea")
    vinculacion = models.ForeignKey(Articulos, verbose_name="Articulo", blank=True, null=True, on_delete=models.CASCADE)
    unidad = models.CharField(max_length=200, verbose_name="Unidad")
    rend = models.FloatField(verbose_name="Rendimiento esperado (hs/unidad)", blank=True, null=True)

    class Meta:
        verbose_name="Tarea"
        verbose_name_plural="Tareas"

    def __str__(self):
        return self.nombre


class SubTarea(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la subtarea")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción de la tarea")
    vinculacion = models.ForeignKey(Tarea, verbose_name="Tarea madre", on_delete=models.CASCADE)
    unidad = models.CharField(max_length=200, verbose_name="Unidad")
    rend = models.FloatField(verbose_name="Rendimiento esperado (hs/unidad)", blank=True, null=True)

    class Meta:
        verbose_name="Sub tarea"
        verbose_name_plural="Sub tareas"

    def __str__(self):
        return self.nombre


class Operario(models.Model):

    class Estado(models.TextChoices):
        ACTIVO = "ACTIVO"
        NO_ACTIVO = "NO ACTIVO"


    dni = models.IntegerField(verbose_name="DNI del operario")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del operario")
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado", default="ACTIVO")

    class Meta:
        verbose_name="Operario"
        verbose_name_plural="Operarios"

    def __str__(self):
        return self.nombre
