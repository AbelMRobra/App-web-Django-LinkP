from django.contrib import admin
from .models import Proveedores, Contratos, Certificados, StockComprasAnticipadas, Compras

# Register your models here.

admin.site.register(Proveedores)
admin.site.register(Compras)
admin.site.register(Contratos)
admin.site.register(Certificados)
admin.site.register(StockComprasAnticipadas)