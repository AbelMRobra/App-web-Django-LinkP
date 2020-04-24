from django.contrib import admin
from .models import RegistroConstantes
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

admin.site.register(RegistroConstantes, RegistrosConstanteAdmin)
