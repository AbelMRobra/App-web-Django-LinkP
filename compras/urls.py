from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^certificados$', login_required(views.certificados), name = 'Certificados'),
    url(r'^proveedores$', login_required(views.proveedores), name = 'Proveedores'),
    url(r'^stockant$', login_required(views.stockant), name = 'Stock compras anticipadas'),
    url(r'^stockantingresar$', login_required(views.stockant_ingresar), name = 'Ingresar compra'),

]