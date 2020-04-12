from django.contrib import admin
from .models import Proyectos
from .models import Contratos
from .models import Certificados

# Register your models here.

admin.site.register(Proyectos)
admin.site.register(Contratos)
admin.site.register(Certificados)
