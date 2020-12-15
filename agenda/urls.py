"""agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   
    path('', include('users.urls')),
    path('presupuestos/', include('presupuestos.urls')),
    path('finanzas/', include('finanzas.urls')),
    path('proyectos/', include('proyectos.urls')),
    path('ventas/', include('ventas.urls')),
    path('computos/', include('computos.urls')),
    path('projects/', include('projects.urls')),
    path('compras/', include('compras.urls')),
    path('sigma/', include('sigma.urls')),
    path('rrhh/', include('rrhh.urls')),
    path('tecnica/', include('tecnica.urls')),
    path('admin/', admin.site.urls),

]

#if settings.DEBUG:
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

