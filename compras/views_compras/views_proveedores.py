from django.shortcuts import render, redirect
from compras.models import Proveedores

def proveedores(request):

    datos = Proveedores.objects.all()

    datos_prov={}
    mensaje=0

    if request.method == 'POST':
        datos_proveedor = request.POST
        for item in datos_proveedor:
            if item!='csrfmiddlewaretoken':
                datos_prov[item]=datos_proveedor[item]

        if 'modificar' in datos_prov:
              
            id_prov=datos_prov['modificar']
            prov=Proveedores.objects.get(pk=id_prov)
            prov.name=datos_prov['nombre']
            prov.phone=int(datos_prov['telefono'])
            prov.descrip=datos_prov['descripcion']
            prov.save()
            mensaje='Registro modificado con exito'
            return redirect('Proveedores')

        elif 'delete' in datos_prov:
            id_prov=datos_prov['delete']
            prov=Proveedores.objects.get(pk=id_prov)
            prov.delete()
            
            mensaje='Registro eliminado con exito'
            return redirect('Proveedores')


        else:
            prov=Proveedores(
                name=datos_prov['nombre'],
                phone=datos_prov['telefono'],
                 descrip=datos_prov['descripcion'],
            )
            mensaje='Registro creado con exito'

            if prov:
                prov.save()
                
    return render(request, 'proveedores/proveedores.html', {'datos':datos ,'mensaje':mensaje})
