from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
   path('clientes/' ,login_required(views.clientes),name='clientes'),
   path('modificarcliente/<int:id>' ,login_required(views.modificarcliente),name='modificarcliente'),
   path('crearconsulta/',login_required(views.crearconsulta.as_view()),name='crearconsulta'),
   path('estadisticascrm/',login_required(views.estadisticas),name='Estadisticas CRM'),
   path('eliminarconsulta/',login_required(views.eliminarconsulta),name='eliminarconsulta'),
]