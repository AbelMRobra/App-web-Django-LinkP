from django.db import models
from presupuestos.models import Constantes

# Create your models here.

class RegistroConstantes(models.Model):
    constante = models.CharField(max_length=200)
    valor = models.FloatField(verbose_name="Valor")
    fecha = models.DateField(verbose_name="Fecha")

    class Meta:
        verbose_name="Registro de contantes"
        verbose_name_plural="Registros de constantes"

