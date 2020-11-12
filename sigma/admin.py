from django.contrib import admin
from .models import Inventario, Tarea, SubTarea
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class InventarioResource(resources.ModelResource):
    class Meta:
        model = Inventario
       
class InventarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('num_inv', 'articulo',  'fecha_compra', 'amortizacion')
    search_fields = ('num_inv', 'articulo__nombre',  'fecha_compra', 'amortizacion')
    resources_class = InventarioResource

class TareaResource(resources.ModelResource):
    class Meta:
        model = Tarea
       
class TareaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'unidad',  'vinculacion', 'rend')
    search_fields = ('nombre', 'unidad',  'vinculacion__nombre', 'rend')
    resources_class = TareaResource

class SubTareaResource(resources.ModelResource):
    class Meta:
        model = SubTarea
       
class SubTareaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'vinculacion',  'unidad', 'rend')
    search_fields = ('nombre', 'vinculacion__nombre',  'unidad', 'rend')
    resources_class = SubTareaResource


admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(SubTarea, SubTareaAdmin)
