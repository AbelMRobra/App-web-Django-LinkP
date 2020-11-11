from django.contrib import admin
from .models import Almacenero, CuentaCorriente, Cuota, RegistroAlmacenero, Pago, ArchivosAdmFin, Arqueo, RetirodeSocios
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class RegistroAlmaceneroResource(resources.ModelResource):
    class Meta:
        model = RegistroAlmacenero

class RegistroAlmaceneroAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'ingreso_ventas')
    search_fields = ('proyecto_nombre' , 'ingreso_ventas')
    readonly_fields = ('fecha', 'proyecto', 'cheques_emitidos', 'gastos_fecha', 'pendiente_admin', 'pendiente_comision', 'pendiente_adelantos', 'pendiente_iva_ventas', 'pendiente_iibb_tem', 'prestamos_proyecto', 'prestamos_otros', 'cuotas_cobradas', 'cuotas_a_cobrar', 'ingreso_ventas', 'Prestamos_dados', 'unidades_socios', 'saldo_mat', 'saldo_mo', 'imprevisto', 'credito', 'fdr')
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

class PagoResource(resources.ModelResource):
    class Meta:
        model = Pago

class PagoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha', 'pago')
    search_fields = ('fecha' , 'pago')
    resources_class = PagoResource

class ArchivosAdmFinResource(resources.ModelResource):
    class Meta:
        model = ArchivosAdmFin

class ArchivosAdmFinAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['fecha']
    search_fields = ['fecha']
    resources_class = ArchivosAdmFinResource

class ArqueoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['fecha']
    search_fields = ['fecha']


class RetirodeSociosResource(resources.ModelResource):
    class Meta:
        model = RetirodeSocios

class RetiroSociosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['fecha', 'monto_pesos', 'comentario']
    search_fields = ['fecha', 'monto_pesos', 'comentario']
    resources_class = RetirodeSociosResource

admin.site.register(RegistroAlmacenero, RegistroAlmaceneroAdmin)
admin.site.register(Almacenero, AlmaceneroAdmin)
admin.site.register(CuentaCorriente, CuentaCorrienteAdmin)
admin.site.register(Cuota, CuotaAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(ArchivosAdmFin, ArchivosAdmFinAdmin)
admin.site.register(Arqueo, ArqueoAdmin)
admin.site.register(RetirodeSocios, RetiroSociosAdmin)
