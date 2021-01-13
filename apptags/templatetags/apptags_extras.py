from __future__ import unicode_literals
from django import template
from datetime import date

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
        return "122, 118, 117 "

