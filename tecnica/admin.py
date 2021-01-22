from django.contrib import admin
from .models import Etapas, ItemEtapa, SubItem, Lp, SubSubItem
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

class SubItemResource(resources.ModelResource):
    class Meta:
        model = SubItem

class SubItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('item', 'nombre')
    search_fields = ('item__nombre','nombre')
    resources_class = SubItemResource

class SubSubItemResource(resources.ModelResource):
    class Meta:
        model = SubSubItem

class SubSubItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('item', 'nombre')
    search_fields = ('item__nombre','nombre')
    resources_class = SubSubItemResource

class LpResource(resources.ModelResource):
    class Meta:
        model = Lp

class LpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'responsable')
    search_fields = ('proyecto__nombre','responsable_identificacion')
    resources_class = LpResource


admin.site.register(Etapas, EtapasAdmin)
admin.site.register(ItemEtapa, ItemEtapaAdmin)
admin.site.register(SubItem, SubItemAdmin)
admin.site.register(SubSubItem, SubSubItemAdmin)
admin.site.register(Lp, LpAdmin)