from django.contrib import admin
from .models import Proyectos
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

admin.site.register(Proyectos, ProyectosAdmin)
