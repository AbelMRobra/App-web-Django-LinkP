from django.db import models
from constantes.models import Constantes

# Create your models here.

class Agenda(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=200)
    constante = models.ForeignKey(Constantes, null=True, blank=True, on_delete=models.CASCADE)
    valor = models.FloatField()
    valor_aux = models.FloatField(null=True)
    descrip = models.TextField()
    Unidad = models.CharField(max_length=10, blank=True,)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        verbose_name="Insumo"
        verbose_name_plural="Insumos"

    def __str__(self):
        return self.nombre
    

    
    