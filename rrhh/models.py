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