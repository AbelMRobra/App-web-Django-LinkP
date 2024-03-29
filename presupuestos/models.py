import datetime
import numpy as np
from django.db import models
from proyectos.models import Proyectos
from computos.models import Tipologias
from rrhh.models import datosusuario
from django.core.validators import MinValueValidator
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
    cuenta_corriente = models.IntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name="Constante"
        verbose_name_plural="Constantes"

    def __str__(self):
        return '{}'.format(self.nombre)


class Articulos(models.Model):

    class Tipo(models.TextChoices):

        MATERIAL = "MATERIAL"
        SUBCONTRATO = "SUBCONTRATO"
        MO = "MO"

    id = models.IntegerField(null=True, blank=True)
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    constante = models.ForeignKey(Constantes, null=True, blank=True, on_delete=models.CASCADE)
    valor = models.FloatField(validators=[MinValueValidator(0.0)], default=0)
    valor_aux = models.FloatField(null=True)
    descrip = models.TextField()
    unidad = models.CharField(max_length=10, blank=True,)
    fecha_c = models.DateField(auto_now_add=True)
    fecha_a = models.DateField(auto_now=True)
    tipo_articulo = models.CharField(choices=Tipo.choices, max_length=20, verbose_name="Estado de las tareas", blank=True, null=True)

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

    def valor_analisis(self):
        instances = CompoAnalisis.objects.filter(analisis = self)
        valor_analisis = sum(np.array(instances.values_list('articulo__valor', flat=True)*np.array(instances.values_list('cantidad', flat=True))))
        return valor_analisis

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


