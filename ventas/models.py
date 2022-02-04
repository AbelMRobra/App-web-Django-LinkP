from django.db import models
from proyectos.models import Proyectos, Unidades
from django.contrib.auth.models import User
from rrhh.models import datosusuario

# Create your models here.

class Clientescontacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name = "Nombre")
    apellido = models.CharField(max_length=100, verbose_name = "Apellido")
    email = models.CharField(max_length=100, verbose_name = "Email")
    telefono = models.CharField(max_length=100, verbose_name = "Telefono", blank=True, null=True)
    fecha_nacimiento = models.DateField(verbose_name = "Fecha de nacimiento", blank=True, null=True)
    imagenlogo = models.ImageField(verbose_name="Imagen", blank=True, null=True)
    activo=models.BooleanField(default=True)

    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

    def __str__(self):
        return '{}, {}'.format(self.nombre, self.apellido)

class Pricing(models.Model):

    class SioNo(models.TextChoices):
        SI = "SI"
        NO = "NO"
    unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, verbose_name = "Unidades")
    frente = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Frente")
    piso_intermedio = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Piso intermedio")
    cocina_separada = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Cocina Separada")
    local = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Local Comercial")
    menor_50_m2 = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Menor a 50 m2")
    menor_45_m2 = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Menor a 45 m2", blank=True, null=True)
    otros = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Otros", blank=True, null=True)

    class Meta:
        verbose_name="Pricing por unidad"
        verbose_name_plural="Pricing por unidades"

    def __str__(self):
        return '{}'.format(self.unidad)

class PricingResumen(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    fecha = models.DateField(verbose_name = "Fecha que corresponde")
    precio_prom_contado = models.FloatField(verbose_name="Precio promedio contado")
    precio_prom_financiado = models.FloatField(verbose_name="Precio promedio financiado")
    base_precio = models.FloatField(verbose_name="Base de precio", null=True, blank=True)
    anticipo = models.FloatField(verbose_name="Anticipo")
    cuotas_pend = models.IntegerField(verbose_name="Cuotas pendientes") 

    class Meta:
        verbose_name="Resumen de pricing"
        verbose_name_plural="Resumen de pricing"

    def __str__(self):
        return '{}'.format(self.proyecto)

class ArchivosComercial(models.Model):

    nombre = models.CharField(max_length=100, verbose_name="Nombre del archivo")
    usuarios_permitidos = models.ManyToManyField(datosusuario, verbose_name = "Usuarios permitidos", blank=True)
    fecha = models.DateField(verbose_name="Fecha que corresponde")
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto", null=True, blank=True)
    adjunto = models.FileField(verbose_name="Adjunto")

    class Meta:

        verbose_name="Archivos comercial"
        verbose_name_plural="Archivos comercial"

    def __str__(self):
        
        return '{}'.format(self.nombre)

class DosierDeVenta(models.Model):
    fecha = models.DateField(verbose_name="Fecha que corresponde")
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    adjunto = models.FileField(verbose_name="Adjunto")

    class Meta:
        verbose_name="Dosier de venta"
        verbose_name_plural="Dosieres de venta"

class VentasRealizadas(models.Model):

    class ModoVenda(models.TextChoices):
        VENTA = "VENTA"
        CANJE = "CANJE"

    class TipoUnidad(models.TextChoices):
        DTO = "DTO"
        COCHERA = "COCHERA"

    class Estado(models.TextChoices):
        ACTIVA = "ACTIVA"
        BAJA = "BAJA"


    comprador = models.CharField(max_length=100, verbose_name = "Nombre del comprador")
    cliente = models.ForeignKey(Clientescontacto, on_delete=models.CASCADE, verbose_name = "Cliente", blank=True, null=True)
    fecha = models.DateField(verbose_name = "Fecha de venta")
    tipo_venta = models.CharField(choices=ModoVenda.choices, max_length=20, verbose_name="Tipo de venta", blank=True, null=True)
    unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, verbose_name = "Unidades", blank=True, null=True)
    tipo_unidad = models.CharField(choices=TipoUnidad.choices, max_length=20, verbose_name="Tipo de unidad", blank=True, null=True)
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    asignacion = models.CharField(max_length=100, verbose_name="Asignacion")   
    m2 = models.FloatField(verbose_name="Metros cuadrados")
    precio_venta = models.FloatField(verbose_name="Precio de venta")
    precio_venta_hormigon = models.FloatField(verbose_name="Precio de venta en hormigon", blank=True, null=True, default=0)
    precio_contado = models.FloatField(verbose_name="Precio de contado", blank=True, null=True, default=0)
    precio_pricing = models.FloatField(verbose_name="Precio pricing", blank=True, null=True)
    precio_desde = models.FloatField(verbose_name="Precio desde", blank=True, null=True)
    anticipo = models.FloatField(verbose_name="Anticipo")
    cuotas_pend = models.IntegerField(verbose_name="Cuotas pendientes")
    observaciones = models.TextField(verbose_name="Observaciones", null=True, blank=True)
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado", blank=True, null=True, default="ACTIVA")
    email = models.CharField(max_length=100, verbose_name = "Email de ventas", null=True, blank=True) 
    
    class Meta:
        verbose_name="Venta"
        verbose_name_plural="Ventas"

    def __str__(self):
        return '{}'.format(self.proyecto)

