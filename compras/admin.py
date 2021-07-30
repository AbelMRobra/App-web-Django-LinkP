from django.contrib import admin
from .models import Proveedores, Contratos, Certificados, StockComprasAnticipadas, Compras, Retiros, Comparativas, ComparativasMensaje
from .models import AvisoOrdenesCompras
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ProveedoresResource(resources.ModelResource):
    class Meta:
        model = Proveedores

class ProveedoresAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resources_class = ProveedoresResource


class ComparativasMensajeResource(resources.ModelResource):
    class Meta:
        model = ComparativasMensaje

class ComparativasMensajeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'mensaje')
    search_fields = ('usuario__identificacion','mensaje')
    resources_class = ComparativasMensajeResource


class ComprasResource(resources.ModelResource):
    class Meta:
        model = Compras

class ComprasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'nombre',  'proveedor', 'articulo', 'cantidad', 'documento' )
    search_fields = ('proyecto__nombre','nombre',  'proveedor__name', 'articulo__nombre', 'cantidad', 'documento' )
    resources_class = ComprasResource

class RetirosResource(resources.ModelResource):
    class Meta:
        model = Retiros

class RetirosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('compra', 'articulo', 'cantidad')
    search_fields = ('articulo__nombre',)
    resources_class = RetirosResource

class ComparativasResource(resources.ModelResource):
    class Meta:
        model = Comparativas

class ComparativasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proveedor', 'proyecto','numero', 'monto', 'estado')
    search_fields = ('proveedor__name', 'proyecto','numero',  'estado', 'monto')
    readonly_fields = ('fecha_c', 'fecha_autorizacion', 'visto')
    resources_class = Comparativas

admin.site.register(AvisoOrdenesCompras)
admin.site.register(Proveedores, ProveedoresAdmin)
admin.site.register(Retiros, RetirosAdmin)
admin.site.register(Comparativas, ComparativasAdmin)
admin.site.register(ComparativasMensaje, ComparativasMensajeAdmin)
admin.site.register(Compras, ComprasAdmin)
admin.site.register(Contratos)
admin.site.register(Certificados)
admin.site.register(StockComprasAnticipadas)