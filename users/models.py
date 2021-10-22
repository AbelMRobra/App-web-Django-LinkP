from django.db import models
from rrhh.models import datosusuario

class ActividadesUsuarios(models.Model):

    usuario = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario")
    categoria = models.CharField(max_length=30, verbose_name="Categoria")
    accion = models.CharField(max_length=50, verbose_name="Acción")
    momento = models.DateTimeField(verbose_name= "Fecha")

    class Meta:
        verbose_name="Actividad"
        verbose_name_plural="Actividades"

    def __str__(self):
        return f'{self.usuario.identificacion} - {self.categoria} - {self.accion}'


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