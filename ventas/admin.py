from django.contrib import admin
from .models import PricingResumen, VentasRealizadas, EstudioMercado, Pricing
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class PricingResource(resources.ModelResource):
    class Meta:
        model = Pricing
        
class PricingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('unidad', 'frente',  'piso_intermedio', 'cocina_separada')
    search_fields = ('unidad', 'frente',  'piso_intermedio', 'cocina_separada')
    resources_class = PricingResource

class PricingResumenResource(resources.ModelResource):
    class Meta:
        model = PricingResumen
        
class PricingResumenAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'fecha',  'precio_prom_contado', 'precio_prom_financiado')
    search_fields = ('proyecto__nombre', 'fecha',  'precio_prom_contado', 'precio_prom_financiado')
    resources_class = PricingResumenResource

class VentasRealizadasResource(resources.ModelResource):
    class Meta:
        model = VentasRealizadas
        
class VentasRealizadasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'fecha', 'comprador')
    search_fields = ('proyecto__nombre', 'fecha', 'comprador')
    resources_class = VentasRealizadasResource

class EstudioMercadoResource(resources.ModelResource):
    class Meta:
        model = EstudioMercado
        
class EstudioMercadoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha', 'empresa', 'proyecto', 'precio')
    search_fields = ('fecha', 'empresa', 'proyecto', 'precio')
    resources_class = EstudioMercadoResource

admin.site.register(PricingResumen, PricingResumenAdmin)
admin.site.register(Pricing, PricingAdmin)
admin.site.register(VentasRealizadas, VentasRealizadasAdmin)
admin.site.register(EstudioMercado, EstudioMercadoAdmin)
