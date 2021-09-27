from django.db import models
from presupuestos.models import Capitulos ,Articulos
from proyectos.models import Proyectos
# Create your models here.


# Partida Capitulo   SubPartida   Particion

class PartidasCapitulos(models.Model):
    nombre = models.CharField(max_length=50)
    capitulo = models.ForeignKey(Capitulos , on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyectos , on_delete=models.CASCADE)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()

    
    class Meta:
        verbose_name = 'Partida'
        verbose_name_plural = 'Partidas'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return '{} - {}'.format(self.proyecto,self.capitulo)

class SubPartidasCapitulos(models.Model):
    nombre = models.CharField(max_length=50)
    partida = models.ForeignKey(PartidasCapitulos , on_delete=models.CASCADE)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()

    class Meta:
        verbose_name = 'Subpartida'
        verbose_name_plural = 'Subpartidas'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return '{} - {}'.format(self.proyecto,self.capitulo)

#Particiones
class ComposicionesSubpartidas(models.Model):
    subpartida = models.ForeignKey(SubPartidasCapitulos , on_delete=models.CASCADE)
    articulo=models.ForeignKey(Articulos , on_delete=models.CASCADE)
    cantidad = models.IntegerField()


    class Meta:
        verbose_name = 'Composicion'
        verbose_name_plural = 'Composiciones'

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return '{} - {}'.format(self.articulo,self.subpartida)


