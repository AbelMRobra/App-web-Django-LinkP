from django.contrib import admin
from .models import Constantes, Articulos, DatosProyectos, Presupuestos, Prametros, Desde, Analisis, CompoAnalisis, Capitulos, Modelopresupuesto
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ArticulosResource(resources.ModelResource):
    class Meta:
        model = Articulos
        import_id_fields = ('codigo',)
        fields = ('codigo', 'nombre', 'valor', 'valor_aux', 'constante__nombre', 'descrip', 'unidad', 'fecha_c', 'fecha_a')

class ArticulosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('codigo', 'nombre',  'valor', 'constante')
    search_fields = ('codigo', 'nombre',  'valor', 'constante')
    resources_class = ArticulosResource

class ModelopresupuestoAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'capitulo',  'analisis', 'vinculacion', 'cantidad')
    search_fields = ('proyecto__nombre', 'capitulo__nombre',  'analisis__nombre')


class AnalisisResource(resources.ModelResource):
    class Meta:
        model = Analisis

class AnalisisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('codigo', 'nombre',  'unidad')
    search_fields = ('codigo', 'nombre',  'unidad')
    resources_class = AnalisisResource


class CompoAnalisisResource(resources.ModelResource):
    class Meta:
        model = CompoAnalisis

class CompoAnalisisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('articulo', 'analisis',  'cantidad')
    search_fields = ('articulo__nombre', 'analisis__nombre',  'cantidad')
    resources_class = CompoAnalisisResource
    

admin.site.register(Constantes)
admin.site.register(Capitulos)
admin.site.register(Articulos, ArticulosAdmin)
admin.site.register(DatosProyectos)
admin.site.register(Presupuestos)
admin.site.register(Prametros)
admin.site.register(Desde)
admin.site.register(Analisis, AnalisisAdmin)
admin.site.register(CompoAnalisis, CompoAnalisisAdmin)
admin.site.register(Modelopresupuesto, ModelopresupuestoAdmin)
