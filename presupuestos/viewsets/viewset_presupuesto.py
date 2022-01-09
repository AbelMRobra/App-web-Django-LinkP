import datetime
from django.http import response
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from presupuestos.models import Bitacoras, Capitulos, Presupuestos, TareasProgramadas
from presupuestos.funciones.functions_capitulos import *
from proyectos.models import Proyectos
from presupuestos.serializers import PresupuestosSerializer, ProyectosSerializer, BitacorasSerializer, TareasSerializer
from rrhh.models import datosusuario
from presupuestos.funciones.f_presupuestos import *

class PresupuestosViewset(viewsets.ModelViewSet):
    queryset = Presupuestos.objects.all()
    serializer_class = PresupuestosSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    @action(detail=False, methods=["POST"])
    def presupuesto_create(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        presupuesto = Presupuestos.objects.create(proyecto = proyecto, valor = 0)
        proyecto.presupuesto = "SIN_MOVIMIENTO"
        proyecto.save()
        serializer_proyectos = ProyectosSerializer(proyecto, many=False)
        response = {'data' : serializer_proyectos.data}
        return Response(response, status=status.HTTP_200_OK)


    @transaction.atomic
    @action(detail=False, methods=["POST"])
    def set_proyecto_extrapolado(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        proyecto_base = Proyectos.objects.get(id = request.data['proyecto_base'])
        presupuesto = Presupuestos.objects.get(proyecto = proyecto)
        presupuesto.valor = request.data['valor']
        presupuesto.saldo = request.data['saldo']
        presupuesto.saldo_mat = request.data['saldo_mat']
        presupuesto.saldo_mo = request.data['saldo_mo']
        presupuesto.proyecto_base = proyecto_base
        presupuesto.save()
        proyecto.presupuesto = "EXTRAPOLADO"
        proyecto.save()
        response = {'messaje' : 'Success'}
        return Response(response, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=["GET"])
    def proyectos_disponibles(self, request):
        proyectos = Proyectos.objects.all()
        presupuestos = Presupuestos.objects.all()
        for presupuesto in presupuestos:
            proyectos = proyectos.exclude(id = presupuesto.proyecto.id)
        serializer_proyectos = ProyectosSerializer(proyectos, many=True)
        response = {'data' : serializer_proyectos.data}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def proyectos_bases(self, request):
        proyectos = Proyectos.objects.filter(presupuesto = "BASE")
        serializer_proyectos = ProyectosSerializer(proyectos, many=True)

        response = {'data' : serializer_proyectos.data}

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def establecer_proyecto_base(self, request):
        proyectos = Proyectos.objects.get(id = request.data['proyecto'])
        if request.data['establecer'] == "si":
            proyectos.presupuesto = "BASE"
        else:
            proyectos.presupuesto = "SIN_MOVIMIENTO"
        proyectos.save()

        response = {'message' : 'Success!'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def asignacion_proyectos(self, request, pk=None):

        try:
            presupuestos = Presupuestos.objects.get(id = pk)
            proyecto = Proyectos.objects.get(id = request.data["proyecto_base"])
            presupuestos.proyecto_base = proyecto
            presupuestos.save()

            response = {'message' : 'Success!'}
            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'message' : 'Problem'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["POST"])
    def capitulos_presupuesto(self, request):

        data = presupuesto_capitulo(request.data['proyecto'])
        response = {'data' : data}
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"])
    def capitulos_presupuesto_detalle(self, request):

        data = presupuesto_capitulo_detalle(request.data['proyecto'], request.data['capitulo'])
        response = {'data' : data, 'title': Capitulos.objects.get(id = request.data['capitulo']).nombre, 'id_capitulo': request.data['capitulo']}
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"])
    def proyectos_afectados(self, request):

        data = presupuesto_afectados(request.data['modelo'])
        response = {'data' : data}
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"])
    def modelo_editar(self, request):

        data = datos_modelo(request.data['modelo'])
        response = {'data' : data}
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"])
    def modelo_editar_guardar(self, request):
        modelo = Modelopresupuesto.objects.get(id = request.data['id'])
        modelo.orden = request.data['orden']
        modelo.comentario = request.data['comentario']
        modelo.cantidad = request.data['cantidad']
        modelo.analisis = Analisis.objects.get(codigo = request.data['analisis'].split('-')[0])
        modelo.save()
        response = {'message' : 'Success', 'capitulo': modelo.capitulo.id}
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"])
    def crear_modelo(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        analisis = Analisis.objects.get(codigo = request.data['analisis'].split('-')[0])
        capitulo = Capitulos.objects.get(id = request.data['capitulo'])
        modelo = Modelopresupuesto.objects.create(capitulo = capitulo, analisis = analisis, orden = request.data['orden'], cantidad = request.data['cantidad'], comentario = request.data['comentario'], proyecto = proyecto)
        response = {'message' : 'Success', 'capitulo': modelo.capitulo.id}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def borrar_modelo(self, request):
        modelo = Modelopresupuesto.objects.get(id = request.data['id'])
        capitulo = modelo.capitulo.id
        modelo.delete()
        response = {'message' : 'Success', 'capitulo': capitulo}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def datos_proyecto(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        presupuesto = Presupuestos.objects.get(proyecto = proyecto)

        if presupuesto.presupuestador:
            presupuestador = datosusuario.objects.get(identificacion = presupuesto.presupuestador).nombre
        else:
            presupuestador = "Sin asignar"

        if presupuesto.proyecto_base:
            proyecto_base = presupuesto.proyecto_base.nombre
        else:
            proyecto_base = "Sin asignar"
        
        response = {
            'tama' : proyecto.m2, 
            'estado': proyecto.presupuesto,
            'proyecto_base': proyecto_base,
            'presupuestador': presupuestador,
            
            }
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"])
    def cambiar_estado_proyecto(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        estado = request.data['estado']
        presupuestos_modificar_estado(proyecto, estado)
        
        response = {
            'message' : 'Success',            
            }
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def cambiar_presupuestador(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        presupuesto = Presupuestos.objects.get(proyecto = proyecto)
        presupuesto.presupuestador = request.data['presupuestador']
        presupuesto.save()
        # if request.data['notificar'] == "SI":
        #     print("Notificar")
        
        response = {
            'message' : 'Success',            
            }
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def guardar_bitacoras(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        bitacora = Bitacoras.objects.create(proyecto = proyecto, hashtag = request.data['hashtag'],
        titulo = request.data['titulo'], descrip = request.data['descrip']) 
        serializer = BitacorasSerializer(bitacora, many=False)      
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def guardar_tareas(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        tareas = TareasProgramadas.objects.create(proyecto = proyecto, tarea = request.data['tarea']) 
        serializer = TareasSerializer(tareas, many=False)      
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def consultar_bitacoras(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        bitacora = Bitacoras.objects.filter(proyecto = proyecto).order_by("-fecha")  
        serializer = BitacorasSerializer(bitacora, many=True)     
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def consultar_tareas(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        tareas = TareasProgramadas.objects.filter(Q (estado = "ESPERA", proyecto = proyecto) | Q(estado = "LISTO", proyecto = proyecto , fecha__gte = (datetime.date.today() - datetime.timedelta(days = 2))))
        serializer = TareasSerializer(tareas, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def completar_tareas(self, request):
        tareas = TareasProgramadas.objects.get(id = request.data['id'])
        if tareas.estado == "ESPERA":
            tareas.estado = "LISTO"
        else:
            tareas.estado = "ESPERA"
        tareas.save()
        response = {"message": "Sucess"}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def desactivar_proyecto(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        proyecto.presupuesto = "SIN_MOVIMIENTO"
        proyecto.save()

        presupuesto = Presupuestos.objects.get(proyecto = proyecto)
        presupuesto.reset_presupuesto()
        presupuesto.save()
        response = {"message": "Sucess"}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def activar_proyecto(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        proyecto.presupuesto = "ACTIVO"
        proyecto.save()

        response = {"message": "Sucess"}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def cambiar_proyecto_base(self, request):
        if request.data['proyecto_base'] != "":
            proyecto = Proyectos.objects.get(id = request.data['proyecto'])
            proyecto_base = Proyectos.objects.get(id = request.data['proyecto_base'])
            presupuesto = Presupuestos.objects.get(proyecto = proyecto)
            presupuesto.proyecto_base = proyecto_base
            presupuesto.save()

            response = {"proyecto": proyecto_base.nombre}
        else:
            proyecto = Proyectos.objects.get(id = request.data['proyecto'])
            presupuesto = Presupuestos.objects.get(proyecto = proyecto)
            presupuesto.proyecto_base = None
            presupuesto.save()

            response = {"proyecto": "Sin asignar"}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def recalcular_proyecto(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        presupuestos_alm=PresupuestosAlmacenados.objects.filter(proyecto = proyecto)

        if len(presupuestos_alm.filter(proyecto = proyecto, nombre = "vigente")) > 1:
            quitar_duplicados = presupuestos_revision_registros(proyecto)

        if len(presupuestos_alm.filter(proyecto = proyecto, nombre = "vigente")) == 1:
            registro_vigente = PresupuestosAlmacenados.objects.get(proyecto = proyecto, nombre = "vigente")
            registro_vigente.nombre = str("{}".format(datetime.date.today()))
            registro_vigente.save()

        recalcular_proyecto = presupuesto_generar_xls_proyecto(proyecto)
        recalcular_saldo = presupuestos_saldo_capitulo(proyecto.id)

        if proyecto.presupuesto == "ACTIVO" or proyecto.presupuesto == "BASE":
            recalcular_presupuesto = presupuesto_recalcular_presupuesto(proyecto)

        response = {"message": "Success"}
        return Response(response, status=status.HTTP_200_OK)


    @action(detail=False, methods=["POST"])
    def datos_presupuesto(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        datos_proyecto = presupuesto_datos_proyecto(proyecto)

        return Response(datos_proyecto, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def saldo_presupuesto_detallado(self, request):
        presupuesto = Presupuestos.objects.get(proyecto__id = request.data['proyecto'])
        datos_saldo = json.loads(presupuesto.balance_details)

        return Response(datos_saldo, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def saldo_detalle_asignacion(self, request):
        presupuesto = Presupuestos.objects.get(proyecto__id = request.data['proyecto'])
        datos_saldo = json.loads(presupuesto.consumption_details)

        return Response(datos_saldo, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def actualizar_valores(self, request):
        proyecto = Proyectos.objects.get(id = request.data['proyecto'])
        presupuesto = Presupuestos.objects.get(proyecto = proyecto)
        presupuesto.valor = request.data['valor']
        presupuesto.saldo = request.data['saldo']
        presupuesto.saldo_mat = request.data['saldo_mat']
        presupuesto.saldo_mo = request.data['saldo_mo']
        presupuesto.imprevisto = request.data['imprevisto']
        presupuesto.save()
        response = {"message": "Success"}
        return Response(response, status=status.HTTP_200_OK)


