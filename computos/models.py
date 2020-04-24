from django.db import models
from proyectos.models import Proyectos

# Create your models here.

class ListaRubros(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del rubro")

    class Meta:
        verbose_name="Rubro"
        verbose_name_plural="Rubros"

    def __str__(self):
        return self.nombre


class Tipologias(models.Model):
    rubro = models.ForeignKey(ListaRubros, on_delete= models.CASCADE, verbose_name="Rubro")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    un = models.CharField(max_length=200, verbose_name="Unidad")

    class Meta:
        verbose_name="Tipologia"
        verbose_name_plural="Tipologias"

    def __str__(self):
        return self.nombre

class Plantas(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")

    class Meta:
        verbose_name="Planta"
        verbose_name_plural="Plantas"

    def __str__(self):
        return self.nombre

class Computos(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete= models.CASCADE, verbose_name="Proyecto")
    planta = models.ForeignKey(Plantas, on_delete = models.CASCADE, verbose_name="Planta")
    rubro = models.ForeignKey(ListaRubros, on_delete = models.CASCADE, verbose_name="Rubro")
    tipologia = models.ForeignKey(Tipologias, on_delete = models.CASCADE, verbose_name="Tipologia")
    valor_lleno = models.FloatField(verbose_name="Valor lleno", blank=True, null=True)
    valor_vacio = models.FloatField(verbose_name="Valor vacio", blank=True, null=True)
    valor_total = models.FloatField(verbose_name="Valor total", blank=True, null=True)
    valor_obra = models.FloatField(verbose_name="Valor en obra", blank=True, null=True)
    fecha_a = models.DateField(blank=True, null=True, auto_now=True, verbose_name="Fecha de actualización")
    class Meta:
        verbose_name="Computo"
        verbose_name_plural="Computos"
        
        
