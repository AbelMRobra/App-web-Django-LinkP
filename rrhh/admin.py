from django.contrib import admin
from .models import datosusuario, mensajesgenerales, NotaDePedido, Vacaciones, MonedaLink, EntregaMoneda, Anuncios, Seguimiento, PremiosMonedas, RegistroContable, CanjeMonedas, Minutas, Sugerencia, DicRegistroContable
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class DicRegistroContableResource(resources.ModelResource):
    class Meta:
        model = DicRegistroContable

class DicRegistroContableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('entrada', 'salida')
    search_fields = ('entrada', 'salida')
    resources_class = DicRegistroContableResource

class DatosUserResource(resources.ModelResource):
    class Meta:
        model = datosusuario

class DatosUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('identificacion', 'area',  'cargo')
    search_fields = ('identificacion', 'area',  'cargo')
    resources_class = DatosUserResource

class RegistroContableResource(resources.ModelResource):
    class Meta:
        model = RegistroContable

class RegistroContableAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'nota',  'categoria')
    search_fields = ('usuari__identificacion', 'nota',  'categoria')
    resources_class = RegistroContableResource

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

class SeguimientoResource(resources.ModelResource):
    class Meta:
        model = Seguimiento

class SeguimientoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'area')
    search_fields = ('nombre', 'area')
    resources_class = SeguimientoResource

class PremiosMonedasResource(resources.ModelResource):
    class Meta:
        model = PremiosMonedas

class PremiosMonedasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'cantidad')
    search_fields = ('nombre', 'cantidad')
    resources_class = PremiosMonedasResource

class CanjeMonedasResource(resources.ModelResource):
    class Meta:
        model = CanjeMonedas

class CanjeMonedasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'premio', 'monedas', 'entregado')
    search_fields = ('usuario__identificacion', 'fecha', 'premio', 'monedas')
    resources_class = CanjeMonedasResource

class MinutasResource(resources.ModelResource):
    
    class Meta:
        model = Minutas

class MinutasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('creador', 'reunion')
    resources_class = MinutasResource

class SugerenciaResource(resources.ModelResource):
    
    class Meta:
        model = Sugerencia

class SugerenciaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('usuario', 'nombre')
    resources_class = SugerenciaResource

admin.site.register(DicRegistroContable, DicRegistroContableAdmin)
admin.site.register(Sugerencia, SugerenciaAdmin)
admin.site.register(Minutas, MinutasAdmin)
admin.site.register(RegistroContable, RegistroContableAdmin)
admin.site.register(datosusuario, DatosUserAdmin)
admin.site.register(PremiosMonedas, PremiosMonedasAdmin)
admin.site.register(CanjeMonedas, CanjeMonedasAdmin)
admin.site.register(mensajesgenerales, MensajesGeneralesAdmin)
admin.site.register(NotaDePedido, NotasDePedidoAdmin)
admin.site.register(Vacaciones, VacacionesAdmin)
admin.site.register(MonedaLink, MonedaLinkAdmin)
admin.site.register(EntregaMoneda, EntregaMonedaAdmin)
admin.site.register(Anuncios, AnunciosAdmin)
admin.site.register(Seguimiento, SeguimientoAdmin)