from django.urls import path, re_path
from django.conf.urls import url
from curvas.api_rest import viewsets
from django.contrib.auth.decorators import login_required


urlpatterns = [
   
    path('apicurvas' , viewsets.APICurvas.as_view() , name='api'),
    
]