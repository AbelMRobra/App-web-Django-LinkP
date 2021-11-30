import datetime
from django.db import models
from presupuestos.models import Articulos, Constantes

# Create your models here.

class Inventario(models.Model):

    num_inv = models.CharField(max_length=200, verbose_name="Numero Inventario")
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, verbose_name="Articulo", related_name='articulo_inventario')
    precio_md = models.FloatField(blank=True, null=True, verbose_name="Precio en moneda dura")
    constante = models.ForeignKey(Constantes, blank=True, null=True, on_delete=models.PROTECT)
    fecha_compra = models.DateField(verbose_name="Fecha de compra")
    amortizacion = models.IntegerField(verbose_name="Amortización (años)")

    def fecha_amortizacion(self):

        fecha_amortizacion = self.fecha_compra + datetime.timedelta(days = (365*self.amortizacion))

        return fecha_amortizacion

    def valor_amortizacion(self):

        fecha_amortizacion = self.fecha_amortizacion()

        fecha_compra = self.fecha_compra

        if datetime.date.today() >= fecha_amortizacion:
            
            valor_amortizacion = 0

        elif fecha_amortizacion == fecha_compra:

            valor_amortizacion = 0

        else:

            articulo = self.articulo

            total_dias = (fecha_amortizacion- fecha_compra).days
            total_transcurrido = (datetime.date.today() - fecha_compra).days
            valor_amortizacion = articulo.valor - round((total_transcurrido/total_dias)*articulo.valor, 2)

        return valor_amortizacion

    class Meta:
        verbose_name="Inventario"
        verbose_name_plural="Inventarios"

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


class Partediario(models.Model):

    usuario = models.ForeignKey(Operario, verbose_name="Usuario", on_delete=models.CASCADE)
    lider = models.CharField(max_length=200, verbose_name="Nombre del lider de cuadrilla")
    subtarea = models.ForeignKey(SubTarea, verbose_name="Subtarea", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha del parte")
    horas = models.FloatField(verbose_name="Horas", blank=True, null=True)
    avance = models.FloatField(verbose_name="Avance", blank=True, null=True)

    class Meta:
        verbose_name="Parte diario"
        verbose_name_plural="Partes diarios"

    def __str__(self):
        return self.fecha
