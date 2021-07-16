from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
   path('clientes/' ,views.clientes,name='clientes'),
   path('modificarcliente/<int:id>' ,views.modificarcliente,name='modificarcliente'),
   path('crearconsulta/',views.crearconsulta.as_view(),name='crearconsulta'),
   path('estadisticascrm/',views.estadisticas,name='Estadisticas CRM'),
   path('eliminarconsulta/',views.eliminarconsulta,name='eliminarconsulta'),
]