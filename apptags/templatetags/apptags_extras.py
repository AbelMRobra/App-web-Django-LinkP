from __future__ import unicode_literals
from django import template
import datetime
from datetime import date
from datetime import datetime, timedelta 
from rrhh.models import datosusuario

register = template.Library()

@register.filter('date_informe')
def date_informe(fecha_informe):

    hoy = date.today()

    fecha_cierre_informe = date(fecha_informe.year, (fecha_informe.month + 1), 4)

    if fecha_cierre_informe > hoy:

        return 1

    else:

        return 0

@register.filter('fecha')
def fecha(fecha):

    hoy = date.today()
    hoy = str(hoy.year)+str(hoy.month)

    return hoy



@register.filter('logo')
def logo(identificacion):

    try:

        usuario = datosusuario.objects.get(identificacion = identificacion)

        return usuario.imagenlogo.url


    except:

        return "{% static 'img/avatar.png' %}"

@register.filter('has_group')
def has_group(user, group_name):
    """
    Verifica se este usuário pertence a un grupo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False


@register.filter('fecha_prueba')
def is_past_due(self):

    if date.today() >= self:

       return True
    else:
        return False

@register.filter('planificacion')
def prueba_planificacion(self):

    fecha_nueva = self - datetime.timedelta(self.weekday())

    fecha_cadena = str(fecha_nueva.year)+'-'+str(fecha_nueva.month)+'-'+str(fecha_nueva.day)

    return fecha_cadena

@register.filter('estadoplan')
def prueba_planificacion(self):

    if self == "LISTO":
        return "77, 142, 62"

    if self == "TRABAJANDO":
        return "192, 173, 52"

    if self == "PROBLEMAS":
        return "192, 71, 52 "

    if self == "ESPERA":
        return "122, 118, 117"

@register.filter('este_mes')
def este_mes(self):

    hoy = date.today()

    if self == None:
        return 0
    else:

        if self.month == hoy.month:

            return 1
        else:
            return 0

@register.filter('years')
def este_mes(self):

    hoy = date.today()

    if self == None:
        return 0
    else:

        return hoy.year - self.year 

@register.simple_tag
def is_past_evaluacion1(prueba):

    if prueba < 0:

       return "34, 201, 24 "
    else:
        return "201, 55, 24"



@register.simple_tag
def is_past_evaluacion2(prueba):

    if prueba == None:

        return "32, 34, 161"

    elif prueba >= 0:

       return "34,187,51"
    else:
        return "187,33,36"

@register.simple_tag
def is_past_evaluacion3(prueba):

    if prueba == None:

        return "32, 34, 161"

    elif prueba == "PREVISTO":

       return "34, 201, 24 "
    else:
        return "201, 55, 24"

@register.simple_tag
def usuario(identificacion):

    data = datosusuario.objects.get(identificacion = identificacion)

    return data.imagenlogo.url

@register.simple_tag
def fecha_final_planif(fecha, estado):

    if fecha:

        if date.today() >= fecha and estado != "LISTO":
            return "238, 48, 14"

        elif date.today() >= fecha and estado == "LISTO":
            return "41, 166, 60"

        else:
            return "122, 118, 117"

@register.simple_tag
def fecha_inicio_planif(fecha_i, estado_i):

    if fecha_i:

        if date.today() >= fecha_i and estado_i == "ESPERA":
            return "238, 48, 14"

        elif date.today() >= fecha_i and estado_i != "ESPERA":
            return "41, 166, 60"

        else:
            return "122, 118, 117"

@register.simple_tag
def sp():

    try:
        aux = datosusuario.objects.get(identificacion = "SP").imagenlogo
        return aux.url

    except:
        return "{% static 'img/avatar.png' %}"

@register.simple_tag
def gannt(fecha_gant, fecha_inicial, fecha_final):

    hoy = date.today()

    fecha_semana_hoy = hoy - timedelta(hoy.weekday())

    if fecha_final == None or fecha_inicial == None:

        if fecha_gant == fecha_semana_hoy:

            # Estamos en esta semana

            return "background: rgba(230, 231, 243); border-left-style: solid; border-left-color: rgb(188, 55, 27); color: rgba(255, 255, 255, .4)"

        else:

            # No estamos en esta semana

            return "background: rgba(230, 231, 243); color: rgba(255, 255, 255, .4)"

    else:

        fecha_semana = fecha_inicial - timedelta(fecha_inicial.weekday())
        fecha_semana_final = fecha_final - timedelta(fecha_inicial.weekday())
        
        if fecha_gant < fecha_semana:

            if fecha_gant == fecha_semana_hoy:

                # Significa que la tarea no inicio pero no termino y estamos en esta semana

                return "background: rgba(230, 231, 243); border-left-style: solid; border-left-color: rgb(188, 55, 27); color: rgba(255, 255, 255, .4)"

            else:

                # Significa que la tarea no inicio

                return "background: rgba(230, 231, 243); color: rgba(255, 255, 255, .4)"

        elif fecha_gant > fecha_semana:

          
            if fecha_gant < fecha_semana_final:

                # Significa que la tarea ya inicio pero no termino

                if fecha_gant == fecha_semana_hoy:

                    # Significa que la tarea ya inicio pero no termino y estamos en esta semana

                    return "background: rgba(119, 170, 70); border-left-style: solid; border-left-color: rgb(188, 55, 27); color: rgba(255, 255, 255, .4)"

                else:

                    return "background: rgba(119, 170, 70); color: rgba(255, 255, 255, .4)"

            else:

                # Significa que la tarea ya termino

                if fecha_gant == fecha_semana_hoy:

                    # Significa que la tarea ya inicio pero no termino y estamos en esta semana

                    return "background: rgba(230, 231, 243); border-left-style: solid; border-left-color: rgb(188, 55, 27); color: rgba(255, 255, 255, .4)"

                else:

                    return "background: rgba(230, 231, 243); color: rgba(255, 255, 255, .4)"


        else:

            # Significa que esta semana inicia la tarea

            if fecha_gant == fecha_semana_hoy:

                return "background: rgba(119, 170, 70); border-left-style: solid; border-left-color: rgb(188, 55, 27); color: rgba(255, 255, 255, .4)"
            else:
                return "background: rgba(230, 231, 243); color: rgba(255, 255, 255, .4)"


@register.simple_tag
def thisweek(fecha_inicial_tw, fecha_final_tw):

    hoy = date.today()

    fecha_semana_hoy_tw = hoy - timedelta(hoy.weekday())

    if fecha_final_tw == None or fecha_inicial_tw == None:

        return 0

    else:

        fecha_semana_tw = fecha_inicial_tw - timedelta(fecha_inicial_tw.weekday())
        fecha_semana_final_tw = fecha_final_tw - timedelta(fecha_inicial_tw.weekday())
        
        if fecha_semana_tw == fecha_semana_hoy_tw:
            return 1
        elif  (fecha_semana_tw < fecha_semana_hoy_tw) and (fecha_final_tw > fecha_semana_hoy_tw):
            return 1

        else:
            return 0




