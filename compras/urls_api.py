from django.urls import path
from .api_rest.viewsets import ComprasViewSet, ComparativasViewSet, ProveedoresViewSet
from rest_framework import routers

route = routers.SimpleRouter()
route.register('compras_api', ComprasViewSet)
route.register('comparativas_api', ComparativasViewSet)
route.register('proveedores_api', ProveedoresViewSet)

urlpatterns = route.urls
