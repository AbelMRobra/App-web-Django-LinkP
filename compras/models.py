from django.db import models
from proyectos.models import Proyectos
from presupuestos.models import Articulos
from rrhh.models import datosusuario
# Create your models here.

class Proveedores(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    descrip = models.TextField(verbose_name="Descripción")
    phone = models.IntegerField(verbose_name="Telefono")
    update = models.DateField(auto_now=True, verbose_name="Actualización")

    class Meta:

        verbose_name="Proveedor"
        verbose_name_plural="Proveedores"
        

    def __str__(self):
        return self.name

class Contratos(models.Model):
    np = models.CharField(max_length=200, verbose_name="Codigo")
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name="Proveedor")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del contrato")
    descripcion = models.CharField(max_length=400, verbose_name="Descripción corta", blank=True, null=True)
    monto = models.IntegerField(verbose_name="Monto final", blank=True, null=True)
    actualiza = models.CharField(max_length=200, verbose_name="Como actualiza", blank=True, null=True)
    

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
    
    def __str__(self):
        return self.np

class AdjuntosContratos(models.Model):
    contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE, verbose_name="Vincala a un contrato", blank=True, null=True)
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    adjunto = models.FileField(verbose_name="Archivo")
    fecha_c = models.DateField(verbose_name="Fecha")

    class Meta:
        verbose_name = "Adjunto de contratos"
        verbose_name_plural = "Adjuntos de contratos"

class Comparativas(models.Model):

    class autoriza(models.TextChoices):
            PL = "PL"
            SP = "SP"

    class publica(models.TextChoices):
            SI = "SI"
            NO = "NO"

    class estados(models.TextChoices):

            ESPERA = "ESPERA"
            AUTORIZADA = "AUTORIZADA"
            NO_AUTORIZADA = "NO AUTORIZADA"
            ADJ_AUTORIZADA = "ADJUNTO ✓"

    class visto(models.TextChoices):

            VISTO = "VISTO"
            NO_VISTO = "NO_VISTO"
            NO_CONFORME = "VISTO NO CONFORME"

    class tipo_compra(models.TextChoices):

            MATERIALES = "MATERIALES"
            SERVICIOS = "SERVICIOS"
            CONTRATOS = "CONTRATOS"

    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name="Nombre del contratista")
    contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE, verbose_name="Vincala a un contrato", blank=True, null=True)
    proyecto = models.CharField(verbose_name="Proyecto", blank=True, null=True, max_length=200)
    numero = models.CharField(verbose_name="Codigo", blank=True, null=True, max_length=200)
    o_c = models.CharField(verbose_name="Nº orden de compra", blank=True, null=True, max_length=200)
    monto = models.IntegerField(verbose_name="Monto de la compra")
    estado = models.CharField(choices=estados.choices, default=estados.ESPERA, editable=False, max_length=20, verbose_name="Estado", blank=True, null=True)
    adjunto = models.ImageField(verbose_name="Imagen adjunta")
    adj_oc = models.FileField(verbose_name="Orden de compra", blank=True, null=True)
    fecha_c = models.DateField(auto_now_add=True, verbose_name="Fecha de carga")
    fecha_autorizacion = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de aturorizacion")
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentario", editable=False)
    visto = models.CharField(choices=visto.choices, default=visto.NO_VISTO, editable=False, max_length=20, verbose_name="Revisado por SP", blank=True, null=True)
    autoriza = models.CharField(choices=autoriza.choices, max_length=20, verbose_name="Autoriza", blank=True, null=True)
    publica = models.CharField(choices=publica.choices, default=publica.SI, max_length=20, verbose_name="Es publica?", blank=True, null=True)
    creador = models.CharField(verbose_name="Crador", blank=True, null=True, max_length=200) 
    tipo_oc = models.CharField(choices=tipo_compra.choices, max_length=40, verbose_name="Tipo de OC", blank=True, null=True)

    class Meta:
        verbose_name = "Comparativa"
        verbose_name_plural = "Comparativas"

class ComparativasMensaje(models.Model):

    usuario =  models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario")
    comparativa =  models.ForeignKey(Comparativas, on_delete=models.CASCADE, verbose_name="Comparativa")
    mensaje =  models.CharField(verbose_name="Mensaje", blank=True, null=True, max_length=200)
    fecha = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True, blank=True, null=True)

    class Meta:

        verbose_name="Mensaje"
        verbose_name_plural="Mensajes"
        

    def __str__(self):
        return self.mensaje

class Compras(models.Model):

    class estados(models.TextChoices):

            ANTICIPADA = "ANT"
            NORMAL = "NORMAL"

    class imprevisto(models.TextChoices):
        IMPREVISTO = "IMPREVISTO"
        PREVISTO = "PREVISTO"

    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name="Proyectos", blank=True, null=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name="Proveedor")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la compra")
    tipo = models.CharField(choices=estados.choices, max_length=20, verbose_name="Tipo", blank=True, null=True)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, verbose_name="Articulo")
    cantidad = models.FloatField(verbose_name="Cantidad")
    precio = models.FloatField(blank=True, null=True, verbose_name="Precio")
    precio_presup = models.FloatField(blank=True, null=True, verbose_name="Precio de presupuesto")
    fecha_c = models.DateField(auto_now_add=True, verbose_name="Fecha de compra")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    documento = models.CharField(max_length=200, verbose_name="Documento de referencia", blank=True, null=True)
    partida = models.FloatField(blank=True, null=True, verbose_name="Partida")
    imprevisto = models.CharField(choices=imprevisto.choices, max_length=200, verbose_name="Imprevisto", blank=True, null=True)


    class Meta:
        verbose_name="Compra"
        verbose_name_plural="Compras"

    def __str__(self):
        return self.nombre

class Retiros(models.Model):
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE, verbose_name="Compra")
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE, verbose_name="Articulo")
    cantidad = models.FloatField(verbose_name = "Cantidad")
    fecha_c = models.DateField(auto_now_add=True, verbose_name="Fecha de retiro")
    fecha_a = models.DateField(auto_now=True, verbose_name="Fecha de actualización")
    documento = models.CharField(max_length=200, verbose_name="Documento de referencia")

    class Meta:
        verbose_name="Retiro"
        verbose_name_plural="Retiros"

    def __str__(self):
        return '{}'.format(self.compra)

class StockComprasAnticipadas(models.Model):
    obra = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Nombre")
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de compra")

    class Meta:

        verbose_name="Stock compra anticipada"
        verbose_name_plural="Stock compras anticipadas"

    def __str__(self):
        return self.name
     
class Certificados(models.Model):

    class Estado(models.TextChoices):
        ESPERA = "ESPERA"
        CHEQUEADO = "CHEQUEADO"

    proyecto = models.ForeignKey(Proyectos, null=False, blank=True, on_delete=models.CASCADE, verbose_name = "Proyecto")
    contrato = models.ForeignKey(Contratos, null=False, blank=True, on_delete=models.CASCADE, verbose_name= "Contrato")
    num_cer =  models.IntegerField(verbose_name="Numero de certificado")
    descrip = models.CharField(max_length=200, verbose_name="Descripción")
    adj = models.FileField(null=True, verbose_name = "Adjunto", upload_to="projects/cert")
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado", blank=True, null=True, default="ESPERA")

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return self.descrip