class Presupuestos(models.Model):

    proyecto = models.OneToOneField(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyectos", related_name="proyecto")
    proyecto_base = models.ForeignKey(Proyectos, blank=True, null=True, on_delete=models.CASCADE, verbose_name = "Proyecto base", related_name="proyecto_base")
    valor = models.FloatField(verbose_name= "Valor del proyecto")
    saldo = models.FloatField(verbose_name= "Saldo del proyecto", blank=True, null=True)
    saldo_mat = models.FloatField(verbose_name= "Saldo del proyecto - Materiales", blank=True, null=True)
    saldo_mo = models.FloatField(verbose_name= "Saldo del proyecto - Mano de obra", blank=True, null=True)
    credito = models.FloatField(verbose_name= "Credito", blank=True, null=True)
    fdr =  models.FloatField(verbose_name= "Fdr", blank=True, null=True)
    imprevisto = models.FloatField(verbose_name= "Saldo del imprevisto", null=True, blank=True)
    anticipos = models.FloatField(verbose_name= "Anticipos", null=True, blank=True)
    saldo_cap = models.FileField(verbose_name="Archivo Saldo Capitulo", null=True, blank=True)
    balance_details = models.TextField(verbose_name="Detalle del saldo", blank=True, null=True)
    consumption_details = models.TextField(verbose_name="Detalle del consumo", blank=True, null=True)
    fecha_a = models.DateField(auto_now=True, verbose_name= "Fecha de actualización")
    presupuestador = models.CharField(verbose_name="Presupuestador", null=True, blank=True ,max_length=100)

    def reset_presupuesto(self):
        self.valor = 0
        self.saldo = 0
        self.saldo_mat = 0
        self.saldo_mo = 0
        self.credito = 0
        self.fdr =  0
        self.imprevisto = 0
        self.anticipos = 0
        self.proyecto_base = None



    def calculo_iva_compras(self):
        valor_a_pagar = (self.imprevisto + self.saldo_mat + self.saldo_mo + self.credito + self.fdr)*0.07875
        return valor_a_pagar

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

    def __str__(self):
        return '{}'.format(self.proyecto)


class Prametros(models.Model):

    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyectos", blank=True, null=True)
    proyecto_no_est = models.CharField(verbose_name="Proyecto no estructurado", null=True, blank=True ,max_length=100)
    tasa_des_p = models.FloatField(verbose_name="Tasa de descuento del costo", default=0)
    soft = models.FloatField(verbose_name="Soft", default=0)
    iva = models.FloatField(verbose_name="IVA", blank=True, null=True, default=0)
    imprevitso = models.FloatField(verbose_name="Imprevisto", default=0)
    terreno = models.FloatField(verbose_name="Honorarios Terreno", default=0)
    link = models.FloatField(verbose_name="Honorarios Desarrolladora", default=0)
    comer = models.FloatField(verbose_name="Honorarios Comercialización", default=0)
    por_comer = models.FloatField(verbose_name="Porcentaje aplicación comercialización", default=0)
    tem_iibb = models.FloatField(verbose_name="TEM e IIBB", default=0)
    por_temiibb = models.FloatField(verbose_name="Porcentaje de aplicación TEM e IIBB", default=0)
    ganancia = models.FloatField(verbose_name="Ganancia", default=0)
    tasa_des = models.FloatField(verbose_name="Tasa descuento", default=0)
    depto = models.FloatField(verbose_name="Proporción depto", blank=True, null=True, default=0)
    

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
    cantidad= models.FloatField(verbose_name="Cantidad", null=True, validators=[MinValueValidator(0.0)], default=0)
    orden = models.IntegerField(verbose_name="Orden", null=True, blank=True)
    comentario = models.CharField(verbose_name="Comentario" ,max_length=200, null=True, blank=True)

    def corregir_componente(self):
        if self.cantidad == None:
            self.cantidad = 0
            self.save()

        return "Ok"

    def valor_componente(self):
        instances = CompoAnalisis.objects.filter(analisis = self.analisis)
        valor_analisis = sum(np.array(instances.values_list('articulo__valor', flat=True)*np.array(instances.values_list('cantidad', flat=True))))
        return valor_analisis* self.cantidad

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


class InformeMensual(models.Model):

    fecha = models.DateField(verbose_name="Fecha del informe")
    user = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Capitulo")
    informe = models.TextField(verbose_name="Descripción de la causa", blank=True, null=True)
    devolucion = models.TextField(verbose_name="Devolución", blank=True, null=True)

    class Meta:
        verbose_name="Informe mensual"
        verbose_name_plural="Informes mensuales"


class TareasProgramadas(models.Model):

    class Estado(models.TextChoices):
        LISTO = "LISTO"
        TRABAJANDO = "TRABAJANDO"
        ESPERA = "ESPERA"
        PROBLEMAS = "PROBLEMAS"

    tarea = models.CharField(max_length=200, verbose_name="Tareas programadas")
    informe = models.ForeignKey(InformeMensual, on_delete=models.CASCADE, verbose_name="Informe", blank=True, null=True)
    proyecto= models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto", blank=True, null=True)
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado de las tareas", default=Estado.ESPERA)
    fecha = models.DateField(verbose_name="Fecha de cumplimiento", blank=True, null=True, auto_now=True)

    def terminar_tarea(self):
        self.fecha = datetime.date.today()
        self.estado = "LISTO"

    class Meta:
        verbose_name="Tarea"
        verbose_name_plural="Tareas"


class Bitacoras(models.Model):
    fecha = models.DateField(verbose_name="Fecha del informe", auto_now=True)
    hashtag = models.CharField(max_length=15, verbose_name="Hashtag", blank=True, null=True)
    titulo = models.CharField(max_length=200, verbose_name="Titulo", blank=True, null=True)
    proyecto= models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    informe = models.ForeignKey(InformeMensual, on_delete=models.CASCADE, verbose_name="Informe", blank=True, null=True)
    descrip = models.TextField(verbose_name="Descripción de la causa", blank=True, null=True)

    class Meta:
        verbose_name="Bitacora"
        verbose_name_plural="Bitacoras"


class PresupuestosAlmacenados(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    archivo = models.FileField(verbose_name="Archivo")

    class Meta:
        verbose_name="Almacen"
        verbose_name_plural="Almacenes"


class DocumentacionProyectoPresupuesto(models.Model):

    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    descrip = models.CharField(max_length=200, verbose_name="Descripción")
    entregado = models.BooleanField(verbose_name="Entregado")
    cuantificado = models.BooleanField(verbose_name="Cuantificado")

    class Meta:
        verbose_name="Check-list-Documentacion"
        verbose_name_plural="Check-list-Documentacion"

    def __str__(self):
        return f'{self.proyecto.nombre}-{self.descrip}'





