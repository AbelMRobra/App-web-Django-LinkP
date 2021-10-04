from django.urls import path, re_path
from django.conf.urls import url
from . import views
from curvas.api_rest import viewsets
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('curvasprincipal' , views.curvas_principal , name='curvas'),
    # path('api' , viewsets.prueba().as_view() , name='api'),
    path('apicurvas' , viewsets.APICurvas.as_view() , name='api'),
    
]