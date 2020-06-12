from django.contrib import admin
from .models import Almacenero
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class AlmaceneroResource(resources.ModelResource):
    class Meta:
        model = Almacenero

class AlmaceneroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'ingreso_ventas')
    search_fields = ('proyecto_nombre' , 'ingreso_ventas')
    resources_class = AlmaceneroResource

admin.site.register(Almacenero, AlmaceneroAdmin)
