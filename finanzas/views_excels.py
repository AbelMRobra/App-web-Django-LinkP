import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from django.views.generic.base import TemplateView 
from django.http import HttpResponse
from .models import CuentaCorriente, Cuota, Pago
from proyectos.models import Proyectos
from presupuestos.models import Constantes, Registrodeconstantes
from ventas.funciones.f_pricing import unidades_calculo_m2

class ExcelCuentasCorrientes(TemplateView):

    def get(self, request, id_proyecto, *args, **kwargs):

        proyecto = Proyectos.objects.get(id = id_proyecto)

        con_cuentas_corrientes = CuentaCorriente.objects.filter(venta__proyecto = proyecto)

        # Comenzamos a crear las distintas pestañas

        wb = Workbook()

        for cuenta in con_cuentas_corrientes:

            cuotas_iterar = Cuota.objects.filter(cuenta_corriente = cuenta)

            total_cuentas = sum(np.array(cuotas_iterar.values_list("precio", flat=True)))
            
            ws = wb.create_sheet(f'{cuenta.venta.unidad.piso_unidad}-{cuenta.venta.unidad.nombre_unidad}, {cuenta.venta.comprador}'.replace("-", " "))
            ws.sheet_view.showGridLines = False

            thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

            ws.column_dimensions['A'].width = 15
            ws.column_dimensions['B'].width = 15
            ws.column_dimensions['C'].width = 20
            ws.column_dimensions['D'].width = 15
            ws.column_dimensions['E'].width = 20
            ws.column_dimensions['F'].width = 20
            ws.column_dimensions['G'].width = 20
            ws.column_dimensions['H'].width = 20
            ws.column_dimensions['I'].width = 20
            ws.column_dimensions['J'].width = 20
            ws.column_dimensions['K'].width = 20
            ws.column_dimensions['L'].width = 20
            ws.column_dimensions['M'].width = 30

            ws["A2"] = "NOMBRE COMPRADOR"
            ws["A3"] = "DIRECCIÓN"
            ws["A4"] = "TELEFONO FIJO"
            ws["A5"] = "TELEFONO CELULAR"
            ws["A6"] = "E-MAIL"

            ws["A2"].font = Font(bold = True)
            ws["A3"].font = Font(bold = True)
            ws["A4"].font = Font(bold = True)
            ws["A5"].font = Font(bold = True)
            ws["A6"].font = Font(bold = True)

            ws["F2"] = f'Proyecto: {cuenta.venta.proyecto.nombre}'
            ws["F2"].font = Font(bold = True)

            ws["C2"] = cuenta.venta.comprador

            if cuenta.direccion:
                ws["C6"] = cuenta.direccion
            else:
                ws["C3"] = "Dirección no asginada **"
                mensaje = 1

            if cuenta.telefono_fijo:
                ws["C6"] = cuenta.telefono_fijo
            else:
                ws["C4"] = "Telefono fijo no asignado **"
                mensaje = 1
            
            if cuenta.telefono_celular:
                ws["C6"] = cuenta.telefono_celular
            else:
                ws["C5"] = "Celular no asignado **"
                mensaje = 1
            
            if cuenta.venta.email:
                ws["C6"] = cuenta.venta.email
            else: 
                ws["C6"] = "Email no asignado **"
                mensaje = 1

            if mensaje:
                ws["A7"] = "** Para asginar estos datos ingrese a LinkP"

            ws.row_dimensions[7].height = 24
            # Cabeza de la operación real

            ws["B9"] = "OPERACIÓN REAL"
            ws["B9"].alignment = Alignment(horizontal = "center")
            ws["B9"].fill =  PatternFill("solid", fgColor= "CFC9D6")
            ws["B9"].font = Font(bold = True)
            ws["B9"].border = thin_border
            ws.merge_cells("B9:H9")


            ws["B10"] = "ASIGNACIÓN"
            ws["C10"] = "UNIDAD"
            ws["D10"] = "NUMERO"
            ws["E10"] = "SUPERFICIE POR UNIDAD EN M2"
            ws["G10"] = "PRECIO M2"
            ws["H10"] = "PRECIO TOTAL"

            ws["B10"].font = Font(bold = True, color="EAE3F2")
            ws["C10"].font = Font(bold = True, color="EAE3F2")
            ws["D10"].font = Font(bold = True, color="EAE3F2")
            ws["E10"].font = Font(bold = True, color="EAE3F2")
            ws["G10"].font = Font(bold = True, color="EAE3F2")
            ws["H10"].font = Font(bold = True, color="EAE3F2")

            ws["B10"].fill = PatternFill("solid", fgColor= "625E66")
            ws["C10"].fill = PatternFill("solid", fgColor= "625E66")
            ws["D10"].fill = PatternFill("solid", fgColor= "625E66")
            ws["E10"].fill = PatternFill("solid", fgColor= "625E66")
            ws["G10"].fill = PatternFill("solid", fgColor= "625E66")
            ws["H10"].fill = PatternFill("solid", fgColor= "625E66")

            ws["B10"].border = thin_border
            ws["C10"].border = thin_border
            ws["D10"].border = thin_border
            ws["E10"].border = thin_border
            ws["G10"].border = thin_border
            ws["H10"].border = thin_border

            ws.merge_cells("E10:F10")

            ws["B11"] = cuenta.venta.unidad.asig
            ws["C11"] = f'{cuenta.venta.unidad.piso_unidad}-{cuenta.venta.unidad.nombre_unidad}'
            ws["D11"] = cuenta.venta.unidad.orden
            ws["E11"] = cuenta.venta.unidad.tipologia
            ws["F11"] = unidades_calculo_m2(cuenta.venta.unidad.id)

            ws["D11"].alignment = Alignment(horizontal = "center")
            ws["E11"].alignment = Alignment(horizontal = "center")
            ws["F11"].alignment = Alignment(horizontal = "center")
            
            ws["B11"].border = thin_border
            ws["C11"].border = thin_border
            ws["D11"].border = thin_border
            ws["E11"].border = thin_border
            ws["F11"].border = thin_border
            ws["G11"].border = thin_border
            ws["H11"].border = thin_border


            # Cabeza de la operación boleto

            ws["B13"] = "OPERACIÓN REAL"
            ws["B13"].alignment = Alignment(horizontal = "center")
            ws["B13"].fill =  PatternFill("solid", fgColor= "CFC9D6")
            ws["B13"].font = Font(bold = True)
            ws["B13"].border = thin_border
            ws.merge_cells("B13:H13")


            ws["B14"] = "ASIGNACIÓN"
            ws["C14"] = "UNIDAD"
            ws["D14"] = "NUMERO"
            ws["E14"] = "SUPERFICIE POR UNIDAD EN M2"
            ws["G14"] = "PRECIO M2"
            ws["H14"] = "PRECIO TOTAL"

            ws["B14"].font = Font(bold = True, color="EAE3F2")
            ws["C14"].font = Font(bold = True, color="EAE3F2")
            ws["D14"].font = Font(bold = True, color="EAE3F2")
            ws["E14"].font = Font(bold = True, color="EAE3F2")
            ws["G14"].font = Font(bold = True, color="EAE3F2")
            ws["H14"].font = Font(bold = True, color="EAE3F2")

            ws["B14"].fill = PatternFill("solid", fgColor= "625E66")
            ws["C14"].fill = PatternFill("solid", fgColor= "625E66")
            ws["D14"].fill = PatternFill("solid", fgColor= "625E66")
            ws["E14"].fill = PatternFill("solid", fgColor= "625E66")
            ws["G14"].fill = PatternFill("solid", fgColor= "625E66")
            ws["H14"].fill = PatternFill("solid", fgColor= "625E66")

            ws["B14"].border = thin_border
            ws["C14"].border = thin_border
            ws["D14"].border = thin_border
            ws["E14"].border = thin_border
            ws["F14"].border = thin_border
            ws["G14"].border = thin_border
            ws["H14"].border = thin_border

            ws.merge_cells("E14:F14")


            ws["B15"] = cuenta.venta.unidad.asig
            ws["C15"] = f'{cuenta.venta.unidad.piso_unidad}-{cuenta.venta.unidad.nombre_unidad}'
            ws["D15"] = cuenta.venta.unidad.orden
            ws["E15"] = cuenta.venta.unidad.tipologia
            ws["F15"] = unidades_calculo_m2(cuenta.venta.unidad.id)

            ws["D15"].alignment = Alignment(horizontal = "center")
            ws["E15"].alignment = Alignment(horizontal = "center")
            ws["F15"].alignment = Alignment(horizontal = "center")

            ws["B15"].border = thin_border
            ws["C15"].border = thin_border
            ws["D15"].border = thin_border
            ws["E15"].border = thin_border
            ws["F15"].border = thin_border
            ws["G15"].border = thin_border
            ws["H15"].border = thin_border

            ws["B17"] = "* Toda la información detalla es resultado de los datos subidos en LinkP"
            ws.row_dimensions[17].height = 24

            ws["B18"] = "INCREMENTO SOBRE SALDO/CUENTAS"
            ws["B18"].alignment = Alignment(horizontal = "center")
            ws["B18"].fill =  PatternFill("solid", fgColor= "CFC9D6")
            ws["B18"].font = Font(bold = True)
            ws["B18"].border = thin_border
            ws.merge_cells("B18:M18")

            ws.row_dimensions[20].height = 36

            ws["B19"] = "AÑO"
            ws["B19"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["B19"].font = Font(bold = True, color="EAE3F2")
            ws["B19"].fill = PatternFill("solid", fgColor= "625E66")
            ws["B19"].border = thin_border
            ws.merge_cells("B19:B20")

            ws["C19"] = "MES PAGO"
            ws["C19"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["C19"].font = Font(bold = True, color="EAE3F2")
            ws["C19"].fill = PatternFill("solid", fgColor= "625E66")
            ws["C19"].border = thin_border
            ws.merge_cells("C19:C20")

            ws["D19"] = "CUOTAS"
            ws["D19"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["D19"].font = Font(bold = True, color="EAE3F2")
            ws["D19"].fill = PatternFill("solid", fgColor= "625E66")
            ws["D19"].border = thin_border

            ws["D20"] = "PARCIALES"
            ws["D20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["D20"].font = Font(bold = True, color="EAE3F2")
            ws["D20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["D20"].border = thin_border

            ws["E19"] = f"{cuotas_iterar.count()}"
            ws["E19"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["E19"].font = Font(bold = True, color="EAE3F2")
            ws["E19"].fill = PatternFill("solid", fgColor= "625E66")
            ws["E19"].border = thin_border

            ws["E20"] = f'{total_cuentas}'
            ws["E20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["E20"].font = Font(bold = True, color="EAE3F2")
            ws["E20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["E20"].border = thin_border

            ws["F19"] = "AUMENTO SALDO % MENSUAL"
            ws["F19"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["F19"].font = Font(bold = True, color="EAE3F2")
            ws["F19"].fill = PatternFill("solid", fgColor= "625E66")
            ws["F19"].border = thin_border
            ws.merge_cells("F19:K19")

            ws["F20"] = """M3 de hormigón
             de deuda"""
            ws["F20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["F20"].font = Font(bold = True, color="EAE3F2")
            ws["F20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["F20"].border = thin_border

            ws["G20"] = """Valor del M3 de
            hormigon"""
            ws["G20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["G20"].font = Font(bold = True, color="EAE3F2")
            ws["G20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["G20"].border = thin_border

            ws["H20"] = """Aumento
            porcentual"""
            ws["H20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["H20"].font = Font(bold = True, color="EAE3F2")
            ws["H20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["H20"].border = thin_border

            ws["I20"] = """Aumento
            numero"""
            ws["I20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["I20"].font = Font(bold = True, color="EAE3F2")
            ws["I20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["I20"].border = thin_border

            ws["J20"] = "Cuota"
            ws["J20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["J20"].font = Font(bold = True, color="EAE3F2")
            ws["J20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["J20"].border = thin_border

            ws["K20"] = "Saldo"
            ws["K20"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["K20"].font = Font(bold = True, color="EAE3F2")
            ws["K20"].fill = PatternFill("solid", fgColor= "625E66")
            ws["K20"].border = thin_border

            ws["L19"] = """FECHA DE
            COBRO"""
            ws["L19"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["L19"].font = Font(bold = True, color="EAE3F2")
            ws["L19"].fill = PatternFill("solid", fgColor= "625E66")
            ws["L19"].border = thin_border
            ws.merge_cells("L19:L20")

            ws["M19"] = """FORMA DE 
            PAGO"""
            ws["M19"].alignment = Alignment(horizontal = "center", vertical="center")
            ws["M19"].font = Font(bold = True, color="EAE3F2")
            ws["M19"].fill = PatternFill("solid", fgColor= "625E66")
            ws["M19"].border = thin_border
            ws.merge_cells("M19:M20")

            valor_inicial = 21
            year_pivote = 0
            celda_pivote = 0
            celda_pivote_2 = 0
            parciales = 1
            valor_anterior = 0
            total_cuentas_acumulado = total_cuentas

            month_names = {
                "1":"Enero",
                "2":"Febrero",
                "3":"Marzo",
                "4":"Abril",
                "5":"Mayo",
                "6":"Junio",
                "7":"Julio",
                "8":"Agosto",
                "9":"Septiembre",
                "10":"Octubre",
                "11":"Noviembre",
                "12":"Diciembre",
            }

            for cuota in cuotas_iterar:
                con_pago = Pago.objects.filter(cuota = cuota)
                pago = sum(np.array(con_pago.values_list("pago", flat=True)))
                total_cuentas_acumulado = total_cuentas_acumulado - pago

                if year_pivote == 0:
                    year_pivote = cuota.fecha.year
                    celda_pivote = "B"+str(valor_inicial)

                if cuota.fecha.year != year_pivote:

                    ws.merge_cells(str(celda_pivote)+":"+str(celda_pivote_2))
                    year_pivote = cuota.fecha.year
                    celda_pivote = "B"+str(valor_inicial)

                ws["B"+str(valor_inicial)] = cuota.fecha.year
                ws["B"+str(valor_inicial)].alignment = Alignment(horizontal = "center", vertical="center")
                ws["B"+str(valor_inicial)].font = Font(bold = True, color="EAE3F2")
                ws["B"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "625E66")
                ws["B"+str(valor_inicial)].border = thin_border
                
                ws["C"+str(valor_inicial)] = month_names[str(cuota.fecha.month)]
                ws["D"+str(valor_inicial)] = parciales
                ws["E"+str(valor_inicial)] = total_cuentas_acumulado
                ws["F"+str(valor_inicial)] = pago

                if pago != 0:
                    pago_pesos = sum(np.array(con_pago.values_list("pago_pesos", flat=True)))
                    valor_hormigon = pago_pesos/pago
                    
                else:
                    try:
                        valor_hormigon = Registrodeconstantes.objects.get(fecha__month = cuota.fecha.mont, fecha__year = cuota.fecha.year, contante__id = 7).valor
                
                    except:
                        valor_hormigon = Constantes.objects.get(id = 7).valor
                
                ws["G"+str(valor_inicial)] = valor_hormigon
                ws["G"+str(valor_inicial)].number_format = '"$"#,##0.00_-'

                if valor_anterior == 0:
                    ws["H"+str(valor_inicial)] = "-"

                else:
                    ws["H"+str(valor_inicial)] = (valor_hormigon/valor_anterior-1)*100
                    ws["H"+str(valor_inicial)].number_format = '#,##0.00_-"%"'
                
                ws["I"+str(valor_inicial)] = valor_hormigon - valor_anterior
                ws["I"+str(valor_inicial)].number_format = '"$"#,##0.00_-'

                ws["J"+str(valor_inicial)] = valor_hormigon*pago
                ws["J"+str(valor_inicial)].number_format = '"$"#,##0.00_-'

                ws["K"+str(valor_inicial)] = (total_cuentas_acumulado - pago)*valor_hormigon
                ws["K"+str(valor_inicial)].number_format = '"$"#,##0.00_-'

                fechas_pago = ""
                metodo_pago = ""

                for consulta in con_pago:
                    fechas_pago += "/"+str(consulta.fecha)
                    metodo_pago += "/"+str(consulta.metodo)

                ws["L"+str(valor_inicial)] = fechas_pago
                ws["M"+str(valor_inicial)] = metodo_pago
                
                valor_anterior = valor_hormigon

                ws["C"+str(valor_inicial)].border = thin_border
                ws["D"+str(valor_inicial)].border = thin_border
                ws["E"+str(valor_inicial)].border = thin_border
                ws["F"+str(valor_inicial)].border = thin_border
                ws["G"+str(valor_inicial)].border = thin_border
                ws["H"+str(valor_inicial)].border = thin_border
                ws["I"+str(valor_inicial)].border = thin_border
                ws["J"+str(valor_inicial)].border = thin_border
                ws["K"+str(valor_inicial)].border = thin_border
                ws["L"+str(valor_inicial)].border = thin_border
                ws["M"+str(valor_inicial)].border = thin_border

                if pago:

                    ws["C"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["D"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["E"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["F"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["G"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["H"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["I"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["J"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["K"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["L"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")
                    ws["M"+str(valor_inicial)].fill = PatternFill("solid", fgColor= "F5F584")

                celda_pivote_2 = "B"+str(valor_inicial)
                valor_inicial += 1
                parciales += 1

            ws.merge_cells(str(celda_pivote)+":"+str(celda_pivote_2))                

        #Establecer el nombre del archivo
        nombre_archivo = "CuentasCorrientes{}.xls".format(proyecto.nombre)
        
        #Definir tipo de respuesta que se va a dar
        response = HttpResponse(content_type = "application/ms-excel")
        contenido = "attachment; filename = {0}".format(nombre_archivo).replace(',', '_')
        response["Content-Disposition"] = contenido
        wb.save(response)
        return response
