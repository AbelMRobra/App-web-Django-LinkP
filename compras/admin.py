from django.contrib import admin
from .models import Proveedores, StockComprasAnticipadas

# Register your models here.

admin.site.register(Proveedores)
admin.site.register(StockComprasAnticipadas)