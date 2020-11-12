from django.db import models
from proyectos.models import Proyectos
from computos.models import Tipologias

# Modelo para constantes


class Capitulos(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Capitulo")
    descrip = models.TextField(verbose_name="Descripción")

    class Meta:
        verbose_name="Capitulo"
        verbose_name_plural="Capitulos"

    def __str__(self):
        return self.nombre

class Constantes(models.Model):
    nombre = models.CharField(max_length=200)
    valor = models.FloatField()
    descrip = models.TextField()
    fecha_a = models.DateField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name="Constante"
        verbose_name_plural="Constantes"

    def __str__(self):
        return '{}'.format(self.nombre)

# Modelo para articulos

class Articulos(models.Model):
    id = models.IntegerField(null=True, blank=True)
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

class Analisis(models.Model):
    id = models.IntegerField(auto_created=True)
    codigo = models.IntegerField(primary_key=True, verbose_name="Codigo")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    unidad = models.CharField(max_length=10, verbose_name="Unidad")

    class Meta:
        verbose_name="Analisis"
        verbose_name_plural="Analisis"

    def __str__(self):
        return self.nombre

class CompoAnalisis(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, verbose_name = "Articulo")
    analisis = models.ForeignKey(Analisis, on_delete=models.CASCADE, verbose_name = "Analisis")
    cantidad = models.FloatField(verbose_name="Cantidad")

    class Meta:
        verbose_name="Composición"
        verbose_name_plural="Composición"

    def __str__(self):
        return '{}'.format(self.analisis)

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
    saldo = models.FloatField(verbose_name= "Saldo del proyecto", blank=True, null=True)
    saldo_mat = models.FloatField(verbose_name= "Saldo del proyecto - Materiales", blank=True, null=True)
    saldo_mo = models.FloatField(verbose_name= "Saldo del proyecto - Mano de obra", blank=True, null=True)
    credito = models.FloatField(verbose_name= "Credito", blank=True, null=True)
    fdr =  models.FloatField(verbose_name= "Fdr", blank=True, null=True)
    imprevisto = models.FloatField(verbose_name= "Saldo del imprevisto", null=True, blank=True)
    anticipos = models.FloatField(verbose_name= "Anticipos", null=True, blank=True)
    saldo_cap = models.FileField(verbose_name="Archivo Saldo Capitulo", null=True, blank=True)
    fecha_a = models.DateField(auto_now=True, verbose_name= "Fecha de actualización")
    presupuestador = models.CharField(verbose_name="Presupuestador", null=True, blank=True ,max_length=100)


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
    pricing = models.FloatField(blank=True, null=True, verbose_name="Pricing")

    class Meta:
        verbose_name = "Indicador de precio"
        verbose_name_plural = "Indicador de precios"

    def __str__(self):
        return '{}'.format(self.parametros)

class Modelopresupuesto(models.Model):
    proyecto= models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name="Proyecto")
    capitulo= models.ForeignKey(Capitulos, on_delete=models.CASCADE, verbose_name="Capitulo")
    analisis= models.ForeignKey(Analisis, on_delete=models.CASCADE, verbose_name="Analisis")
    vinculacion= models.ForeignKey(Tipologias, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Vinculación")
    cantidad= models.FloatField(verbose_name="Cantidad", null=True, blank=True)

    class Meta:
        verbose_name="Modelo presupuesto"
        verbose_name_plural="Modelo presupuestos"

    def __str__(self):
        return '{}'.format(self.capitulo)


class Registrodeconstantes(models.Model):
    constante = models.ForeignKey(Constantes, on_delete=models.CASCADE, verbose_name = "Constante")
    valor = models.FloatField(verbose_name="Valor", blank=True, null=True)
    fecha = models.DateField(verbose_name="Fecha", blank=True, null=True)

    class Meta:
        verbose_name="Registro de contantes ultimo"
        verbose_name_plural="Registros de constantes ultimo"

class PorcentajeCapitulo(models.Model):
    proyecto= models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    capitulo = models.ForeignKey(Capitulos, on_delete=models.CASCADE, verbose_name="Capitulo")
    porcentaje = models.FloatField(verbose_name="Porcentaje")

    class Meta:
        verbose_name="Incidencia del capitulo"
        verbose_name_plural="incidencia del capitulo"



