from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.projects), name = 'Proyectos'),
    url(r'^certificados$', login_required(views.certificados), name = 'Certificados'),

]