from __future__ import unicode_literals
from django import template
import datetime
from datetime import date
from datetime import datetime, timedelta 

register = template.Library()

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


