from django.db import models
from proyectos.models import Proyectos

# Create your models here.

class NotaDePedido(models.Model):

    class SioNo(models.TextChoices):
        SI = "SI"
        NO = "NO"

    class Tipo(models.TextChoices):
        NP = "NP"
        OS = "OS"

    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name = "Proyecto")
    numero = models.IntegerField(verbose_name="Nota de pedido numero")
    titulo = models.CharField(max_length=200, verbose_name="Titulo de la nota de pedido")
    creador = models.CharField(max_length=200, verbose_name="Creador")
    destinatario = models.CharField(max_length=200, verbose_name="Destinatario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualiacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    fecha_requerida = models.CharField(max_length=200, verbose_name="Fecha requerida")
    copia = models.CharField(max_length=200, verbose_name="Quien recibe en copia")
    adjuntos = models.FileField(verbose_name="Adjuntos", blank=True, null=True)
    envio_documentacion = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Es para enviar documentación")
    cambio_proyecto = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Genera cambios al proyecto")
    comunicacion_general = models.CharField(choices=SioNo.choices, max_length=20, verbose_name="Es comunicación general")
    descripcion = models.TextField(verbose_name="Descripción de la causa")
    tipo = models.CharField(choices=Tipo.choices, max_length=20, verbose_name="Tipo de correspondencia", blank=True, null=True)
    numero = models.IntegerField(verbose_name="Nota de pedido numero", blank=True, null=True)
    visto = models.CharField(max_length=200, verbose_name="Visto", blank=True, null=True)

    class Meta:
        verbose_name="Correspondencia"
        verbose_name_plural="Correspondencias"

    def __str__(self):
        return self.titulo

class datosusuario(models.Model):
    identificacion = models.CharField(max_length=200, verbose_name="Identificacion")
    imagen = models.CharField(max_length=200, verbose_name="Imagen", blank=True, null=True, editable=False)
    imagenlogo = models.ImageField(verbose_name="Imagen", blank=True, null=True)
    area = models.CharField(max_length=200, verbose_name="Area", blank=True, null=True)
    cargo = models.CharField(max_length=200, verbose_name="Cargo", blank=True, null=True)

    class Meta:
        verbose_name="Dato de usuario"
        verbose_name_plural="Datos de los usuarios"

    def __str__(self):
        return self.identificacion


class mensajesgenerales(models.Model):

    usuario = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha", blank=True, null=True)
    mensaje = models.CharField(verbose_name="Mensaje", blank=True, null=True, max_length=200)


    class Meta:
        verbose_name="Mensaje general"
        verbose_name_plural="Mensajes generales"

    def __str__(self):
        return self.mensaje