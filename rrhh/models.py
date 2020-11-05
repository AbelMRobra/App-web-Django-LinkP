from django.db import models

# Create your models here.

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