class EstudioMercado(models.Model):
    fecha = models.DateField(verbose_name="Fecha del estudio")
    zona = models.CharField(max_length=100, verbose_name="Zona del estudio")
    empresa = models.CharField(max_length=100, verbose_name="Empresa")
    proyecto = models.CharField(max_length=100, verbose_name="Nombre del proyecto")
    meses = models.IntegerField(verbose_name="Meses a la entrega")
    precio = models.FloatField(verbose_name="Precio")

    class Meta:
        verbose_name="Estudio de mercado"
        verbose_name_plural="Estudios de mercado"

    def __str__(self):
        return self.empresa

class ArchivosAreaVentas(models.Model):
    fecha = models.DateField(verbose_name="Fecha que corresponde")
    radiografia_cliente = models.FileField(verbose_name="Radiografia del cliente", blank=True, null=True)
    informe_redes = models.FileField(verbose_name="Informe de redes", blank=True, null=True)
    encuesta_postventa = models.FileField(verbose_name="Encuesta de postventa", blank=True, null=True)
    caja_area = models.FileField(verbose_name="Caja area", blank=True, null=True)
    invest_mercado = models.FileField(verbose_name="Investigacion de mercado", blank=True, null=True)
    evo_usd = models.FileField(verbose_name="Evolución USD/m2", blank=True, null=True)
    informe_venta = models.FileField(verbose_name="Informe de venta", blank=True, null=True)
    historial_venta = models.FileField(verbose_name="Historial de venta", blank=True, null=True)

    class Meta:
        verbose_name = "Archivos Área Ventas"
        verbose_name_plural = "Archivos Área Ventas"

    def __str__(self):
        return "Archivos del area"

class ArchivoFechaEntrega(models.Model):
    fecha = models.DateField(verbose_name="Fecha de carga", auto_now_add=True)
    archivo = models.FileField(verbose_name="archivo", blank=True, null=True)

    class Meta:
        verbose_name = "Archivo Fecha de entrega"
        verbose_name_plural = "Archivos Fecha de entrega"

    def __str__(self):
        return "Archivos de fecha de entrega"

class ArchivoVariacionHormigon(models.Model):
    fecha = models.DateTimeField(verbose_name="Fecha de carga", auto_now_add=True)
    archivo = models.FileField(verbose_name="archivo", blank=True, null=True)

    class Meta:
        verbose_name = "Archivo Variacion Hormigon"
        verbose_name_plural = "Archivos Variacion Hormigon"

    def __str__(self):
        return "Archivos de fecha de entrega"

class ClasificacionReclamosPostventa(models.Model):

    nombre = models.CharField(max_length=300, verbose_name = "Clasificacion del problema", unique=True)

    class Meta:
        verbose_name = "Clasificacion del reclamo"
        verbose_name_plural = "Clasificaciones de los reclamos"

    def __str__(self):
        return self.nombre

