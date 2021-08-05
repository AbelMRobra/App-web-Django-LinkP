from django.db import models
from rrhh.models import datosusuario

class Atajos(models.Model):
    nombre = models.CharField(max_length=400, verbose_name="Nombre")
    url = models.CharField(max_length=400, verbose_name="URL")
    icono = models.ImageField(verbose_name="Icono")
    usuario = models.ManyToManyField(datosusuario, verbose_name="Usuarios")

    class Meta:
        verbose_name="Atajo del home"
        verbose_name_plural="Atajos del home"

    def __str__(self):
        return self.nombre