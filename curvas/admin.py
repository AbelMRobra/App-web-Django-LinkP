from django.contrib import admin

# Register your models here.
from .models import ComposicionesSubpartidas,SubPartidasCapitulos,PartidasCapitulos


admin.site.register(ComposicionesSubpartidas)
admin.site.register(SubPartidasCapitulos)
admin.site.register(PartidasCapitulos)