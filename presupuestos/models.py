from django.db import models
from proyectos.models import Proyectos

# Modelo para constantes

class Constantes(models.Model):
    nombre = models.CharField(max_length=200)
    valor = models.FloatField()
    descrip = models.TextField()
    
    class Meta:
        verbose_name="Constante"
        verbose_name_plural="Constantes"

    def __str__(self):
        return '{}'.format(self.nombre)

# Modelo para articulos

class Articulos(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    constante = models.ForeignKey(Constantes, null=True, blank=True, on_delete=models.CASCADE)
    valor = models.FloatField()
    valor_aux = models.FloatField(null=True)
    descrip = models.TextField()
    unidad = models.CharField(max_length=10, blank=True,)
    fecha_c = models.DateField(auto_now_add=True)
    fecha_a = models.DateField(auto_now=True)

    class Meta:
        verbose_name="Articulo"
        verbose_name_plural="Articulos"

    def __str__(self):
        return self.nombre

# Modelo para pasar datos

class DatosProyectos(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    fecha_a = models.DateTimeField(auto_now=True, verbose_name = "Fecha de actualización")
    img = models.ImageField(verbose_name = "Imagen", upload_to="proyects")
    presup = models.FileField(null=True, verbose_name = "Presupuesto", upload_to="proyects/presupuestos")
    exp = models.FileField(null=True, verbose_name = "Explosión de insumos", upload_to="proyects/exp")
    curva = models.FileField(null=True, verbose_name = "Curva de inversión", upload_to="proyects/curva")

    class Meta:
        verbose_name = "Dato de proyecto"
        verbose_name_plural = "Datos de proyectos"

    def __str__(self):
        return '{}'.format(self.proyecto)


# Modelo para pasar presupuestos

class Presupuestos(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyectos")
    valor = models.FloatField(verbose_name= "Valor del proyecto")
    fecha_a = models.DateField(auto_now=True, verbose_name= "Fecha de actualización")

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

    def __str__(self):
        return '{}'.format(self.proyecto)

class Prametros(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyectos")
    tasa_des_p = models.FloatField(verbose_name="Tasa de descuento del costo")
    soft = models.FloatField(verbose_name="Soft + IVA")
    imprevitso = models.FloatField(verbose_name="Imprevisto")
    terreno = models.FloatField(verbose_name="Honorarios Terreno")
    link = models.FloatField(verbose_name="Honorarios Desarrolladora")
    comer = models.FloatField(verbose_name="Honorarios Comercialización")
    por_comer = models.FloatField(verbose_name="Porcentaje aplicación comercialización")
    tem_iibb = models.FloatField(verbose_name="TEM e IIBB")
    por_temiibb = models.FloatField(verbose_name="Porcentaje de aplicación TEM e IIBB")
    ganancia = models.FloatField(verbose_name="Ganancia")
    tasa_des = models.FloatField(verbose_name="Tasa descuento")

    class Meta:
        verbose_name = "Parametro"
        verbose_name_plural = "Parametros"

    def __str__(self):
        return '{}'.format(self.proyecto)

class Desde(models.Model):
    parametros = models.ForeignKey(Prametros, on_delete=models.CASCADE, verbose_name = "Parametros")
    presupuesto = models.ForeignKey(Presupuestos, on_delete=models.CASCADE, verbose_name = "Presupuesto", null=True, blank=True)
    fecha_c = models.DateField(auto_now=True, blank=True, null=True, verbose_name="Fecha del informe")
    valor_costo = models.FloatField(blank=True, null=True, verbose_name="Valor de costo")
    valor_costo_usd = models.FloatField(blank=True, null=True, verbose_name="Valor de costo en USD")
    valor_final = models.FloatField(blank=True, null=True, verbose_name="Valor final")
    valor_final_usd = models.FloatField(blank=True, null=True, verbose_name="Valor final en USD")

    class Meta:
        verbose_name = "Indicador de precio"
        verbose_name_plural = "Indicador de precios"

    def __str__(self):
        return '{}'.format(self.parametros)
