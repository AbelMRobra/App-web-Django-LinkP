from django.contrib import admin
from .models import datosusuario
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class DatosUserResource(resources.ModelResource):
    class Meta:
        model = datosusuario

class DatosUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('identificacion', 'area',  'cargo')
    search_fields = ('identificacion', 'area',  'cargo')
    resources_class = DatosUserResource

admin.site.register(datosusuario, DatosUserAdmin)