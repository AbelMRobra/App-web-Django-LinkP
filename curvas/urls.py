from django.urls import path, re_path
from django.conf.urls import url
from . import views
from curvas.api_rest import viewsets
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('curvasprincipal' , views.curvas_principal , name='curvas'),
    path('api_curva' , viewsets.curva_inversion().as_view() , name='API Curva de inversion'),
    
]