from compras.models import Proveedores, Contratos, Comparativas
from rrhh.models import datosusuario

def comparativas_agregar_validaciones(proveedor, numero_oc):

    if len(Proveedores.objects.filter(name=proveedor)) == 0:
        
        return "El proveedor seleccionado no existe"

    elif len(numero_oc) > 10:
        
        return "El numero de OC es demasiado largo, pruebe un formato 99-9999"

    else:

        return True

def comparativas_agregar_metodo(proveedor, proyecto, referencia, valor, imagen, numerooc, autoriza, publica, 
    creador, tipo_oc, contrato, gerente):

    try:
        proveedor = Proveedores.objects.get(name=proveedor)
        if gerente != "":
            gerente_autoriza = datosusuario.objects.get(identificacion = gerente)
        else:
            gerente_autoriza = None
        nueva_comparativa = Comparativas(

            proveedor = proveedor,
            proyecto = proyecto,
            numero  = referencia,
            monto = float(valor),
            adjunto = imagen,
            o_c = numerooc,
            autoriza = autoriza,
            publica = publica,
            creador = str(creador),
            tipo_oc = tipo_oc,
            gerente_autoriza = gerente_autoriza
 
        )

        nueva_comparativa.save()

        try:
            nueva_comparativa.contrato = Contratos.objects.get(id=int(contrato))
            nueva_comparativa.save()

        except:
            pass

        return [True, nueva_comparativa.id]
    
    except UnicodeEncodeError:
        return [False, "Algún documento adjunto tiene tildes, 'ñ' o simbolos no permitidos"]

    except:
        return [False, "Surgio un error inesperado"]