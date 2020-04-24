from django.contrib import admin
from .models import ListaRubros, Tipologias, Plantas, Computos
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class PlantasResource(resources.ModelResource):
    class Meta:
        model = Plantas

class PlantasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', )
    resources_class = PlantasResource


class TipologiasResource(resources.ModelResource):
    class Meta:
        model = Tipologias

class TipologiasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('rubro', 'nombre')
    search_fields = ('nombre', )
    resources_class = TipologiasResource


class ComputosResource(resources.ModelResource):
    class Meta:
        model = Computos

class ComputosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('fecha_a', )
    list_display = ('proyecto', 'planta', 'rubro', 'tipologia', 'fecha_a', 'valor_total', 'valor_obra')
    search_fields = ('proyecto__nombre', 'planta__nombre', 'rubro__nombre', 'tipologia__nombre', 'fecha_a', 'valor_total', 'valor_obra')
    resources_class = ComputosResource

# Register your models here.
admin.site.register(Computos, ComputosAdmin)
admin.site.register(ListaRubros)
admin.site.register(Tipologias, TipologiasAdmin)
admin.site.register(Plantas, PlantasAdmin)
