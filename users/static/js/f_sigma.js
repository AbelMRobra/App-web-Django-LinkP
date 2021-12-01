window.onload = service_consulta_resumen()

document.getElementById("crear_inventario").addEventListener("click", function(event){
    event.preventDefault()
    });

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

async function service_consulta_valor(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/sigma/api_inventario/consulta_valor_inventario/`

    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_consulta_valor(response, status)

}

function validar_consulta_valor(response, status){

    if (status >= 200 && status <300){
        console.log("Valor")
        console.log(response)
        var valor = document.getElementById('valor_inventario');

        valor.innerHTML = `$ ${response['data'].toFixed(2)}`

        
    }
}

async function service_consulta_resumen(nombre_articulo){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/sigma/api_inventario/consulta_resumen_articulos/`

    var respuesta = await fetch(url ,{
        method: "GET",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_consulta_resumen(response, status)

}

function validar_consulta_resumen(response, status){

    if (status >= 200 && status <300){
        
        if (document.getElementById('listado_resumen')) {
            var listado = document.getElementById('listado_resumen');
            listado.remove()

            if (response['data'].length > 0) {
            
                modificar_template_consulta_resumen(response)
            } 
        } else {
            sweet_alert("Consulta a la BBDD exitosa", "info");
            if (response['data'].length > 0) {
                
                modificar_template_consulta_resumen(response)
            } 
            
        }

        
    
    }
}

function modificar_template_consulta_resumen(response){

    var contenedor = document.getElementById('contenedor_resumen');

    var listado= document.createElement('div');
    listado.id = `listado_resumen`;
    contenedor.appendChild(listado);

    for (let i=0; i <= response['data'].length -1; i++){
        var componente = document.createElement('div');
        componente.id = `contedor_resumen_${response['data'][i].id}`
        componente.innerHTML = `
        
        <small onclick="service_consulta_inventario('${response['data'][i].articulo}')">${response['data'][i].articulo}</small>
        <p>Cantidad: <b>${response['data'][i].cantidad}</b></p>
        
        `

        listado.appendChild(componente);

    }

    service_consulta_valor()
    
}


async function service_consulta_inventario(nombre_articulo){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/sigma/api_inventario/consulta_articulos/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "nombre_articulo" : nombre_articulo,

        })

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_consulta_inventario(response, status)

}

function validar_consulta_inventario(response, status){

    if (status >= 200 && status <300){

        if (document.getElementById('padre_listado')) {
            var listado = document.getElementById('padre_listado');
            listado.remove()

            if (response['data'].length > 0) {
            
                modificar_template_consulta_inventario(response)
            } 
        } else {
            if (response['data'].length > 0) {
                sweet_alert("Listado de articulos", "info");
                modificar_template_consulta_inventario(response)
            } 
            
        }

        
    
    }
}

function modificar_template_consulta_inventario(response){

    var contenedor = document.getElementById('contenedor_listado');

    var listado= document.createElement('div');
    listado.id = `padre_listado`;
    contenedor.appendChild(listado);

    for (let i=0; i <= response['data'].length -1; i++){
        var componente = document.createElement('div');
        componente.className = "bg-white shadow-sm mb-2 p-3"
        componente.id = `contedor_${response['data'][i].id}`
        componente.innerHTML = `
        
            <div class="row">
                <div class="col-11">
                    <div class="row">

                    <div class="col-10">
                        <div class="row">
                            <h6><b>${response['data'][i].num_inv}</b></h6>
                        </div>
                        <div class="row">
                            <div class="col-6"> 
                                <p class="mb-0"><small><b>Compra:</b> ${response['data'][i].fecha_compra}</small></p>
                                <p class="mb-0"><small><b>Amort:</b> ${response['data'][i].fecha_amortizacion}</small></p>
                            </div>
                            <div class="col-6">
                                <p class="mb-0"><small><b>Valor:</b> $ ${response['data'][i]['articulo'].valor.toFixed(2)}</small></p>
                                <p class="mb-0"><small><b>Amort:</b> $ ${response['data'][i].valor_amortizacion.toFixed(2)}</small></p>
                            </div>
                        </div>
                    </div>

                    <div class="col-2 align-self-center">
                        <h5 class="text-center"><b>${response['data'][i].amortizacion}</b>  años</h5>
                    </div>
                </div>
                </div>
                <div class="col-1 align-self-center">
                    <i onclick="service_inventario_delete(${response['data'][i].id})" class="fa fa-trash text-danger"></i>
                </div>
            
            </div>
        
        `

        listado.appendChild(componente);

    }
    
}

async function service_inventario_delete(id_inventario){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/sigma/api_inventario/${id_inventario}/`

    var respuesta = await fetch(url ,{
        method: "DELETE",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },


    })


    var status = await respuesta.status

    return validar_inventario_delete(id_inventario, status)

}

function validar_inventario_delete(id_inventario, status){

    if (status >= 200 && status <300){

        sweet_alert("Inventario eliminado", "success");
        modificar_template_inventario_delete(id_inventario);
    
    } else {
        
        sweet_alert("Problemas de conexión", "warning");
    }
}

function modificar_template_inventario_delete(id_inventario){

    var componente = document.getElementById(`contedor_${id_inventario}`)
    componente.remove()

    service_consulta_resumen()

}

async function service_create_inventario(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/sigma/api_inventario/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            "num_inv" : document.getElementById("new_num_inv").value,
            "articulo" : document.getElementById("new_articulo").value,
            "precio_md" : document.getElementById("new_precio_md").value,
            // "constante" : document.getElementById("new_constante").value,
            "fecha_compra" : document.getElementById("new_fecha_compra").value,
            "amortizacion" : document.getElementById("new_amortizacion").value,
        })


    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_create_inventario(response, status)
}

function validar_respuesta_create_inventario(response, status){
    
    if (status >= 200 && status <300){

        sweet_alert("Inventado creado", "success");
        modificar_template_inventario_create(response);
    
    } else {
        
        sweet_alert("Problemas de conexión", "warning");
    }
}

function modificar_template_inventario_create(response){
    service_consulta_resumen()
}