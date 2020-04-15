from django.contrib import admin
from .models import Constantes, Articulos, DatosProyectos, Presupuestos, Prametros, Desde

# Register your models here.

admin.site.register(Constantes)
admin.site.register(Articulos)
admin.site.register(DatosProyectos)
admin.site.register(Presupuestos)
admin.site.register(Prametros)
admin.site.register(Desde)
