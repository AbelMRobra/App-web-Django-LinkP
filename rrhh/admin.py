from django.contrib import admin
from .models import datosusuario, mensajesgenerales, NotaDePedido, Vacaciones, MonedaLink, EntregaMoneda, Anuncios
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

class MonedaLinkResource(resources.ModelResource):
    class Meta:
        model = MonedaLink

class MonedaLinkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'fecha')
    search_fields = ('nombre', 'fecha')
    resources_class = MonedaLinkResource

class EntregaMonedaResource(resources.ModelResource):
    class Meta:
        model = EntregaMoneda

class EntregaMonedaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('moneda', 'fecha')
    search_fields = ('moneda__nombre', 'fecha')
    resources_class = EntregaMonedaResource

class AnunciosResource(resources.ModelResource):
    class Meta:
        model = Anuncios

class AnunciosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria')
    search_fields = ('titulo', 'categoria')
    resources_class = AnunciosResource


admin.site.register(datosusuario, DatosUserAdmin)
admin.site.register(mensajesgenerales, MensajesGeneralesAdmin)
admin.site.register(NotaDePedido, NotasDePedidoAdmin)
admin.site.register(Vacaciones, VacacionesAdmin)
admin.site.register(MonedaLink, MonedaLinkAdmin)
admin.site.register(EntregaMoneda, EntregaMonedaAdmin)
admin.site.register(Anuncios, AnunciosAdmin)