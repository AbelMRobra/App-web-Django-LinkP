from django.contrib import admin
from .models import Almacenero, CuentaCorriente, Cuota, RegistroAlmacenero
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class RegistroAlmaceneroResource(resources.ModelResource):
    class Meta:
        model = RegistroAlmacenero

class RegistroAlmaceneroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'ingreso_ventas')
    search_fields = ('proyecto_nombre' , 'ingreso_ventas')
    resources_class = RegistroAlmaceneroResource

class AlmaceneroResource(resources.ModelResource):
    class Meta:
        model = Almacenero

class AlmaceneroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'ingreso_ventas')
    search_fields = ('proyecto_nombre' , 'ingreso_ventas')
    resources_class = AlmaceneroResource

class CuentaCorrienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('venta', )

class CuotaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha', )

admin.site.register(RegistroAlmacenero, RegistroAlmaceneroAdmin)
admin.site.register(Almacenero, AlmaceneroAdmin)
admin.site.register(CuentaCorriente, CuentaCorrienteAdmin)
admin.site.register(Cuota, CuotaAdmin)
