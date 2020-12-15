from django.contrib import admin
from .models import Etapas, ItemEtapa
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class EtapasResource(resources.ModelResource):
    class Meta:
        model = Etapas

class EtapasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'nombre')
    search_fields = ('proyecto__nombre','nombre')
    resources_class = EtapasResource

class ItemEtapaResource(resources.ModelResource):
    class Meta:
        model = Etapas

class ItemEtapaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('etapa', 'nombre')
    search_fields = ('etapa__nombre','nombre')
    resources_class = ItemEtapaResource

admin.site.register(Etapas, EtapasAdmin)
admin.site.register(ItemEtapa, ItemEtapaAdmin)