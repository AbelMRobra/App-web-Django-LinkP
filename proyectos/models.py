from django.db import models


# Create your models here.

class Proyectos(models.Model):

    class presupuesto(models.TextChoices):

            ACTIVO = "ACTIVO"
            EXTRAPOLADO = "EXTRAPOLADO"
            BASE = "BASE"

    presupuesto = models.CharField(choices=presupuesto.choices, default="EXTRAPOLADO", max_length=30, verbose_name="Estado presupuesto")
    base = models.FloatField(verbose_name="Valor con respecto a base", default=1, blank=True, null=True)
    nombre = models.CharField(max_length=200, verbose_name='Nombre del proyecto')
    descrip = models.CharField(max_length=200, verbose_name='Descripción')
    google_maps = models.CharField(max_length=400, verbose_name='Google Maps', blank=True, null=True)
    iamgen = models.ImageField(verbose_name="Logo del proyecto", blank=True, null=True)
    imagen = models.ImageField(verbose_name="Imagen del proyecto", blank=True, null=True)
    color = models.TextField(verbose_name="Color del proyecto", blank=True, null=True)
    fecha_f = models.DateField(verbose_name="Fecha de entrega")
    fecha_i = models.DateField(verbose_name="Fecha de inicio", blank=True, null=True)
    fecha_f_contrato = models.DateField(verbose_name="Fecha de entrega", blank=True, null=True)
    fecha_i_contrato = models.DateField(verbose_name="Fecha de inicio", blank=True, null=True)
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    m2 =  models.FloatField(verbose_name="Tamaño de la obra")
    numero_cuenta =  models.CharField(max_length=200, verbose_name="Numero de cuenta corriente", blank=True, null=True)
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
    folleto = models.FileField(verbose_name="Folleto", blank=True, null=True)
    precio_linkp = models.FloatField(null=True, blank=True, verbose_name="Precio Link-P")
    precio_pricing = models.FloatField(null=True, blank=True, verbose_name="Precio Pricing")
    precio_posta = models.FloatField(null=True, blank=True, verbose_name="Precio posta")


    # Datos almacenados de finanzas
    fechas_ctas_ctes = models.TextField(verbose_name="Fechas", blank=True, null=True)
    flujo_ingreso = models.TextField(verbose_name="Fluejo de ingreso", blank=True, null=True)
    flujo_ingreso_link = models.TextField(verbose_name="Fluejo de ingreso de Link", blank=True, null=True)
    flujo_ingreso_proyecto = models.TextField(verbose_name="Fluejo de ingreso de Proyecto", blank=True, null=True)
    flujo_ingreso_m3 = models.TextField(verbose_name="Fluejo de ingreso M3", blank=True, null=True)
    flujo_ingreso_link_m3 = models.TextField(verbose_name="Fluejo de ingreso de Link M3", blank=True, null=True)
    flujo_ingreso_proyecto_m3 = models.TextField(verbose_name="Fluejo de ingreso de Proyecto M3", blank=True, null=True)



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
            COCHERA_SD = "COCHERA S/D"
            DEPARTAMENTO = "DEPARTAMENTO"
            LOCAL = "LOCAL"
            BAULERA = "BAULERA"

    class estados(models.TextChoices):

            VENDIDA = "VENDIDA"
            DISPONIBLE = "DISPONIBLE"
            SEÑADA = "SEÑADA"

    class asignacion(models.TextChoices):

            PROYECTO = "PROYECTO"
            TERRENO = "TERRENO"
            HON_LINK = "HON. LINK"
            SOCIOS = "SOCIOS"


    class iibb(models.TextChoices):

        SI = "SI"
        NO = "NO"

    class comision(models.TextChoices):

        SI = "SI"
        NO = "NO"


    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    piso_unidad = models.CharField(max_length=50, verbose_name="Piso")
    nombre_unidad = models.CharField(max_length=50, verbose_name="Nomenclatura")
    tipo = models.CharField(choices=tipos.choices, max_length=20, verbose_name="Tipo")
    sup_propia = models.FloatField(verbose_name="Sup. Propia")
    sup_patio = models.FloatField(verbose_name="Sup. Patio", blank=True, null=True)
    sup_balcon = models.FloatField(verbose_name="Sup. Balcon", blank=True, null=True)
    sup_comun = models.FloatField(verbose_name="Sup. Comun")
    estado = models.CharField(choices=estados.choices, max_length=20, verbose_name="Estado")
    estado_iibb = models.CharField(choices=iibb.choices, max_length=20, verbose_name="Estado de IIBB", default=iibb.NO, blank=True, null=True)
    estado_comision = models.CharField(choices=comision.choices, max_length=20, verbose_name="Estado de comision", default=comision.NO, blank=True, null=True)
    asig = models.CharField(choices=asignacion.choices, max_length=20, verbose_name="Asignacion")
    sup_equiv = models.FloatField(verbose_name="Sup. Equivalente", blank=True, null=True)
    tipologia = models.CharField(max_length=50, verbose_name="Tipologia", blank=True, null=True)
    orden = models.IntegerField(verbose_name="Orden", default = 0, blank=True, null=True)
    contado = models.FloatField(verbose_name="Precio de contado", default = 0, blank=True, null=True)
    plano_venta = models.FileField(verbose_name="Plano de venta", blank=True, null=True)

    class Meta:
        verbose_name="Unidad"
        verbose_name_plural="Unidades"


    def superficie(self):

        if self.sup_equiv > 0:

            m2 = self.sup_equiv

        else:

            m2 = self.sup_propia + self.sup_balcon + self.sup_comun + self.sup_patio

        return m2

    def __str__(self):
        return '{} - {}'.format(self.piso_unidad, self.nombre_unidad)


class ProyeccionesProyectos(models.Model):
    fecha_inicial = models.DateField(blank=True,null=True)
    fecha_final = models.DateField(blank=True,null=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    ritmo_venta=models.IntegerField()
    cant_unidades = models.IntegerField()


    def __str__(self):
        return self.proyecto.nombre