class ReclamosPostventa(models.Model):

    class Estado(models.TextChoices):

        ESPERA = "ESPERA"
        TRABAJANDO = "TRABAJANDO"
        PROBLEMAS = "PROBLEMAS"
        LISTO = "LISTO"

    numero = models.IntegerField(verbose_name = "Numero de reclamo")
    propietario = models.CharField(max_length=100, verbose_name = "Propietario")
    usuario = models.CharField(max_length=100, verbose_name = "Usuario")
    telefono = models.IntegerField(verbose_name = "Telefono", blank=True, null=True)
    email = models.CharField(max_length=100, verbose_name = "Email", blank=True, null=True)
    proyecto = models.CharField(max_length=100, verbose_name = "Proyecto")
    unidad = models.CharField(max_length=100, verbose_name = "Unidad")
    fecha_reclamo = models.DateField(verbose_name="Fecha del reclamo")
    fecha_solucion = models.DateField(verbose_name="Fecha del reclamo", blank=True, null=True)
    estado = models.CharField(choices=Estado.choices, max_length=40, verbose_name="Estado", default="ESPERA")
    responsable =  models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Responsable", blank=True, null=True)
    clasificacion = models.CharField(max_length=300, verbose_name = "Clasificacion del problema")
    descripcion = models.TextField(verbose_name="Descripción del problema")
    visto = models.BooleanField(default=False, verbose_name="Visto por responsable")
    monto = models.FloatField(default=0, verbose_name="Monto del reclamo")

    class Meta:
        verbose_name = "Reclamo de Postventa"
        verbose_name_plural = "Reclamos de Postventa"

    def __str__(self):
        return self.propietario

class FormularioSolucionPostventa(models.Model):

    reclamo = models.ForeignKey(ReclamosPostventa, on_delete=models.CASCADE, verbose_name="Reclamo asociado")
    fecha = models.DateField(verbose_name="Fecha del formulario", auto_now_add=True)
    responsable = models.CharField(max_length=100, verbose_name = "Responsable")
    metodo_pago = models.CharField(max_length=100, verbose_name = "Metodo de pago")
    costo_mo = models.FloatField(verbose_name="Costo de MO")
    costo_mat = models.FloatField(verbose_name="Costo de materiales")
    descripcion = models.TextField(verbose_name="Descripción")
    observacion = models.TextField(verbose_name="Observación")

    class Meta:
        verbose_name = "Formulario de solución de postventa"
        verbose_name_plural = "Formularios de solución de postventa"

    def __str__(self):
        return f" Reclamo nº {self.reclamo.numero}"

class FormularioDetallePostventa(models.Model):

    reclamo = models.ForeignKey(ReclamosPostventa, on_delete=models.CASCADE, verbose_name="Reclamo asociado")
    fecha_inicio = models.DateField(verbose_name="Fecha inicio")
    fecha_final = models.DateField(verbose_name="Fecha final")
    descripcion = models.TextField(verbose_name="Descripción")


    class Meta:
        verbose_name = "Formulario de detalle de postventa"
        verbose_name_plural = "Formularios de detalles de postventa"

    def __str__(self):
        return f" Reclamo nº {self.reclamo.numero}"

class AdjuntosReclamosPostventa(models.Model):

    nombre = models.CharField(max_length=100, verbose_name = "Nombre del archivo", blank=True, null=True)
    reclamo = models.ForeignKey(ReclamosPostventa, on_delete=models.CASCADE, verbose_name="Reclamo asociado")
    archivo = models.FileField(verbose_name="Adjunto")

    class Meta:
        verbose_name = "Adjunto de reclamo"
        verbose_name_plural = "Adjuntos de reclamo"

    def __str__(self):
        return f'{self.reclamo.numero}, {self.reclamo.propietario}'

class FeaturesProjects(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    nombre = models.CharField(max_length=100, verbose_name = "Nombre")
    inc = models.FloatField(verbose_name="Porcentaje de variación")

    class Meta:
        verbose_name="Feature Project"
        verbose_name_plural="Features Project"

    def _str_(self):
        return '{}'.format(self.nombre)

class FeaturesUni(models.Model):
    unidad = models.ForeignKey(Unidades, on_delete=models.CASCADE, verbose_name = "Unidades")
    feature = models.ForeignKey(FeaturesProjects, on_delete=models.CASCADE, verbose_name = "Feature")

    class Meta:
        verbose_name="Feature Project"
        verbose_name_plural="Features Project"

    def _str_(self):
        return '{}'.format(self.feature.nombre)

class ImgEnlacesProyecto(models.Model):
    
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    enlace = models.CharField(max_length=200, verbose_name = "Enlaces")

    class Meta:
        verbose_name="Enlace de imagenes"
        verbose_name_plural="Enlaces de imagenes"

    def _str_(self):
        return '{}'.format(self.proyecto.nombre)


