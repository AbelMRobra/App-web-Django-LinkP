from django.db import models

# Create your models here.

class Proyectos(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    descrip = models.CharField(max_length=200, verbose_name='Descripción')
    iamgen = models.ImageField(verbose_name="Logo del proyecto", blank=True, null=True)
    color = models.TextField(verbose_name="Color del proyecto", blank=True, null=True)
    fecha_f = models.DateField(verbose_name="Fecha de entrega")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    m2 =  models.FloatField(verbose_name="Tamaño de la obra")
    desde = models.FloatField(null=True, blank=True, verbose_name="Precio desde")
    tasa_f = models.FloatField(null=True, blank=True, verbose_name="Tasa de finan.")
    descuento_cochera = models.FloatField(null=True, blank=True, verbose_name="Descuento cochera")
    recargo_frente = models.FloatField(null=True, blank=True, verbose_name="Recargo por frente")
    recargo_piso_intermedio = models.FloatField(null=True, blank=True, verbose_name="Recargo por piso intermedio")
    recargo_cocina_separada = models.FloatField(null=True, blank=True, verbose_name="Recargo cocina separada")
    recargo_local = models.FloatField(null=True, blank=True, verbose_name="Recargo local")
    recargo_menor_45 = models.FloatField(null=True, blank=True, verbose_name="Recargo unid. menor 45m2")
    recargo_menor_50 = models.FloatField(null=True, blank=True, verbose_name="Recargo unid. menor 50m2")
    recargo_otros = models.FloatField(null=True, blank=True, verbose_name="Otros recargos")

    class Meta:
        verbose_name="Proyecto"
        verbose_name_plural="Proyectos"

    def __str__(self):
        return self.nombre

class ProyectosTerceros(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    descrip = models.CharField(max_length=200, verbose_name='Descripción')
    fecha_f = models.DateField(verbose_name="Fecha de entrega")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    m2 =  models.FloatField(verbose_name="Tamaño de la obra")
    class Meta:
        verbose_name="Proyecto de tercero"
        verbose_name_plural="Proyectos de terceros"

    def __str__(self):
        return self.nombre


class Unidades(models.Model):

    class tipos(models.TextChoices):

            COCHERA = "COCHERA"
            DEPARTAMENTO = "DEPARTAMENTO"

    class estados(models.TextChoices):

            VENDIDA = "VENDIDA"
            DISPONIBLE = "DISPONIBLE"
            SEÑADA = "SEÑADA"

    class asignacion(models.TextChoices):

            PROYECTO = "PROYECTO"
            TERRENO = "TERRENO"
            HON_LINK = "HON. LINK"
            SOCIOS = "SOCIOS"


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
    sup_equiv = models.FloatField(verbose_name="Sup. Equivalente", blank=True, null=True)
    tipologia = models.CharField(max_length=50, verbose_name="Tipologia", blank=True, null=True)

    class Meta:
        verbose_name="Unidad"
        verbose_name_plural="Unidades"

    def __str__(self):
        return '{}'.format(self.proyecto)
