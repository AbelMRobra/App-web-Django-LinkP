from django.db import models

# Create your models here.

class Constantes(models.Model):
    nombre = models.CharField(max_length=200)
    valor = models.FloatField()
    descrip = models.TextField()

    def __str__(self):
        return '{}'.format(self.nombre)