from django.contrib import admin
from .models import datosusuario, mensajesgenerales
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

class MensajesGeneralesResource(resources.ModelResource):
    class Meta:
        model = mensajesgenerales

class MensajesGeneralesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'mensaje')
    search_fields = ('usuario__identificacion', 'mensaje')
    resources_class = MensajesGeneralesResource

admin.site.register(datosusuario, DatosUserAdmin)
admin.site.register(mensajesgenerales, MensajesGeneralesAdmin)