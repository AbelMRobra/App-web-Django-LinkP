import numpy as np
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rrhh.models import MonedaLink, EntregaMoneda, CanjeMonedas


class LinkcoinsViewset(viewsets.GenericViewSet):
    queryset = MonedaLink.objects.all()
    permission_classes = (AllowAny,)

    @action(detail=True, methods=["GET"])
    def reporte(self, request, ident=None):
        quey_canje = CanjeMonedas.objects.filter(usuario__identificacion=ident).count()
        monedas_generadas = MonedaLink.objects.filter(usuario_portador__identificacion=ident).count()
        monedas_recibidas = EntregaMoneda.objects.filter(usuario_recibe__identificacion=ident).count()
        monedas_canjeadas = sum(np.array(quey_canje.values_list('monedas', flat=True)))
        canjes_pendientes = quey_canje.filter(entregado='NO').count()
        ultimo_canje = quey_canje.order_by('-fecha').first()
        ultimo_canje = ultimo_canje.premio if ultimo_canje else ""

        response = {
            'monedas_generadas' : monedas_generadas,
            'monedas_recibidas' : monedas_recibidas,
            'monedas_canjeadas' : monedas_canjeadas,
            'canjes_pendientes' : canjes_pendientes,
            'ultimo_canje' : ultimo_canje,
        }

        return Response(response, status=status.HTTP_200_OK)