from django.db import models
from proyectos.models import Proyectos
from ventas.models import Clientescontacto
from rrhh.models import datosusuario
# Create your models here.


def get_medios():
    medios=[
    ('Instagram','INSTAGRAM'),
    ('Facebook','FACEBOOK'),
    ('Twitter','TWITTER'),
    ('Whatsapp','WHATSAPP'),
    ('Recomendacion','RECOMENDACION'),
    ('Publicidad de obra','PUBLICIDAD'),
    ('Avisos en gaceta','GACETA'),
    ('Pagina web','PAGINA'),

    ]
    return medios


class Tipologia(models.Model):
    nombre=models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Consulta(models.Model):
    
    fecha = models.DateField(verbose_name='Fecha de la consulta')
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE,blank=True,null=True)
    proyecto_no_est = models.CharField(max_length=50,blank=True,null=True)
    cliente=models.ForeignKey(Clientescontacto, on_delete=models.CASCADE)
    medio_contacto=models.CharField(verbose_name='Medio de contacto',max_length=50,blank=True,null=True)
    usuario=models.ForeignKey(datosusuario, on_delete=models.CASCADE,blank=True,null=True)
    tipologia=models.CharField(max_length=50,blank=True,null=True)
    tipologia2= models.ManyToManyField(Tipologia,blank=True,null=True)
    adjunto_propuesta = models.FileField(verbose_name="Propuesta", blank=True, null=True)

    class Meta:

        verbose_name = 'Consulta de cliente'
        verbose_name_plural = 'Consultas de clientes'

    def __str__(self):
        return str(self.cliente.nombre)

  
