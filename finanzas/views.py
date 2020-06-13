from django.shortcuts import render
from presupuestos.models import Proyectos, Presupuestos, Constantes
from .models import Almacenero

# Create your views here.


def almacenero(request):

    proyectos = Proyectos.objects.order_by("nombre")

    usd_blue = Constantes.objects.get(nombre = "USD_BLUE")

    datos = 0

    if request.method == 'POST':

        #Trae el proyecto elegido

        proyecto_elegido = request.POST.items()

        #Crea los datos del pricing

        datos = []

        for i in proyecto_elegido:

            if i[0] == "proyecto":
                proyecto = Proyectos.objects.get(id = i[1])
                presupuesto = Presupuestos.objects.get(proyecto = proyecto)
                almacenero = Almacenero.objects.get(proyecto = proyecto)
                datos.append(proyecto)
                datos.append(presupuesto)
                datos.append(almacenero)

                pend_gast = almacenero.pendiente_admin + almacenero.pendiente_comision + presupuesto.saldo_mat + presupuesto.saldo_mo + presupuesto.imprevisto + presupuesto.credito + presupuesto.fdr + almacenero.pendiente_adelantos + almacenero.pendiente_iva_ventas + almacenero.pendiente_iibb_tem
                prest_cobrar = almacenero.prestamos_proyecto + almacenero.prestamos_otros
                total_costo = almacenero.cheques_emitidos + almacenero.gastos_fecha + pend_gast + almacenero.Prestamos_dados
                total_ingresos = prest_cobrar + almacenero.cuotas_cobradas + almacenero.cuotas_a_cobrar + almacenero.ingreso_ventas
                saldo_caja = almacenero.cuotas_cobradas - almacenero.gastos_fecha - almacenero.Prestamos_dados
                saldo_proyecto = total_ingresos - total_costo
                rentabilidad = (saldo_proyecto/total_ingresos)*100

                datos.append((pend_gast, prest_cobrar, total_costo, total_ingresos, rentabilidad, saldo_caja, saldo_proyecto))

        proyectos = 0

        

    datos = {"proyectos":proyectos,
    'datos':datos,
    "usd":usd_blue}

    return render(request, 'almacenero.html', {"datos":datos} )