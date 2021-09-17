
import datetime as dt


def saludo():
    hora_actual = dt.datetime.now()
    
    if hora_actual.hour >= 20:
        mensaje_bievenida = "¡Buenas noches {}!"

    elif hora_actual.hour >= 13:
        mensaje_bievenida = "¡Buenas tardes {}!"

    else:
        mensaje_bievenida = "¡Buen dia {}!"

    return mensaje_bievenida