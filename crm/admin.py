from django.contrib import admin
from .models import Consulta, Tipologia
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ConsultaResource(resources.ModelResource):
    class Meta:
        model = Consulta

class ConsultaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('cliente', 'proyecto', 'medio_contacto')
    search_fields = ('cliente__nombre', 'proyecto__nombre', 'medio_contacto')
    resources_class = ConsultaResource

admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Tipologia)