from django.db import models

# Create your models here.

class Proyectos(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    descrip = models.CharField(max_length=200, verbose_name='Descripción')
    fecha_f = models.DateField(verbose_name="Fecha de entrega")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    m2 =  models.IntegerField(verbose_name="Tamaño de la obra")

    class Meta:
        verbose_name="Proyecto"
        verbose_name_plural="Proyectos"

    def __str__(self):
        return self.nombre