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