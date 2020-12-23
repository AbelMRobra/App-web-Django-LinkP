from django.db import models
from proyectos.models import Proyectos
from compras.models import Contratos
from rrhh.models import datosusuario

# Create your models here.

class Etapas(models.Model):
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE, verbose_name="Proyecto")
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la etapa")

    class Meta:

        verbose_name="Etapa"
        verbose_name_plural="Etapas"
        
    def __str__(self):
        return self.nombre

class ItemEtapa(models.Model):

    class estados(models.TextChoices):

        ESPERA = "ESPERA"
        TRABAJANDO = "TRABAJANDO"
        PROBLEMAS = "PROBLEMAS"
        LISTO = "LISTO"

    nombre = models.CharField(max_length=200, verbose_name="Nombre de la subetapa")
    responsable = models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Responsable", blank=True, null=True)
    etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE, verbose_name="Proyecto")
    estado = models.CharField(choices=estados.choices, default=estados.ESPERA, max_length=20, verbose_name="Estado")
    contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE, verbose_name="Contrato", blank=True, null=True)
    archivo_vigente = models.FileField(verbose_name="Archivo vigente", blank=True, null=True)
    fecha_estimada = models.DateField(verbose_name="Fecha estimada de finalziación", blank=True, null=True)
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio", blank=True, null=True)
    fecha_final = models.DateField(verbose_name="Fecha final", blank=True, null=True)

    class Meta:

        verbose_name="Sub etapa"
        verbose_name_plural="Sub etapas"
        
    def __str__(self):
        return self.nombre

class TecnicaMensaje(models.Model):
    usuario =  models.ForeignKey(datosusuario, on_delete=models.CASCADE, verbose_name="Usuario")
    item =  models.ForeignKey(ItemEtapa, on_delete=models.CASCADE, verbose_name="Item asociado")
    mensaje =  models.CharField(verbose_name="Mensaje", blank=True, null=True, max_length=200)
    fecha = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True, blank=True, null=True)

    class Meta:

        verbose_name="Mensaje"
        verbose_name_plural="Mensajes"
        
    def __str__(self):
        return self.mensaje