from statistics import mode
from django.db.models import Count , Sum , F ,Q

from email.mime.text import MIMEText

from rrhh.models import EntregaMoneda, datosusuario
from funciones_generales.f_mandar_email import mandar_email





def calculos(datos_usuarios,monedas,monedas_entregadas,usuario,loged_user,canjemonedas):

        list_usuarios = datos_usuarios.filter(~Q(identificacion = loged_user ) & ~Q(estado = "NO ACTIVO")).order_by("identificacion")
       


        usuarios_con_regalos=monedas_entregadas.filter(Q(moneda__usuario_portador__identificacion=loged_user) & ~Q(usuario_recibe__estado="NO ACTIVO")) \
                              .values(user_recibe=F('usuario_recibe__identificacion')) \
                              .annotate(suma=Count('mensaje')) 

        info_coins_entregadas=[( i , datosusuario.objects.get(identificacion=i['user_recibe']).imagenlogo) for i in usuarios_con_regalos]



        monedas_usuario = monedas.filter(usuario_portador = usuario)
        

        monedas_disponibles =sum([1 for m in monedas_usuario if monedas_entregadas.filter(moneda=m).count()==0])
        ########################################
        # Precio por DAR
        ########################################

        if monedas.count() == monedas_disponibles:
            amor = 0
        else:
            amor = 1

        ########################################
        # Premio al puesto numero 1 y 2
        ########################################

        rey=0
        rey_l = monedas_entregadas.values_list("usuario_recibe", flat = True)

        try:
            if int(usuario.id) == int(mode(rey_l)):
                rey = 1

                
            rey_2 = monedas_entregadas.values_list("usuario_recibe", flat = True).exclude(usuario_recibe__id = int(mode(rey_l)))

            if int(usuario.id) == int(mode(rey_2)):
                rey = 2
        except:
            rey = 0
            rey_2 = 0
        
        ########################################
        # Calculo de monedas recibidas 
        ########################################
  
        monedas_recibidas = monedas_entregadas.filter(usuario_recibe = usuario).count()
        monedas_canjeadas =  sum(canjemonedas.filter(usuario = usuario).values_list("monedas", flat=True))
        monedas_disponibles_canje = monedas_recibidas - monedas_canjeadas
        recibidas_list = monedas_entregadas.filter(usuario_recibe = usuario).values_list("mensaje", flat = True)

        recibidas_list = list(set(recibidas_list))

        recibidas = []
   
        for r in recibidas_list:

            data = monedas_entregadas.filter(usuario_recibe = usuario, mensaje = r)

            usuarios_entrega = ""

            for d in data:

                if str(d.moneda.usuario_portador.identificacion) not in usuarios_entrega:
                    usuarios_entrega = usuarios_entrega + str(d.moneda.usuario_portador.identificacion) + ""

            recibidas.append((len(data), r, usuarios_entrega))

        
        return info_coins_entregadas,monedas_disponibles,recibidas,amor,monedas_disponibles_canje,list_usuarios,rey,rey_l,rey_2

def estadisticasLinkcoin():

    con_principal = EntregaMoneda.objects.all()
    datos_usuarios=datosusuario.objects.all()
    

    resultados = {}

    list_mensaje = list(con_principal.values_list("mensaje", flat=True))
    list_mensaje.sort(key = len)
    resultados['mensajeMasCorto'] = (list_mensaje[0], len(list_mensaje[0]), datos_usuarios.get(identificacion = con_principal.filter(mensaje = list_mensaje[0]).values_list("usuario_recibe__identificacion", flat=True)[0]))
    
    list_mensaje.sort(key = len, reverse=True)
    resultados["mensaje_largo"] = (list_mensaje[0], len(list_mensaje[0]), datos_usuarios.get(identificacion = con_principal.filter(mensaje = list_mensaje[0]).values_list("usuario_recibe__identificacion", flat=True)[0]))

    list_entregas = list(con_principal.values_list("usuario_recibe__identificacion", flat=True))
    resultados["usuario_mas_recibio"] = (datos_usuarios.get(identificacion = mode(list_entregas)), list_entregas.count(mode(list_entregas)))

    list_entregas_areas = list(EntregaMoneda.objects.all().values_list("usuario_recibe__area", flat=True))
    resultados["area_querida"] = (mode(list_entregas_areas), list_entregas_areas.count(mode(list_entregas_areas)))

    return resultados


def email_canje_rrhh(usuario, premio, monedas):

    rrhh = "rrhh@linkinversiones.com.ar"

    #rrhh = "abel.robra.93@gmail.com"

    cabeza = "{} realizo un canje".format(usuario)

    mensaje = MIMEText("""
                
Hola!,

{} acaba de canjear Linkcoins, el premio es {} que costó {} monedas.

Podrás visualizarlo en el panel de seguimiento. Cualquier duda, comunicate con el equipo de IT.

Saludos!

-- Link-Help 

                    """.format(usuario, premio, monedas))

    mandar_email(mensaje, rrhh ,cabeza)

def email_canje_usuario(email, usuario, premio, monedas):

    rrhh = email

    cabeza = "Realizaste un canje de Linkcoins".format(usuario)

    mensaje = MIMEText("""
                    
¡Hola!,

Acabas canjear {}  Linkcoins por el siguiente premio: {}.

El equipo de RRHH te notificará cuando el mismo esté disponible para retirarlo (esta gestión puede tomar hasta 10 días hábiles posteriores a la fecha límite de canje).

Si hubiera algún problema del sistema, comunicate con el equipo de IT para solucionarlo.

Saludos,

-- Link-Help 

                
                    """.format(monedas, premio))

    mandar_email(mensaje, rrhh ,cabeza)

