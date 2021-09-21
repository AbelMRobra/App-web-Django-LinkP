
from ventas.models import FeaturesProjects, FeaturesUni, VentasRealizadas
from proyectos.models import Unidades

def atributo_agregar(proyecto, nombre, inc):

    try:

        nuevo_atributo = FeaturesProjects(
            proyecto = proyecto,
            nombre = nombre,
            inc = inc
        )

        nuevo_atributo.save()

        return [1, "Atributo creado correctamente!"]

    except:

        return [0, "Ocurrio un error inesperado"]

def atributo_editar(id_atributo, nombre, inc):

    try:

        atributo_a_editar = FeaturesProjects.objects.get(id = int(id_atributo))
        atributo_a_editar.nombre = nombre
        atributo_a_editar.inc = inc
        atributo_a_editar.save()

        return [1, "Atributo editado correctamente!"]

    except:

        return [0, "Ocurrio un error inesperado"]

def atributo_borrar(id_atributo):

    try:

        atributo_a_borrar = FeaturesProjects.objects.get(id = int(id_atributo))
        atributo_a_borrar.delete()

        return [1, "Atributo borrado correctamente!"]

    except:

        return [0, "Ocurrio un error inesperado"]

def atributo_asignar_unidad(info_template):

    nombre_unidad = info_template[0].split(sep='&')
    nombre = nombre_unidad[0]
    id_unidad = nombre_unidad[1]

    if len(FeaturesUni.objects.filter(feature__nombre = nombre, unidad = int(id_unidad))) == 0 and info_template[1] == "on":
                    
        unidad = Unidades.objects.get(id = int(id_unidad))
        atributo = FeaturesProjects.objects.get(proyecto = unidad.proyecto, nombre = nombre)
    
        nueva_asignacion_atributo_a_unidad = FeaturesUni(
            
            feature = atributo,
            unidad = unidad)
        
        nueva_asignacion_atributo_a_unidad.save()


    if len(FeaturesUni.objects.filter(feature__nombre = nombre, unidad = int(id_unidad))) > 0 and info_template[1] == "off":
        
        asignacion_existente = FeaturesUni.objects.filter(feature__nombre = nombre, unidad = int(id_unidad))

        for asignacion in asignacion_existente:

            asignacion.delete()



