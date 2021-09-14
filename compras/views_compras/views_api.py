from django.http import JsonResponse, HttpResponse
from rest_framework.response import  Response
from rest_framework import status

from compras.models import Compras

def manualJson(request):

    data = Compras.objects.all()
    response = {'data': list(data.values("proyecto__nombre", "documento"))}

    return JsonResponse(response)