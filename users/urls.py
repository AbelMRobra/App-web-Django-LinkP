from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.welcome, name = 'Bienvenido'),
    url(r'^guia$', views.guia, name = 'Guia'),
    url(r'^register$', views.register, name = 'Registro'),
    url(r'^login$', views.login, name = 'Login'),
    url(r'^logout$', views.logout, name = 'Logout'),
    url(r'^inicio$', login_required(views.inicio), name = 'Inicio'),
    url(r'^accounts/login/$', views.welcome, name = 'Redicrección'),
    url(r'^dashboard$', views.dashboard, name = 'Dashboard'),
    url(r'^password$', login_required(views.password), name = 'Password'),

]