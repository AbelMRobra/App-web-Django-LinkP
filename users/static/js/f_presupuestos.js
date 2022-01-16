
window.onload = service_datos_presupuesto()

document.getElementById("modal_asignacion").addEventListener("click", function(event){
    event.preventDefault()
    });

// Constantes iniciales
let bitacoras = false;
let tareas = false;
let presupuesto_detallado = false;
let detalle_asignacion = false;

function sweet_alert(mensaje, estado) {

    const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 5000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
    })

    Toast.fire({
        icon: estado,
        title: mensaje
    })

};
async function service_datos_presupuesto(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/presupuestos/api_presupuesto/`

    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },
    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_consulta(response, status)
}
function validar_respuesta_consulta(response, status){

    if (status >= 200 && status <300){

        validar_presupuestos(response);

    } else {
    sweet_alert("Problemas de conexión", "warning")
    }

}
function validar_presupuestos(response, status){
    
    for (let i=0; i <= response.length -1; i++){
      
        if (response[i].proyecto.presupuesto == 'EXTRAPOLADO' && response[i].proyecto_base == null){

            sweet_alert("Se necesita definir", "info");
            var proyecto_problemas = document.getElementById("proyecto_problemas")
            proyecto_problemas.value = response[i].id
            service_datos_presupuesto_base()

            console.log("Aqui se abre el modal")
            $( document ).ready(function() {
                var proyecto_modal = document.getElementById("proyecto")
                proyecto_modal.innerHTML = response[i].proyecto.nombre
                $('#modalProyecto').modal('toggle')
            });
            break
        } else {
            console.log("NO ACTIVAR MODAL")
        }
    }
}

async function service_datos_presupuesto_base(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/presupuestos/api_presupuesto/proyectos_bases/`

    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },


    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_base(response, status)
}

function validar_respuesta_base(response, status){

    if (status >= 200 && status <300){

        if (response.data.length > 0) {
            var select = document.getElementById("select_modal")
            for (let i=0; i <= response.data.length -1; i++) {
                var option = document.createElement("option")
                option.value = response.data[i].id
                option.innerHTML = response.data[i].nombre

                select.appendChild(option)
            }
        }



    } else {
    
        sweet_alert("Problemas de consulta", "warning")
    }

}

async function service_asignar_proyecto(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/presupuestos/api_presupuesto/${document.getElementById("proyecto_problemas").value}/asignacion_proyectos/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto_base":document.getElementById("select_modal").value,
        })


    })


    var status = await respuesta.status

    return validar_respuesta_asignacion(status)
}

function validar_respuesta_asignacion(status){

    if (status >= 200 && status <300){

        console.log("Print de cosas")
        var alert = sweet_alert("Asignado", "success");
        $('#modalProyecto').modal('toggle')
        
        return setTimeout(async function(){ await service_datos_presupuesto()} , 1500)



    } else {
    
        sweet_alert("Problemas de consulta", "warning")
    }

}

async function service_establecer_base(id){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    const url = `${host}/presupuestos/api_presupuesto/establecer_proyecto_base/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "proyecto": id,
            "establecer": "si",
        })
    })
    var status = await respuesta.status

    return validar_asignacion_base(status, id)

}

function validar_asignacion_base(status, id){

    if (status >= 200 && status <300){
        sweet_alert("Asignado", "success");
        modificar_template_asignacion_base(id);
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}

function modificar_template_asignacion_base(id){

    var buttom_flag_off = document.getElementById('proyecto_base_off');
    buttom_flag_off.style = 'display: none;'
    
    var buttom_flag_on = document.getElementById('proyecto_base_on');
    buttom_flag_on.style = ''

    var contenedor_extrapolados = document.getElementById('contenedor_extrapolados');
    contenedor_extrapolados.style = 'text-align: end;'
    var contenedor_refresh = document.getElementById('contenedor_refresh');
    contenedor_refresh.style = 'text-align: end;'
    var contenedor_save = document.getElementById('contenedor_save');
    contenedor_save.style = 'text-align: start;'
}

async function service_no_establecer_base(id){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    const url = `${host}/presupuestos/api_presupuesto/establecer_proyecto_base/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "proyecto": id,
            "establecer": "no",
        })
    })
    var status = await respuesta.status

    return validar_asignacion_no_base(status, id)

}

