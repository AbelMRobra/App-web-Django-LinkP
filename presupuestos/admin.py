from django.contrib import admin
from .models import Constantes, Articulos, DatosProyectos, Presupuestos, Prametros, Desde, Analisis, CompoAnalisis, Capitulos, Modelopresupuesto, Registrodeconstantes, InformeMensual, Bitacoras, PresupuestosAlmacenados
from .models import DocumentacionProyectoPresupuesto
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
    search_fields = ('codigo', 'nombre')
    resources_class = ArticulosResource

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
    list_display = ('analisis','articulo',   'cantidad')
    search_fields = ('articulo__nombre', 'analisis__nombre',  'cantidad')
    resources_class = CompoAnalisisResource

class ConstantesResource(resources.ModelResource):
    class Meta:
        model = Constantes

class ConstantesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre','valor', 'descrip')
    search_fields = ('nombre','valor', 'descrip')
    resources_class = ConstantesResource

class ModeloPreResource(resources.ModelResource):
    class Meta:
        model = Modelopresupuesto

class ModelopresupuestoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'capitulo',  'analisis', 'vinculacion', 'cantidad')
    search_fields = ('proyecto__nombre', 'capitulo__nombre',  'analisis__nombre')
    resources_class = ModeloPreResource

class CapituloResource(resources.ModelResource):
    class Meta:
        model = Modelopresupuesto

class CapituloAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resources_class = ModeloPreResource

class RegistrodeConstanteResource(resources.ModelResource):
    class Meta:
        model = Registrodeconstantes

class RegistrodeConstanteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('constante', 'valor',  'fecha')
    search_fields = ('constante__nombre', 'valor', 'fecha')
    resources_class = RegistrodeConstanteResource

class InformeMensualResource(resources.ModelResource):
    class Meta:
        model = InformeMensual

class InformeMensualAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha', 'user')
    search_fields = ('fecha', 'user__identificacion')
    resources_class = InformeMensualResource

class BitacorasResource(resources.ModelResource):
    class Meta:
        model = Bitacoras

class BitacorasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha', 'proyecto')
    search_fields = ('fecha', 'proyecto__nombre')
    resources_class = BitacorasResource

class PresupuestosAlmacenadosResource(resources.ModelResource):
    class Meta:
        model = PresupuestosAlmacenados

class PresupuestosAlmacenadosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'nombre')
    resources_class = PresupuestosAlmacenadosResource

class PrametrosResource(resources.ModelResource):
    class Meta:
        model = Prametros

class PrametrosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'imprevitso')
    resources_class = PrametrosResource

admin.site.register(PresupuestosAlmacenados, PresupuestosAlmacenadosAdmin)
admin.site.register(Constantes, ConstantesAdmin)
admin.site.register(Registrodeconstantes, RegistrodeConstanteAdmin)
admin.site.register(Capitulos, CapituloAdmin)
admin.site.register(Articulos, ArticulosAdmin)
admin.site.register(DatosProyectos)
admin.site.register(Presupuestos)
admin.site.register(Prametros, PrametrosAdmin)
admin.site.register(Desde)
admin.site.register(Analisis, AnalisisAdmin)
admin.site.register(CompoAnalisis, CompoAnalisisAdmin)
admin.site.register(Modelopresupuesto, ModelopresupuestoAdmin)
admin.site.register(InformeMensual, InformeMensualAdmin)
admin.site.register(Bitacoras, BitacorasAdmin)
admin.site.register(DocumentacionProyectoPresupuesto)

