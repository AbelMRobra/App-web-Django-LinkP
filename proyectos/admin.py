from django.contrib import admin
from .models import Proyectos, Unidades
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ProyectosResource(resources.ModelResource):
    class Meta:
        model = Proyectos

class ProyectosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre','m2', 'descrip')
    search_fields = ('nombre','m2', 'descrip')
    resources_class = ProyectosResource

class UnidadesResource(resources.ModelResource):
    class Meta:
        model = Unidades

class UnidadesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto','piso_unidad', 'nombre_unidad')
    search_fields = ('proyecto__nombre','piso_unidad', 'nombre_unidad')
    resources_class = UnidadesResource



admin.site.register(Proyectos, ProyectosAdmin)
admin.site.register(Unidades, UnidadesAdmin)
