from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^estmerc$', views.estmercado, name = 'Estudio de mercado'),
    url(r'^panelunidades$', views.panelunidades, name = 'Panel de unidades'),
    url(r'^pricing/(?P<id_proyecto>\d+)/$', views.pricing, name = 'Pricing'),
    url(r'^radiografia$', views.radiografia, name = 'Radiografia del cliente'),
    url(r'^resumenprecio$', views.resumenprecio, name = 'Resumen de precio'),

]