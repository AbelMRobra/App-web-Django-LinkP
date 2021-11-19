import os
import datetime
from django.shortcuts import render
from django.views.generic.base import View 
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse

from xhtml2pdf import pisa
from ventas.models import FormularioSolucionPostventa, ReclamosPostventa, FormularioDetallePostventa

class Formulario_detalle(View):

    def link_callback(self, uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

            # make sure that file exists
            if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
            return path

    def get(self, request, id_reclamo, *args, **kwargs):

        #Creamos la información

        dato_reclamo = ReclamosPostventa.objects.get(id = id_reclamo) 

        datos_formulario = FormularioDetallePostventa.objects.filter(reclamo = dato_reclamo).order_by("-id")[0]

        # Aqui llamamos y armamos el PDF
      
        template = get_template('postventa/postventa_PDF_formuario_2.html')
        contexto = {
            'datos_formulario':datos_formulario, 
            'fecha':datetime.date.today(),
            'logo':'{}{}'.format(settings.STATIC_URL, 'img/link.png'),
            'cabecera':'{}{}'.format(settings.STATIC_URL, 'img/fondo.png'),
            'fondo':'{}{}'.format(settings.STATIC_URL, 'img/fondo.jpg')}
        
        
        html = template.render(contexto)
        response = HttpResponse(content_type = "application/pdf")
        
        #response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        
        pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
        
        if pisaStatus.err:
            
            return HttpResponse("Hay un error")

        return response


class Formulario_solucion(View):

    def link_callback(self, uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

            # make sure that file exists
            if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
            return path

    def get(self, request, id_reclamo, *args, **kwargs):

        #Creamos la información

        dato_reclamo = ReclamosPostventa.objects.get(id = id_reclamo) 

        datos_formulario = FormularioSolucionPostventa.objects.filter(reclamo = dato_reclamo).order_by("-id")[0]

        # Aqui llamamos y armamos el PDF
      
        template = get_template('postventa/postventa_PDF_formuario_1.html')
        contexto = {
            'datos_formulario':datos_formulario, 
            'fecha':datetime.date.today(),
            'logo':'{}{}'.format(settings.STATIC_URL, 'img/link.png'),
            'cabecera':'{}{}'.format(settings.STATIC_URL, 'img/fondo.png'),
            'fondo':'{}{}'.format(settings.STATIC_URL, 'img/fondo.jpg')}
        
        
        html = template.render(contexto)
        response = HttpResponse(content_type = "application/pdf")
        
        #response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        
        pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
        
        if pisaStatus.err:
            
            return HttpResponse("Hay un error")

        return response