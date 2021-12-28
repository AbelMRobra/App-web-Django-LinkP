from rest_framework import serializers
from .models import Articulos, Bitacoras, Presupuestos, TareasProgramadas
from proyectos.models import Proyectos


class ArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulos
        fields = ('__all__')

class ProyectosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyectos
        fields = ('id', 'presupuesto', 'nombre')

class PresupuestosSerializer(serializers.ModelSerializer):

    proyecto = ProyectosSerializer(many = False)
    proyecto_base = ProyectosSerializer(many = False)
    class Meta:
        model = Presupuestos
        fields = ('id', 'proyecto', 'proyecto_base')

class BitacorasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacoras
        fields = ('id', 'titulo', 'hashtag', 'descrip', 'fecha')

class TareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareasProgramadas
        fields = ('id', 'tarea', 'estado')