function validar_asignacion_no_base(status, id){

    if (status >= 200 && status <300){
        sweet_alert("Sin asignar", "success");
        modificar_template_asignacion_no_base(id);
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}

function modificar_template_asignacion_no_base(id){

    var buttom_flag_off = document.getElementById('proyecto_base_off');
    buttom_flag_off.style = ''
    
    var buttom_flag_on = document.getElementById('proyecto_base_on');
    buttom_flag_on.style = 'display: none;'

    var contenedor_extrapolados = document.getElementById('contenedor_extrapolados');
    contenedor_extrapolados.style = 'display: none;'
    var contenedor_refresh = document.getElementById('contenedor_refresh');
    contenedor_refresh.style = 'display: none;'
    var contenedor_save = document.getElementById('contenedor_save');
    contenedor_save.style = 'display: none;'
}

function service_configurar_proyecto(){

    service_datos_presupuesto_base();
    $('#modalProyecto').modal('toggle');

}

function service_configurar_proyecto_extrapolado(){

    $('#modalProyecto').modal('toggle');
    $('#modalProyectoExtrapolado').modal('toggle');

}

function service_crear_presupuesto_modal(){

    id_seleccionado = document.getElementById('select_project');

    if (id_seleccionado.value == "NEW"){
        service_datos_presupuesto_disponible();
        $('#modalCrearPresupuesto').modal('toggle');
    } 
}

async function service_datos_presupuesto_disponible(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/presupuestos/api_presupuesto/proyectos_disponibles/`

    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_disponible(response, status)
}

function validar_respuesta_disponible(response, status){

    if (status >= 200 && status <300){

        if (response.data.length > 0) {
            var select = document.getElementById("select_modal_create")
            for (let i=0; i <= response.data.length -1; i++) {
                var option = document.createElement("option")
                option.id = `create-${response.data[i].id}`
                option.value = response.data[i].id
                option.innerHTML = response.data[i].nombre

                select.appendChild(option)
            }
        }

    } else {
        sweet_alert("Problemas de consulta", "warning")
    }

}
// CREACIÓN DE PRESUPUESTOS
async function service_crear_presupuesto(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;
    var id = document.getElementById("select_modal_create").value;
    
    const url = `${host}/presupuestos/api_presupuesto/presupuesto_create/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": id,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_creacion(response, status)
}

function validar_respuesta_creacion(response, status){

    if (status >= 200 && status <300){
        $('#modalCrearPresupuesto').modal('toggle');
        sweet_alert("Presupuesto creado", "success");
        modificar_template_creacion(response);
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}

function modificar_template_creacion(response){

    var select = document.getElementById("select_project");
    var option = document.createElement("option");
    option.value = response.data.id;
    option.innerHTML = response.data.nombre;
    select.appendChild(option);
    var option_delete = document.getElementById(`create-${response.data.id}`);
    option_delete.remove();


}
// SETEO DE PROYECTO EXTRAPOLADO
async function service_set_presupuesto_extrapolado(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/set_proyecto_extrapolado/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "proyecto_base": document.getElementById("select_modal").value,
            "valor": document.getElementById("valor").value,
            "saldo": document.getElementById("saldo").value,
            "saldo_mat": document.getElementById("saldo_mat").value,
            "saldo_mo": document.getElementById("saldo_mo").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_set_extrapolado(response, status)
}
async function service_activar_proyecto(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/activar_proyecto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_proyecto_activado(response, status)
}
function validar_proyecto_activado(response, status){

    if (status >= 200 && status <300){
        sweet_alert("Presupuesto seteado", "success");
        modificar_template_seteo(response);
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_respuesta_set_extrapolado(response, status){

    if (status >= 200 && status <300){
        $('#modalProyectoExtrapolado').modal('toggle');
        sweet_alert("Presupuesto seteado", "success");
        modificar_template_seteo(response);
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function modificar_template_seteo(response){

    var activo_off = document.getElementById("activo_off");
    activo_off.style = "display: none";
    var activo_on = document.getElementById("activo_on");
    activo_on.style = "";
}

// PRESUPUESTOS - CONSOLA

function activar_consola(){
    var consola = document.getElementById("consola").value
    if (consola == "TOOLS") {
        ocultar_home();
        ocultar_consola_gestor();
        ocultar_consola_datos();
        ocultar_consola_reporte();
        mostrar_consola_tools();
    } else if (consola == "GESTOR"){
        ocultar_home();
        ocultar_consola_tools();
        ocultar_consola_datos();
        ocultar_consola_reporte();
        mostrar_consola_gestor();
    } else if (consola == "DATOS"){
        ocultar_home();
        ocultar_consola_tools();
        ocultar_consola_gestor();
        ocultar_consola_reporte();
        mostrar_consola_datos();
    } else if (consola == "REPORTE"){
        ocultar_home();
        ocultar_consola_tools();
        ocultar_consola_gestor();
        ocultar_consola_datos();
        mostrar_consola_reporte();
    }
}

// PRESUPUESTOS - HERRAMIENTAS

function abrir_consola_edicion_modelo(id){

    limpiar_seleccion_analisis();
    realizar_sleccion_analisis(id);
    mostrar_ventana_edicion();
    proyectos_afectados(id);
    modelo_editar(id);
    
}
// PRESUPUESTOS - SERVICES DE CONSULTAS
async function service_valor_capitulos(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/capitulos_presupuesto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_valores_capitulo(response, status)
}
async function capitulos_presupuesto_detalle(id){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/capitulos_presupuesto_detalle/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "capitulo": id
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_armado_tabla(response, status)
}
async function modelo_editar(id){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/modelo_editar/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "modelo": id
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_modelo_editar(response, status)
}
async function proyectos_afectados(id){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/proyectos_afectados/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "modelo": id
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_proyectos_afectados(response, status)
}
async function service_datos_proyecto(id){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/datos_proyecto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_datos_proyecto(response, status)
}

// PRESUPUESTOS - MODIFICACIONES DE TEMPLATE POR SERVICES DE CONSULTA
function validar_respuesta_datos_proyecto(response, status){

    if (status >= 200 && status <300){
        armar_panel_resumen(response);
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_respuesta_valores_capitulo(response, status){

    if (status >= 200 && status <300){
        if (document.getElementById("list_capitulos")){
            list = document.getElementById("list_capitulos")
            list.remove()
        }

        if (response.data.length > 0) {
            var contenedor = document.getElementById("contenedor_capitulos")
            var lista_capitulos = document.createElement("ul")
            lista_capitulos.id = "list_capitulos"
            contenedor.appendChild(lista_capitulos)
            for (let i=0; i <= response.data.length -1; i++) {
                var lista = document.createElement("li")
                lista.id = `cap-${response.data[i].id}`
                lista.innerHTML = `<b class="box" onclick="capitulos_presupuesto_detalle(${response.data[i].id})">${response.data[i].nombre}</b>`;
                lista_capitulos.appendChild(lista)
            }
        }
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_modelo_editar(response, status){
    if (status >= 200 && status <300){

        var id_editar = document.getElementById("id_modelo")
        id_editar.value = response.data.id

        var order_editar = document.getElementById("order")
        order_editar.value = response.data.orden

        var analisis_editar = document.getElementById("analisis")
        analisis_editar.value = response.data.analisis

        var comentario_editar = document.getElementById("comentario")
        comentario_editar.value = response.data.comentario

        var cantidad_editar = document.getElementById("cantidad")
        cantidad_editar.value = response.data.cantidad


    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_armado_tabla(response, status){
    if (status >= 200 && status <300){

        modificar_capitulo_activo(response.title, response.id_capitulo);
        mostrar_boton_agregar();


        if (document.getElementById("tabla_detalle")){
            list = document.getElementById("tabla_detalle");
            list.remove();
        }


        var contenedor = document.getElementById("contenedor_detalle_capitulos");
        var tabla = document.createElement("table");
        tabla.className = 'table table-bordered';
        tabla.id = 'tabla_detalle';
        var tabla_cuerpo = document.createElement("tbody");
        tabla.appendChild(tabla_cuerpo);

        var fila = document.createElement("tr");
        fila.id = 'cabeza_tabla';
        fila.className = "font-bold";
        var celda_orden = document.createElement("td");
        celda_orden.innerHTML = 'Nº';
        var celda_nombre = document.createElement("td");
        celda_nombre.innerHTML = 'Analisis';
        var celda_precio_unitario = document.createElement("td");
        celda_precio_unitario.innerHTML = '$ unit';
        var celda_cantidad = document.createElement("td");
        celda_cantidad.innerHTML = 'Cantidad';
        var celda_precio_total = document.createElement("td");
        celda_precio_total.innerHTML = 'Total';

        fila.appendChild(celda_orden);
        fila.appendChild(celda_nombre);
        fila.appendChild(celda_precio_unitario);
        fila.appendChild(celda_cantidad);
        fila.appendChild(celda_precio_total);

        tabla_cuerpo.appendChild(fila);

        for (let i=0; i <= response.data.length -1; i++) {
            var fila = document.createElement("tr");
            fila.id = response.data[i].id;
            fila.className = "box";
            fila.onclick = function() {
                abrir_consola_edicion_modelo(response.data[i].id);
            }
            fila.style = "font-size: 13px"

            var celda_orden = document.createElement("td")
            celda_orden.innerHTML = response.data[i].orden
            var celda_nombre = document.createElement("td")
            celda_nombre.innerHTML = `${response.data[i].nombre} (${response.data[i].unidad})<div><small>${response.data[i].comentario}</small></div> `
            var celda_precio_unitario = document.createElement("td")
            celda_precio_unitario.innerHTML = Intl.NumberFormat().format(response.data[i].valor)
            var celda_cantidad = document.createElement("td")
            celda_cantidad.innerHTML = Intl.NumberFormat().format(response.data[i].cantidad)
            var celda_precio_total = document.createElement("td")
            celda_precio_total.innerHTML = Intl.NumberFormat().format(response.data[i].valor_analisis)

            fila.appendChild(celda_orden)
            fila.appendChild(celda_nombre)
            fila.appendChild(celda_precio_unitario)
            fila.appendChild(celda_cantidad)
            fila.appendChild(celda_precio_total)

            tabla_cuerpo.appendChild(fila)

        }
        contenedor.appendChild(tabla)

        

    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_proyectos_afectados(response, status){
    if (status >= 200 && status <300){
        if (document.getElementById("list_proyectos_afectados")){
            list = document.getElementById("list_proyectos_afectados")
            list.remove()
        }

        if (response.data.length > 0) {
            var contenedor = document.getElementById("contenedor_proyectos_afectados")
            var lista_proyectos_afectados = document.createElement("div")
            lista_proyectos_afectados.id = "list_proyectos_afectados"
            lista_proyectos_afectados.className = "mt-4"
            contenedor.appendChild(lista_proyectos_afectados)

            for (let i=0; i <= response.data.length -1; i++) {
                var proyecto = document.createElement("p")
                proyecto.innerHTML = response.data[i].nombre;
                lista_proyectos_afectados.appendChild(proyecto)
            }
        }
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
// PRESUPUESTOS - SERVICE DATOS DE PROYECTO
async function service_consultar_datos_presupuesto(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/datos_presupuesto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })
    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_datos_proyecto(response, status)
}
async function service_actualizar_valores_proyecto(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/actualizar_valores/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "valor": document.getElementById("CD_valor").value,
            "saldo": document.getElementById("CD_saldo").value,
            "saldo_mo": document.getElementById("CD_saldo_mo").value,
            "saldo_mat": document.getElementById("CD_saldo_mat").value,
            "imprevisto": document.getElementById("CD_imprevisto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_actualizacion_datos(response, status)
}
async function service_recalcular_presupuesto(){

    var loader = document.getElementById("loader_presupuestos")
    loader.style = ' ';

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/recalcular_proyecto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })
    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_recalcular_presupuesto(response, status)
}
async function service_saldo_detallado_presupuesto(){

    var loader = document.getElementById("loader_presupuestos")
    loader.style = ' ';

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/saldo_presupuesto_detallado/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })
    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_saldo_detalle(response, status)
}
async function service_consultar_detalle_asignacion(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/saldo_detalle_asignacion/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })
    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_detalle_asignacion(response, status)
}
async function service_saldo_detallado_consumo_articulo(){

    var loader = document.getElementById("loader_presupuestos")
    loader.style = ' ';

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/saldo_presupuesto_detallado/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })
    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_saldo_detalle(response, status)
}
function validar_respuesta_actualizacion_datos(response, status){
    if (status >= 200 && status <300){
        service_consultar_datos_presupuesto();
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_detalle_asignacion(response, status){
    if (status >= 200 && status <300){
        detalle_asignacion = response;

    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_saldo_detalle(response, status){
    if (status >= 200 && status <300){
        presupuesto_detallado = response;
        armar_detalle_saldo_presupuesto();
        var loader = document.getElementById("loader_presupuestos");
        loader.style = 'display: none;';  

    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_recalcular_presupuesto(response, status){
    if (status >= 200 && status <300){
        service_consultar_datos_presupuesto();
        service_saldo_detallado_presupuesto();
        service_consultar_detalle_asignacion();
        var loader = document.getElementById("loader_presupuestos")
        loader.style = 'display: none;';  
        sweet_alert("Proyecto guardado", "success");
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_datos_proyecto(response, status){
    if (status >= 200 && status <300){
        armar_encabezado(response);  
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function armar_detalle_saldo_presupuesto(){

    var contenedor = document.getElementById("contenedor_CD_detalle")
    if (document.getElementById("detalle_saldo_lista")){
        var lista = document.getElementById("detalle_saldo_lista")
        lista.remove()
    }
    var lista = document.createElement("ul")
    lista.id = "detalle_saldo_lista"
    lista.className = "scrollbox mt-2"
    lista.style = "height: 75vh; overflow-y: auto;"
    contenedor.appendChild(lista)

    for (let i=0; i <= presupuesto_detallado.length -1; i++) {
        var elemento = document.createElement("li")
        var nombre_capitulo = Object.keys(presupuesto_detallado[i])
        elemento.className = "mt-2"

        elemento.innerHTML = `<h6 class="box text-primary" onclick="mostrar_analisis_capitulo(${presupuesto_detallado[i][nombre_capitulo].id})">Capitulo N: ${presupuesto_detallado[i][nombre_capitulo].id}: ${nombre_capitulo}
        <div class = "text-dark"><small>inc: <b>${Intl.NumberFormat().format(presupuesto_detallado[i][nombre_capitulo].inc)}%</b>
        Valor: <b>$${Intl.NumberFormat().format(presupuesto_detallado[i][nombre_capitulo].valor_capitulo)}</b> - 
        Saldo <b>$${Intl.NumberFormat().format(presupuesto_detallado[i][nombre_capitulo].saldo)}</b></small></div>
        </h6> 
        `

        lista.appendChild(elemento)
    }
 
}
function armar_encabezado(response){
    var valor = document.getElementById("valor_presupuesto_CD");
    valor.innerHTML = `$ ${Intl.NumberFormat().format(response.valor_reposicion)}`;
    var input = document.getElementById("CD_valor");
    input.value = response.valor_reposicion;
    var saldo = document.getElementById("saldo_total_CD")
    saldo.innerHTML = `$ ${Intl.NumberFormat().format(response.saldo_total)}`
    var input = document.getElementById("CD_saldo");
    input.value = response.saldo_total;
    var saldo_mo = document.getElementById("saldo_material_CD")
    saldo_mo.innerHTML = `$ ${Intl.NumberFormat().format(response.saldo_material)}`
    var input = document.getElementById("CD_saldo_mat");
    input.value = response.saldo_material;
    var saldo_mat = document.getElementById("saldo_mo_CD")
    saldo_mat.innerHTML = `$ ${Intl.NumberFormat().format(response.saldo_mo)}`
    var input = document.getElementById("CD_saldo_mo");
    input.value = response.saldo_mo;
    var imprevisto = document.getElementById("imprevisto_CD")
    imprevisto.innerHTML = `$ ${Intl.NumberFormat().format(response.imprevisto)}`
    var input = document.getElementById("CD_imprevisto");
    input.value = response.imprevisto;
}
function mostrar_input_CD_valor(){
    var field = document.getElementById("valor_presupuesto_CD")
    field.onclick = function(){
        ocultar_input_CD_valor();
    }
    var input = document.getElementById("CD_valor")
    input.style = ' '

}
function ocultar_input_CD_valor(){
    var input = document.getElementById("CD_valor")
    input.style = 'display: none;'

    var field = document.getElementById("valor_presupuesto_CD")
    field.onclick = function(){
        mostrar_input_CD_valor();
    }
}
function mostrar_input_CD_saldo(){
    var field = document.getElementById("saldo_total_CD")
    field.onclick = function(){
        ocultar_input_CD_saldo();
    }
    var input = document.getElementById("CD_saldo")
    input.style = ' '

}
function ocultar_input_CD_saldo(){
    var input = document.getElementById("CD_saldo")
    input.style = 'display: none;'

    var field = document.getElementById("saldo_total_CD")
    field.onclick = function(){
        mostrar_input_CD_saldo();
    }
}
function mostrar_input_CD_saldo_mat(){
    var field = document.getElementById("saldo_material_CD")
    field.onclick = function(){
        ocultar_input_CD_saldo_mat();
    }
    var input = document.getElementById("CD_saldo_mat")
    input.style = ' '

}
function ocultar_input_CD_saldo_mat(){
    var input = document.getElementById("CD_saldo_mat")
    input.style = 'display: none;'

    var field = document.getElementById("saldo_material_CD")
    field.onclick = function(){
        mostrar_input_CD_saldo_mat();
    }
}
function mostrar_input_CD_saldo_mo(){
    var field = document.getElementById("saldo_mo_CD")
    field.onclick = function(){
        ocultar_input_CD_saldo_mo();
    }
    var input = document.getElementById("CD_saldo_mo")
    input.style = ' '

}
function ocultar_input_CD_saldo_mo(){
    var input = document.getElementById("CD_saldo_mo")
    input.style = 'display: none;'

    var field = document.getElementById("saldo_mo_CD")
    field.onclick = function(){
        mostrar_input_CD_saldo_mo();
    }
}
function mostrar_input_CD_imprevisto(){
    var field = document.getElementById("imprevisto_CD")
    field.onclick = function(){
        ocultar_input_CD_imprevisto();
    }
    var input = document.getElementById("CD_imprevisto")
    input.style = ' '

}
function ocultar_input_CD_imprevisto(){
    var input = document.getElementById("CD_imprevisto")
    input.style = 'display: none;'

    var field = document.getElementById("imprevisto_CD")
    field.onclick = function(){
        mostrar_input_CD_imprevisto();
    }
}
function mostrar_datos_generales(){
    var display_general = document.getElementById("datos_generales")
    display_general.style = " "
    var display_analisis = document.getElementById("datos_analisis")
    display_analisis.style = "display: none;"

}
function mostrar_datos_anteriores(){
    var display_analisis = document.getElementById("datos_analisis")
    display_analisis.style = " "
    var display_consumo = document.getElementById("detalle_consumo")
    display_consumo.style = "display: none;"

}
function mostrar_detalle_articulo(codigo){

    var display_consumo = document.getElementById("detalle_consumo")
    display_consumo.style = " "
    var display_analisis = document.getElementById("datos_analisis")
    display_analisis.style = "display: none;"
    var contenedor_general = document.getElementById("logs_consumo")

    if (document.getElementById("contenedor_log")){
        contenedor = document.getElementById("contenedor_log");
        contenedor.remove();

    }

    var contenedor = document.createElement("div");
    contenedor.id = "contenedor_log"
    contenedor_general.append(contenedor)

    for (let i=0; i <= detalle_asignacion.length -1; i++) {
        if (Object.keys(detalle_asignacion[i]) == codigo) {

            var compras = detalle_asignacion[i][codigo]['compras']
            var detalle = detalle_asignacion[i][codigo]['detalle']

            for (let c=0; c <= compras.length -1; c++) {
                var log = document.createElement("p");
                log.innerHTML = compras[c]
                contenedor.appendChild(log);
            };

            for (let d=0; d <= detalle.length -1; d++) {
                var log = document.createElement("p");
                log.innerHTML = detalle[d]
                contenedor.appendChild(log);
            };

            break;
        }

    }

}
function mostrar_analisis_capitulo(capitulo){
    var display_general = document.getElementById("datos_generales")
    display_general.style = "display: none;"

    var display_analisis = document.getElementById("datos_analisis")
    display_analisis.style = " "
    
    if (document.getElementById("tabla_detalle_saldo")){
        table = document.getElementById("tabla_detalle_saldo");
        table.remove();

        filter = document.getElementById("tabla_detalle_saldo_filter");
        filter.remove();

        wrapper = document.getElementById("tabla_detalle_saldo_wrapper");
        wrapper.remove();
    }

    var tabla_articulos_saldo = document.getElementById("tabla_articulos_saldo")

    var tabla = document.createElement("table");
    tabla.className = 'table table-bordered';
    tabla.id = 'tabla_detalle_saldo';
    
    var tabla_head = document.createElement("thead");
    tabla.appendChild(tabla_head);

    var tabla_cuerpo = document.createElement("tbody");
    tabla.appendChild(tabla_cuerpo);

    var fila = document.createElement("tr");
    fila.id = 'cabeza_tabla_saldo';
    fila.className = "font-bold";
    
    var celda_articulo = document.createElement("td");
    celda_articulo.innerHTML = 'Articulo';
    
    var celda_solicitado = document.createElement("td");
    celda_solicitado.innerHTML = 'Solicitado';
   
    var celda_comprado = document.createElement("td");
    celda_comprado.innerHTML = 'Comprado';
    
    var celda_saldo = document.createElement("td");
    celda_saldo.innerHTML = 'Saldo';


    fila.appendChild(celda_articulo);
    fila.appendChild(celda_solicitado);
    fila.appendChild(celda_comprado);
    fila.appendChild(celda_saldo);

    tabla_head.appendChild(fila);

    var object_capitulo = presupuesto_detallado[capitulo -1]
    var key_capitulo = Object.keys(object_capitulo)[0]

    for (let i=0; i <= object_capitulo[key_capitulo].data.length -1; i++) {
        
        var object = object_capitulo[key_capitulo].data[i]
        var id_articulo = Object.keys(object)[0]
        var fila = document.createElement("tr");
        fila.id = id_articulo;
        fila.style = "font-size: 13px"

        var celda_articulo = document.createElement("td")
        if (object[id_articulo].comprado > 0){
            celda_articulo.innerHTML = `<b class = "box text-primary" onclick="mostrar_detalle_articulo(${id_articulo})">${object[id_articulo].articulo}</b>`
        } else {
            celda_articulo.innerHTML = `<b class = "text-dark">${object[id_articulo].articulo}</b>`
        }
        
        var celda_solicitado = document.createElement("td")
        celda_solicitado.innerHTML = Intl.NumberFormat().format(object[id_articulo].cantidad)
        var celda_comprado = document.createElement("td")
        celda_comprado.innerHTML = Intl.NumberFormat().format(object[id_articulo].comprado)
        var celda_saldo = document.createElement("td")
        celda_saldo.innerHTML = `$${Intl.NumberFormat().format((object[id_articulo].cantidad - object[id_articulo].comprado) * object[id_articulo].precio)}`

        fila.appendChild(celda_articulo)
        fila.appendChild(celda_solicitado)
        fila.appendChild(celda_comprado)
        fila.appendChild(celda_saldo)
 
        tabla_cuerpo.appendChild(fila)

    }
    tabla_articulos_saldo.appendChild(tabla)

    $(document).ready(function () {
        $('#tabla_detalle_saldo').DataTable({
            "language": {
                "lengthMenu": "Mostar _MENU_ documentos",
                "zeroRecords": "Sin resultados ",
                "info": "Pagina _PAGE_ de _PAGES_",
                "infoEmpty": "Sin registros disponibles",
                "infoFiltered": "(filtrado de _MAX_ registros totales)",
                "search": "Buscar"
            },
            "paging": false,
            "info": false
        });
    });
}
// PRESUPUESTOS - SERVICE GESTION DE PROYECTO
async function service_cambio_estado(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/cambiar_estado_proyecto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "estado": document.getElementById("select_estado_presupuesto").value,
        })
    })

    var status = await respuesta.status
    return validar_cambio_estado(status)
}
async function service_cambio_presupuestador(){

    var notificar = 'NO'
    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/cambiar_presupuestador/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "presupuestador": document.getElementById("select_presupuestador").value,
            "notificar": notificar,
        })
    })

    var status = await respuesta.status
    return validar_cambio_presupuestador(status)
}
async function service_cambio_proyecto_base(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/cambiar_proyecto_base/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "proyecto_base": document.getElementById("select_proyecto_base").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_cambio_proyecto_base(response, status)
}
async function service_guardar_bitacora(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/guardar_bitacoras/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "titulo": document.getElementById("titulo").value,
            "hashtag": document.getElementById("hashtag_form").value,
            "descrip": document.getElementById("descrip").value,
        })
    })
    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_guardar_bitacora(response, status)
}
async function service_guardar_tarea(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/guardar_tareas/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "tarea": document.getElementById("tarea_guardar").value,
        })
    })
    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_guardar_tarea(response, status)
}
async function service_consultar_datos_bitacora(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/guardar_bitacoras/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "titulo": document.getElementById("titulo").value,
            "hashtag": document.getElementById("hashtag_form").value,
            "descrip": document.getElementById("descrip").value,
        })
    })

    var status = await respuesta.status
    return validar_guardar_bitacora(status)
}
async function service_consultar_bitacoras(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/consultar_bitacoras/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_consulta_bitacora(response, status)
}
async function service_consultar_tareas(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/consultar_tareas/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_consulta_tareas(response, status)
}
async function service_completar_tareas(id){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/completar_tareas/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "id": id,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_general(response, status)
}
async function service_desactivar_proyecto(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/desactivar_proyecto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_desactivar(response, status)
}
function validar_desactivar(response, status){
    if (status >= 200 && status <300){
        ventana_desactivado = document.getElementById("activo_off");
        ventana_desactivado.style = ' ';
        ventana_activado = document.getElementById("activo_on");
        ventana_activado.style = 'display: none;';
        desactivar_proyecto = document.getElementById("desactivar_proyecto");
        desactivar_proyecto.setAttribute('checked','checked');
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_general(response, status){
    if (status >= 200 && status <300){
        console.log("Realizado")
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_consulta_tareas(response, status){
    if (status >= 200 && status <300){
        tareas =  response
        armar_seccion_tareas();  
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_consulta_bitacora(response, status){
    if (status >= 200 && status <300){
        bitacoras =  response
        armar_seccion_bitacoras();  
    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_guardar_bitacora(response, status){
    if (status >= 200 && status <300){
        sweet_alert("Bitacora guardada", "success");  
        bitacoras.unshift(response);
        armar_seccion_bitacoras();  
    } else {
        sweet_alert("Error", "warning")
    }
}
function validar_guardar_tarea(response, status){
    if (status >= 200 && status <300){
        sweet_alert("Listo!", "success");  
        tareas.unshift(response);
        armar_seccion_tareas();  
    } else {
        sweet_alert("Error", "warning")
    }
}
function validar_cambio_estado(status){
    if (status >= 200 && status <300){
        sweet_alert("Cambio realizado", "success");
        armar_panel_gestion_proyecto();       
    } else {
        sweet_alert("Error", "warning")
    }
}
function validar_cambio_proyecto_base(response, status){
    if (status >= 200 && status <300){
        sweet_alert("Cambio realizado", "success");
        ocultar_select_proyecto_bases();
        var proyecto_base = document.getElementById("id_gp_proyecto_base")
        proyecto_base.innerHTML = response.proyecto  
        
        var select_proyecto_base = document.getElementById("select_proyecto_base")
        select_proyecto_base.style = "display: none;" 
    } else {
        sweet_alert("Error", "warning")
    }
}
function validar_cambio_presupuestador(status){
    if (status >= 200 && status <300){
        sweet_alert("Cambio realizado", "success");
        armar_panel_gestion_proyecto();       
    } else {
        sweet_alert("Error", "warning")
    }
}
// PRESUPUESTOS - GESTION DE PROYECTO
function armar_panel_gestion_proyecto(){
    service_datos_proyecto();
    ocultar_select_estados();
    ocultar_select_presupuestadores();
    service_consultar_bitacoras();
    service_consultar_tareas();  
}
function armar_seccion_tareas(){

    if (document.getElementById("listado_tareas")) {
        var listado = document.getElementById("listado_tareas")
        listado.remove()
    }

    var contenedor = document.getElementById("contenedor_tareas")
    var listado = document.createElement("ul")
    listado.id = "listado_tareas"
    listado.className = "scrollbox mt-2"
    listado.style = "height: 30vh; overflow-y: auto;"
    contenedor.append(listado)

    for (let i=0; i <= tareas.length -1; i++) {
        if (tareas[i].estado == "LISTO"){
            var tarea = document.createElement("li")
            tarea.id = `tarea_${tareas[i].id}`
            tarea.innerHTML = `<input type="checkbox" checked id="cb_tarea_${tareas[i].id}" class="chk-col-teal" />
            <label onclick="service_completar_tareas(${tareas[i].id})" for="cb_tarea_${tareas[i].id}">${tareas[i].tarea}</label>`
        } else {
            var tarea = document.createElement("li")
            tarea.id = `tarea_${tareas[i].id}`
            tarea.innerHTML = `<input type="checkbox" id="cb_tarea_${tareas[i].id}" class="chk-col-teal" />
            <label onclick="service_completar_tareas(${tareas[i].id})" for="cb_tarea_${tareas[i].id}">${tareas[i].tarea}</label>`
        }
        
        listado.appendChild(tarea)
    }
}
function armar_seccion_bitacoras(){

    if (document.getElementById("listado_bitacoras")) {
        var listado = document.getElementById("listado_bitacoras")
        listado.remove()
    }

    var contenedor = document.getElementById("contenedor_bitacoras")
    var listado = document.createElement("ul")
    listado.id = "listado_bitacoras"
    listado.className = "scrollbox mt-2"
    listado.style = "height: 30vh; overflow-y: auto;"
    contenedor.append(listado)
    for (let i=0; i <= bitacoras.length -1; i++) {
        
        var bitacora = document.createElement("li")
        bitacora.id = `bitacora_${bitacoras[i].id}`
        bitacora.className = "box"
        bitacora.innerHTML = `<b>${bitacoras[i].fecha}</b>: “${bitacoras[i].titulo}”`
        bitacora.onclick = function(){
            armar_modal_bitacora(bitacoras[i].id)
        }

        listado.appendChild(bitacora)
    }
}
function armar_panel_resumen(response){
    var estado_presupuesto_general = document.getElementById('proyecto_estado_referencia')
    estado_presupuesto_general.innerHTML = response.estado
    var estado_presupuesto = document.getElementById('id_gp_estado')
    estado_presupuesto.innerHTML = response.estado
    var tama = document.getElementById('id_gp_tamaño')
    tama.innerHTML = response.tama
    var proyecto_base = document.getElementById('id_gp_proyecto_base')
    proyecto_base.innerHTML = response.proyecto_base
    var presupuestador = document.getElementById('id_gp_presupuestador')
    presupuestador.innerHTML = response.presupuestador
    
}
function armar_modal_bitacora(id){
    for (let i=0; i <= bitacoras.length -1; i++) {

        if (bitacoras[i].id == id){
            var titulo = document.getElementById('titulo_ver_bitacora');
            titulo.innerHTML = bitacoras[i].titulo;

            var fecha = document.getElementById('fecha_ver_bitacora');
            fecha.innerHTML = bitacoras[i].fecha;

            var descrip = document.getElementById('descrip_ver_bitacora');
            descrip.innerHTML = `“${bitacoras[i].descrip}"`;
        }
    
    }
    
    $('#modalVerBitacora').modal('toggle')

}
function mostrar_select_estados(){
    var select = document.getElementById('select_estado_presupuesto');
    select.style = ' '
    var estado_presupuesto = document.getElementById('id_gp_estado');
    estado_presupuesto.onclick = function() {
        ocultar_select_estados();
    }
}
function ocultar_select_estados(){
    var select = document.getElementById('select_estado_presupuesto');
    select.style = 'display: none;'
    var estado_presupuesto = document.getElementById('id_gp_estado');
    estado_presupuesto.onclick = function() {
        mostrar_select_estados();
    }
}
function mostrar_select_presupuestadores(){
    var select = document.getElementById('contenedor_select_estado_presupuesto');
    select.style = ' '
    var presupuestador = document.getElementById('id_gp_presupuestador');
    presupuestador.onclick = function() {
        ocultar_select_presupuestadores();
    }
}
function mostrar_select_proyecto_bases(){
    var select = document.getElementById('select_proyecto_base');
    select.style = ' '
}
function ocultar_select_proyecto_bases(){
    var select = document.getElementById('select_proyecto_base');
    select.style = 'display: none;'
}
function ocultar_select_presupuestadores(){
    var select = document.getElementById('contenedor_select_estado_presupuesto');
    select.style = 'display: none;'
    var presupuestador = document.getElementById('id_gp_presupuestador');
    presupuestador.onclick = function() {
        mostrar_select_presupuestadores();
    }
}
// PRESUPUESTOS - REPORTE

async function service_datos_graficos(grafico, value){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/grafico_valor_proyecto/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
            "grafico": grafico,
            "value": value,

        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return modificar_grafico_valor_proyecto(response, status)
}
async function service_datos_graficos_constante(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/grafico_constantes/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return modificar_grafico_constantes(response, status)
}
async function service_datos_graficos_saldo(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/grafico_saldo/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById("proyecto").value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return modificar_grafico_saldo(response, status)
}
function modificar_grafico_saldo(response, status){

    if (status >= 200 && status <300){
        var data = response.data
        chart_saldo.data.datasets[0].data = data
        chart_saldo.update();
    }
    
}
function modificar_grafico_constantes(response, status){

    if (status >= 200 && status <300){
        var label = response.labels
        var data = response.data
        chart_constantes.data.labels = label
        chart_constantes.data.datasets[0].data = data
        chart_constantes.update();
    }
    
}
function modificar_grafico_valor_proyecto(response, status){
    console.log(response);
    if (status >= 200 && status <300){
        var label = response.labels
        var data = response.data
        chart_valor_proyecto.data.labels = label
        chart_valor_proyecto.data.datasets[0].data = data
        chart_valor_proyecto.update();
    }
    
}
// PRESUPUESTOS - HERRAMIENTAS EDICION DE COMPOSICIÓN
async function service_editar_modelo(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/modelo_editar_guardar/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "id": document.getElementById('id_modelo').value,
            "comentario": document.getElementById('comentario').value,
            "orden": document.getElementById('order').value,
            "cantidad": document.getElementById('cantidad').value,
            "analisis": document.getElementById('analisis').value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_edicion_modelo(response, status)
}
async function service_create_modelo(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/crear_modelo/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "proyecto": document.getElementById('proyecto').value,
            "capitulo": document.getElementById('capitulo_activo').value,
            "comentario": document.getElementById('comentario_create').value,
            "orden": document.getElementById('order_create').value,
            "cantidad": document.getElementById('cantidad_create').value,
            "analisis": document.getElementById('analisis_create').value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_creacion(response, status)
}
async function service_delete_modelo(){

    var host = document.getElementById("host").value;
    var token = document.getElementById("token").value;  
    const url = `${host}/presupuestos/api_presupuesto/borrar_modelo/`
    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "id": document.getElementById('id_modelo').value,
        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_borrado(response, status)
}
function validar_borrado(response, status){

    if (status >= 200 && status <300){
        limpiar_proyectos_afectados();
        limpiar_formulario_edicion();
        capitulos_presupuesto_detalle(response.capitulo);

    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
function validar_creacion(response, status){
    if (status >= 200 && status <300){
        sweet_alert("Modelo agregado", "success");
        limpiar_ventana_creacion();
        capitulos_presupuesto_detalle(response.capitulo);
        
    } else {
        sweet_alert("Error", "warning")
    }

}
function validar_edicion_modelo(response, status){

    if (status >= 200 && status <300){
        var boton_editar = document.getElementById("button_save");
        boton_editar.className = 'btn btn-secondary btn-rounded btn-xs';
        limpiar_proyectos_afectados();
        limpiar_formulario_edicion();
        capitulos_presupuesto_detalle(response.capitulo);

    } else {
        sweet_alert("Problemas de conexión", "warning")
    }
}
// PRESUPUESTOS - FUNCIONES GENERALES - CONSOLAS
function mostrar_consola_tools(){
    var consola = document.getElementById('presupuestos_tools');
    consola.style = " ";
    service_valor_capitulos();
}
function mostrar_consola_gestor(){
    var consola = document.getElementById('presupuestos_gestor');
    consola.style = " ";
    armar_panel_gestion_proyecto();
}
function mostrar_consola_datos(){
    var consola = document.getElementById('presupuestos_datos');
    consola.style = " ";
    service_consultar_datos_presupuesto();
    service_saldo_detallado_presupuesto();
    service_consultar_detalle_asignacion();
}
function mostrar_consola_reporte(){
    var consola = document.getElementById('presupuestos_reporte');
    consola.style = " ";
}
function ocultar_consola_datos(){
    var consola = document.getElementById('presupuestos_datos');
    consola.style = "display: none;";
}
function ocultar_consola_tools(){
    var consola = document.getElementById('presupuestos_tools');
    consola.style = "display: none;";
    service_valor_capitulos();
}
function ocultar_consola_gestor(){
    var consola = document.getElementById('presupuestos_gestor');
    consola.style = "display: none;";
    service_valor_capitulos();
}
function ocultar_consola_reporte(){
    var consola = document.getElementById('presupuestos_reporte');
    consola.style = "display: none;";
}
function ocultar_home(){
    var home = document.getElementById('presupuestos_home');
    home.style = "display: none;";
}
// PRESUPUESTOS - FUNCIONES GENERALES - TOOLS
function cambiar_boton_save(){
    var boton_editar = document.getElementById("button_save")
    boton_editar.className = 'btn btn-success btn-rounded btn-xs'
}
function mostrar_ventana_creacion(){
    limpiar_seleccion_analisis();
    ocultar_ventana_edicion();
    ocultar_boton_save();
    ocultar_boton_delete();
    mostrar_boton_save_creacion();

    var contenedor_create = document.getElementById("crear_analisis")
    contenedor_create.style = ''
}
function mostrar_ventana_edicion(){
    ocultar_ventana_creacion();
    mostrar_boton_save();
    var editar_opciones = document.getElementById("editar_analisis");
    editar_opciones.style = "";
}
function mostrar_boton_agregar(){
    var boton_agregar = document.getElementById("button_create");
    boton_agregar.style = ' ';
}
function mostrar_boton_save_creacion(){
    var boton_save = document.getElementById("button_create_mandar");
    boton_save.style = ' ';
}
function ocultar_boton_save_creacion(){
    var boton_save = document.getElementById("button_create_mandar");
    boton_save.style = 'display: none';
}
function mostrar_boton_save(){
    var button_save = document.getElementById("button_save");
    button_save.className = 'btn btn-secondary btn-rounded btn-xs';
    button_save.style = "";
}
function mostrar_boton_delete(){
    var boton_delete = document.getElementById("button_delete");
    boton_delete.style = ' ';
}
function ocultar_boton_delete(){
    var boton_delete = document.getElementById("button_delete");
    boton_delete.style = 'display: none';
}
function ocultar_ventana_creacion(){

    var contenedor_create = document.getElementById("crear_analisis")
    contenedor_create.style = 'display: none'
    ocultar_boton_save_creacion();
}
function ocultar_ventana_edicion(){

    var contenedor_editar = document.getElementById("editar_analisis")
    contenedor_editar.style = 'display: none'
}
function ocultar_boton_save(){

    var boton_save = document.getElementById("button_save")
    boton_save.style = 'display: none'
}
function limpiar_ventana_creacion(){

    var comentario = document.getElementById('comentario_create');
    comentario.value = "";
    var orden = document.getElementById('order_create');
    orden.value = " ";
    var cantidad = document.getElementById('cantidad_create');
    cantidad.value = " ";
    var analisis = document.getElementById('analisis_create');
    analisis.value = "";
}
function limpiar_formulario_edicion(){
    ocultar_boton_delete();
    var id_editar = document.getElementById("id_modelo");
    id_editar.value = "";

    var order_editar = document.getElementById("order");
    order_editar.value = "";

    var analisis_editar = document.getElementById("analisis");
    analisis_editar.value = "";

    var comentario_editar = document.getElementById("comentario");
    comentario_editar.value = "";

    var cantidad_editar = document.getElementById("cantidad");
    cantidad_editar.value = "";
}
function limpiar_proyectos_afectados(){
    var list = document.getElementById("list_proyectos_afectados");
    list.remove();
}
function realizar_sleccion_analisis(id){
    mostrar_boton_delete();
    var fila = document.getElementById(id);
    fila.className = "box text-info";
}
function modificar_capitulo_activo(title, id){
    var titulo = document.getElementById("titulo_composicion");
    titulo.innerHTML = ` ${title}`;

    var hidden_id_capitulo = document.getElementById("capitulo_activo");
    hidden_id_capitulo.value = ` ${id}`;
}
function limpiar_seleccion_analisis(){
    ocultar_boton_delete();
    var fila_old = document.getElementsByClassName("box text-info");
    if (fila_old.length > 0){
        fila_old[0].className = "box";
    }
}
