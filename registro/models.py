from django.db import models
from presupuestos.models import Constantes
from proyectos.models import Proyectos

# Create your models here.

class RegistroConstantes(models.Model):
    constante = models.CharField(max_length=200)
    valor = models.FloatField(verbose_name="Valor")
    fecha = models.DateField(verbose_name="Fecha")

    class Meta:
        verbose_name="Registro de contantes"
        verbose_name_plural="Registros de constantes"

class RegistroValorProyecto(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    fecha = models.DateField(verbose_name = "Fecha que corresponde")
    precio_proyecto = models.FloatField(verbose_name="Precio del proyecto")

    class Meta:
        verbose_name="Registro de precios de proyecto"
        verbose_name_plural="Registro de precios de proyectos"

    def __str__(self):
        return '{}'.format(self.proyecto)

