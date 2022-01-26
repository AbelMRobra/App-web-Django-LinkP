from django.contrib import admin
from .models import DosierDeVenta, PricingResumen, VentasRealizadas, EstudioMercado, Pricing, ArchivosAreaVentas, ArchivoFechaEntrega, \
                ArchivoVariacionHormigon, ReclamosPostventa, FeaturesProjects, Clientescontacto, ImgEnlacesProyecto, \
                    ArchivosComercial, ClasificacionReclamosPostventa, FormularioDetallePostventa, FormularioSolucionPostventa
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ClientescontactoResource(resources.ModelResource):
    class Meta:
        model = Clientescontacto
        
class ClientescontactoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'apellido',  'email')
    search_fields = ('nombre', 'apellido',  'email')
    resources_class = ClientescontactoResource

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
    list_display = ('proyecto', 'unidad', 'fecha', 'comprador')
    search_fields = ('proyecto__nombre','unidad__nombre_unidad','unidad__piso_unidad', 'fecha', 'comprador')
    resources_class = VentasRealizadasResource

class EstudioMercadoResource(resources.ModelResource):
    class Meta:
        model = EstudioMercado

class ArchivosComercialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'proyecto')
    search_fields = ('nombre', 'fecha', )
    resources_class = ArchivosComercial
        
class EstudioMercadoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha', 'empresa', 'proyecto', 'precio')
    search_fields = ('fecha', 'empresa', 'proyecto', 'precio')
    resources_class = EstudioMercadoResource

class ArchivosResource(resources.ModelResource):
    class Meta:
        model = ArchivosAreaVentas
        
class ArchivosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha',)
    resources_class = ArchivosResource

class ArchivoFechaEntregaResource(resources.ModelResource):
    class Meta:
        model = ArchivoFechaEntrega
        
class ArchivoFechaEntregaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha',)
    resources_class = ArchivoFechaEntregaResource

class ArchivoVariacionHormigonResource(resources.ModelResource):
    class Meta:
        model = ArchivoVariacionHormigon
        
class ArchivoVariacionHormigonAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha',)
    resources_class = ArchivoVariacionHormigonResource

class ReclamosPostventaResource(resources.ModelResource):
    class Meta:
        model = ReclamosPostventa
        
class ReclamosPostventaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('numero', 'proyecto', 'propietario', 'usuario', 'unidad', 'clasificacion')
    search_fields = ('proyecto', 'propietario', 'clasificacion')
    resources_class = ReclamosPostventaResource

class FeaturesProjectsResource(resources.ModelResource):
    class Meta:
        model = FeaturesProjects
        
class FeaturesProjectsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('proyecto', 'nombre')
    resources_class = FeaturesProjectsResource

class ClasificacionReclamosPostventaResource(resources.ModelResource):
    class Meta:
        model = ClasificacionReclamosPostventa

class ClasificacionReclamosPostventaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'nombre')
    resources_class = ClasificacionReclamosPostventaResource

admin.site.register(ClasificacionReclamosPostventa, ClasificacionReclamosPostventaAdmin)
admin.site.register(Clientescontacto, ClientescontactoAdmin)
admin.site.register(FeaturesProjects, FeaturesProjectsAdmin)
admin.site.register(PricingResumen, PricingResumenAdmin)
admin.site.register(Pricing, PricingAdmin)
admin.site.register(VentasRealizadas, VentasRealizadasAdmin)
admin.site.register(ArchivosComercial, ArchivosComercialAdmin)
admin.site.register(EstudioMercado, EstudioMercadoAdmin)
admin.site.register(ArchivosAreaVentas, ArchivosAdmin)
admin.site.register(ArchivoFechaEntrega, ArchivoFechaEntregaAdmin)
admin.site.register(ArchivoVariacionHormigon, ArchivoVariacionHormigonAdmin)
admin.site.register(ReclamosPostventa, ReclamosPostventaAdmin)
admin.site.register(ImgEnlacesProyecto)
admin.site.register(DosierDeVenta)
admin.site.register(FormularioSolucionPostventa)
admin.site.register(FormularioDetallePostventa)
