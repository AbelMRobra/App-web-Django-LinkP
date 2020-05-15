from django.db import models

# Create your models here.

class Proyectos(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    descrip = models.CharField(max_length=200, verbose_name='Descripción')
    fecha_f = models.DateField(verbose_name="Fecha de entrega")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    m2 =  models.FloatField(verbose_name="Tamaño de la obra")

    class Meta:
        verbose_name="Proyecto"
        verbose_name_plural="Proyectos"

    def __str__(self):
        return self.nombre

class Unidades(models.Model):

    class tipos(models.TextChoices):

            COCHERA = "COCHERA"
            DEPARTAMENTO = "DEPARTAMENTO"

    class estados(models.TextChoices):

            VENDIDA = "VENDIDA"
            DISPONIBLE = "DISPONIBLE"

    class asignacion(models.TextChoices):

            PROYECTO = "PROYECTO"
            HON_TERRENO = "HON. TERRENO"
            HON_LINK = "HON. LINK"


    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    piso_unidad = models.CharField(max_length=50, verbose_name="Piso")
    nombre_unidad = models.CharField(max_length=50, verbose_name="Nomenclatura")
    tipo = models.CharField(choices=tipos.choices, max_length=20, verbose_name="Tipo")
    sup_propia = models.FloatField(verbose_name="Sup. Propia")
    sup_patio = models.FloatField(verbose_name="Sup. Patio", blank=True, null=True)
    sup_balcon = models.FloatField(verbose_name="Sup. Balcon", blank=True, null=True)
    sup_comun = models.FloatField(verbose_name="Sup. Comun")
    estado = models.CharField(choices=estados.choices, max_length=20, verbose_name="Estado")
    asig = models.CharField(choices=asignacion.choices, max_length=20, verbose_name="Asignacion")

    class Meta:
        verbose_name="Unidad"
        verbose_name_plural="Unidades"

    def __str__(self):
        return '{}'.format(self.proyecto)
