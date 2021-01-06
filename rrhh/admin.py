from django.contrib import admin
from .models import datosusuario, mensajesgenerales, NotaDePedido, Vacaciones
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


class NotasDePedidoResource(resources.ModelResource):
    class Meta:
        model = NotaDePedido

class NotasDePedidoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('titulo', 'creador', 'destinatario')
    search_fields = ('titulo', 'creador', 'destinatario')
    resources_class = NotasDePedidoResource

class VacacionesResource(resources.ModelResource):
    class Meta:
        model = Vacaciones

class VacacionesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'fecha_final')
    search_fields = ('usuario__nombre', 'fecha_inicio', 'fecha_final')
    resources_class = NotasDePedidoResource

admin.site.register(datosusuario, DatosUserAdmin)
admin.site.register(mensajesgenerales, MensajesGeneralesAdmin)
admin.site.register(NotaDePedido, NotasDePedidoAdmin)
admin.site.register(Vacaciones, VacacionesAdmin)