from django.contrib import admin
from .models import Inventario
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class InventarioResource(resources.ModelResource):
    class Meta:
        model = Inventario
       
class InventarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('num_inv', 'articulo',  'fecha_compra', 'amortizacion')
    search_fields = ('num_inv', 'articulo__nombre',  'fecha_compra', 'amortizacion')
    resources_class = InventarioResource

admin.site.register(Inventario, InventarioAdmin)
