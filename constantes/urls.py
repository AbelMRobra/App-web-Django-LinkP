from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^cons_create/$', login_required(views.cons_create), name = 'Cons_create'),
    url(r'^$', login_required(views.cons_list), name = 'Cons_list'),
    url(r'^editar/(?P<id_cons>\d+)/$', login_required(views.cons_edit), name = 'Editar_cons'),
    url(r'^eliminar/(?P<id_cons>\d+)/$', login_required(views.cons_delete), name = 'Eliminar_cons'),

]