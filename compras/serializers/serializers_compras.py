from rest_framework import serializers
from compras.models import Compras, Proveedores
from presupuestos.models import Articulos, Capitulos
from proyectos.models import Proyectos

class ArticulosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Articulos
        fields = ('codigo', 'nombre', 'unidad', 'valor')

class ProveedoresSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Proveedores
        fields = ('id', 'name')

class ProyectosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Proyectos
        fields = ('id', 'nombre')

class CapitulosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Capitulos
        fields = ('id', 'nombre')

class ComprasFullSerializer(serializers.ModelSerializer):

    articulo = ArticulosSerializer(many = False)
    proveedor = ProveedoresSerializer(many = False)
    proyecto = ProyectosSerializer(many = False)
    capitulo = CapitulosSerializer(many = False)

    
    class Meta:
        model = Compras
        fields = ('id', 'proyecto', 'articulo', 'cantidad', 'precio', 'fecha_c', 'documento', 'proveedor', 'capitulo')

class ComprasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Compras
        fields = ('__all__')
