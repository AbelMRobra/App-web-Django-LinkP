from django.http import response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from compras.models import Proveedores
from compras.serializers.serializers_proveedores import ProveedoresSerializer


class ProveedoresViewset(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedoresSerializer
    permission_classes = (AllowAny,)