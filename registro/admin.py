from django.contrib import admin
from .models import RegistroConstantes, RegistroValorProyecto, RegistroLeccionesAprendidasPresup, RegistroInformeRedes
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class RegistroInformeRedesResource(resources.ModelResource):
    class Meta:
        model = RegistroInformeRedes

class RegistroInformeRedesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resources_class = RegistroInformeRedesResource


class RegistrosConstanteResource(resources.ModelResource):
    class Meta:
        model = RegistroConstantes

class RegistrosConstanteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('constante', 'valor',  'fecha')
    search_fields = ( 'valor',  'fecha')
    resources_class = RegistrosConstanteResource

class RegistroValorProyectoResource(resources.ModelResource):
    class Meta:
        model = RegistroValorProyecto

class RegistroValorProyectoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'fecha', 'precio_proyecto')
    search_fields = ('proyecto__nombre',  'fecha', 'precio_proyecto')
    resources_class = RegistroValorProyectoResource

class RegistroLecAprenPresupResource(resources.ModelResource):
    class Meta:
        model = RegistroLeccionesAprendidasPresup

class RegistroLecAprenPresupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('area', 'nombre', 'confeciona', 'tema', 'fecha_actualizacion')
    search_fields = ('area', 'nombre', 'confeciona', 'tema', 'fecha_actualizacion')
    resources_class = RegistroLecAprenPresupResource


admin.site.register(RegistroConstantes, RegistrosConstanteAdmin)
admin.site.register(RegistroInformeRedes, RegistroInformeRedesAdmin)
admin.site.register(RegistroValorProyecto, RegistroValorProyectoAdmin)
admin.site.register(RegistroLeccionesAprendidasPresup, RegistroLecAprenPresupAdmin)
