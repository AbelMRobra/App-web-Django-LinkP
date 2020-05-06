from django.contrib import admin
from .models import RegistroConstantes, RegistroValorProyecto
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class RegistrosConstanteResource(resources.ModelResource):
    class Meta:
        model = RegistroConstantes

class RegistrosConstanteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('constante', 'valor',  'fecha')
    search_fields = ('constante', 'valor',  'fecha')
    resources_class = RegistrosConstanteResource

class RegistroValorProyectoResource(resources.ModelResource):
    class Meta:
        model = RegistroValorProyecto

class RegistroValorProyectoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'fecha', 'precio_proyecto')
    search_fields = ('proyecto__nombre',  'fecha', 'precio_proyecto')
    resources_class = RegistroValorProyectoResource


admin.site.register(RegistroConstantes, RegistrosConstanteAdmin)
admin.site.register(RegistroValorProyecto, RegistroValorProyectoAdmin)
