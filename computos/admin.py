from django.contrib import admin
from .models import ListaRubros, Tipologias, Plantas, Computos

class PlantasAdmin(admin.ModelAdmin):
    list_display = ('nombre', )

class TipologiasAdmin(admin.ModelAdmin):
    list_display = ('rubro', 'nombre')

class ComputosAdmin(admin.ModelAdmin):
    readonly_fields = ('fecha_a', )
    list_display = ('proyecto', 'planta', 'rubro', 'tipologia', 'fecha_a', 'valor_total', 'valor_obra')
    search_fields = ('proyecto__nombre', 'planta__nombre', 'rubro__nombre', 'tipologia__nombre', 'fecha_a', 'valor_total', 'valor_obra')


# Register your models here.
admin.site.register(Computos, ComputosAdmin)
admin.site.register(ListaRubros)
admin.site.register(Tipologias, TipologiasAdmin)
admin.site.register(Plantas, PlantasAdmin)
