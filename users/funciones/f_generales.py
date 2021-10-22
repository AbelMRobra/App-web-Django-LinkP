import datetime
from users.models import ActividadesUsuarios
from rrhh.models import datosusuario

def generales_registro_actividad(identificacion, categoria, accion):

    usuario = datosusuario.objects.get(identificacion = identificacion)
    now = datetime.datetime.now()

    nueva_actividad = ActividadesUsuarios(
        usuario = usuario,
        categoria = categoria,
        accion = accion,
        momento = now
    )

    nueva_actividad.save()