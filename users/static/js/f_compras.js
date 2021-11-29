// Deshabilitar refresh por form

document.getElementById("form_create").addEventListener("click", function(event){
    event.preventDefault()
    });

document.getElementById("form_upload").addEventListener("click", function(event){
    event.preventDefault()
    });

document.getElementById("cabeza_compra").addEventListener("click", function(event){
    event.preventDefault()
    });

document.getElementById("form_create_compra").addEventListener("click", function(event){
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

async function service_crear_proveedor(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/compras/api_proveedores/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'name' : document.getElementById("new_name").value,
            'descrip' : document.getElementById("new_descrip").value,
            'phone' : document.getElementById("new_phone").value,

        })

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_create(response, status)
}

function validar_respuesta_create(response, status){

    if (status >= 200 && status <300){

    sweet_alert("Proveedor creado!", "success");

    modificar_template_create(response);

    } else {
    sweet_alert("Hubo un problema!", "warning")
    }

}

function modificar_template_create(response){


    var row = `<tr>
    <td>${response.id}</td>
    <td id="${response.id}_proveedor_name"><a href='#' data-toggle="modal" data-target="#Modalproveedores" onclick="modal_editar_proveedor(${response.id})">${response.name}</a></td>
    <td id="${response.id}_proveedor_phone">${response.phone}</td>
    <td id="${response.id}_proveedor_descrip">${response.descrip}</td>
    </tr>`

    $('#example > tbody').append(row)


}

function modal_editar_proveedor(id_proveedor) {


    var name = document.getElementById(`${id_proveedor}_proveedor_name`).textContent
    var phone = document.getElementById(`${id_proveedor}_proveedor_phone`).textContent
    var descrip = document.getElementById(`${id_proveedor}_proveedor_descrip`).textContent
    var id = id_proveedor

    var upload_id = document.getElementById(`upload_proveedor_id`)
    upload_id.value = id
    var upload_name = document.getElementById(`upload_proveedor_name`)
    upload_name.value = name
    var upload_phone = document.getElementById(`upload_proveedor_phone`)
    upload_phone.value = phone
    var upload_descrip = document.getElementById(`upload_proveedor_descrip`)
    upload_descrip.textContent = descrip


}

async function service_upload_proveedor(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    id =  document.getElementById("upload_proveedor_id").value;
    
    const url = `${host}/compras/api_proveedores/${id}/`

    var respuesta = await fetch(url ,{
        method: "PUT",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'name' : document.getElementById("upload_proveedor_name").value,
            'phone' : document.getElementById("upload_proveedor_phone").value,
            'descrip' : document.getElementById("upload_proveedor_descrip").value,

        })

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_upload(response, status)
}

function validar_respuesta_upload(response, status){

    if (status >= 200 && status <300){

    sweet_alert("Proveedor modificado!", "success");

    modificar_template_upload(response);

    } else {
    sweet_alert("Hubo un problema!", "warning")
    }

}

function modificar_template_upload(response){

    var name = document.getElementById(`${response.id}_proveedor_name`)
    name.innerHTML = `<a href='#'
        data-toggle="modal" data-target="#Modalproveedores" 
        onclick="modal_editar_proveedor(${response.id})"
    >${response.name}</a>`


    var phone = document.getElementById(`${response.id}_proveedor_phone`)
    phone.innerHTML = response.phone

    var descrip = document.getElementById(`${response.id}_proveedor_descrip`)
    descrip.innerHTML = response.descrip



}

// Carga de compras

async function service_consulta_compra(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/compras/api_compras/consulta_compras/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'proyecto' : document.getElementById("proyecto").value,
            'proveedor' : document.getElementById("proveedor").value,
            'documento' : document.getElementById("documento").value,

        })

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_consulta_compra(response, status)
}

function validar_respuesta_consulta_compra(response, status){

    if (status >= 200 && status <300){

        if (document.getElementById('tarjeta')) {
            var tarjeta = document.getElementById('tarjeta');
            tarjeta.remove()

            var fecha = document.getElementById("fecha_c")
            fecha.value = ""

            if (response['data'].length > 0) {
            
                modificar_template_compras(response)
            } 
        } else {
            if (response['data'].length > 0) {
                sweet_alert("OC existente", "info");
                modificar_template_compras(response)
            } 
            
        }

        
    
    }
}

function modificar_template_compras(response){

    var fecha = document.getElementById("fecha_c")
    fecha.value = response['data'][0].fecha_c

    var contenedor = document.getElementById('list_articulos');

    var tarjeta = document.createElement('ol');
    tarjeta.id = `tarjeta`;
    contenedor.appendChild(tarjeta);
    for (let i=0; i <= response['data'].length -1; i++){
        var articulo = document.createElement('li');
        articulo.id = `articulo_${response['data'][i].id}`;
        articulo.className = 'list-group-item d-flex justify-content-between align-items-start'
        articulo.innerHTML = `
        
        <div class="ms-2 me-auto">
            <div class="fw-bold">${response['data'][i]['articulo'].codigo} - ${response['data'][i]['articulo'].nombre}</div>
            <small><b>Cantidad: </b> ${response['data'][i].cantidad.toFixed(2)} / <b>Precio: </b>$ ${response['data'][i].precio.toFixed(2)} / <b>Total: </b>$ ${(response['data'][i].precio * response['data'][i].cantidad).toFixed(2)}</small> 
            </div>
            <span class="badge bg-danger rounded-pill"
            onclick="borrar_compra(${response['data'][i].id})"><i 
            data-toggle="tooltip" data-placement="left" title="Borrar contacto"
            class="fa fa-trash-o"></i> </span>
        
        `

        tarjeta.appendChild(articulo);

    }
    
}

async function service_consulta_articulo(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/compras/api_compras/consulta_articulo/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'proyecto' : document.getElementById("proyecto").value,
            'articulo' : document.getElementById("articulo").value,

        })

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_consulta_articulo(response, status)
}

function validar_respuesta_consulta_articulo(response, status){
    if (status >= 200 && status <300){

        modificar_template_consulta_articulo(response)
    
    } else {
        console.log("Aqui")
        var cantidad = document.getElementById("cantidad_presupuesto")
        cantidad.innerHTML = ""

        var cantidad = document.getElementById("cantidad_comprada")
        cantidad.innerHTML = ""

        var unidad = document.getElementById("unidad_articulo")
        unidad.innerHTML = ""

        var partida = document.getElementById("partida_cargar")
        partida.value = ""
        

        var precio_presupuesto = document.getElementById("precio_presupuesto_cargar")
        precio_presupuesto.value = ""
    }
}

function modificar_template_consulta_articulo(response){
    
    var cantidad = document.getElementById("cantidad_presupuesto")
    cantidad.innerHTML = response.cantidad

    var cantidad = document.getElementById("cantidad_comprada")
    cantidad.innerHTML = response.comprado

    var unidad = document.getElementById("unidad_articulo")
    unidad.innerHTML = response.unidad

    var partida = document.getElementById("partida_cargar")
    partida.value = response.partida
    

    var precio_presupuesto = document.getElementById("precio_presupuesto_cargar")
    precio_presupuesto.value = response.precio
}

async function service_crear_compra(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/compras/api_compras/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'proyecto' : document.getElementById("proyecto").value,
            'proveedor' : document.getElementById("proveedor").value,
            'nombre' : document.getElementById("documento").value,
            'documento' : document.getElementById("documento").value,
            'articulo' : document.getElementById("articulo").value,
            'tipo' : 'normal',
            'cantidad' : document.getElementById("cantidad_cargar").value,
            'precio' : document.getElementById("precio_cargar").value,
            'precio_presup' : document.getElementById("precio_presupuesto_cargar").value,
            'fecha_c' : document.getElementById("fecha_c").value,
            'partida' : document.getElementById("partida_cargar").value,
            'cantidad_presupuesto' : document.getElementById("cantidad_presupuesto").innerHTML,
 
        })

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_consulta_compra_carga(response, status)
}


function validar_respuesta_consulta_compra_carga(response, status){
    if (status >= 200 && status <300){

        sweet_alert("Compra cargada", "success");
        service_consulta_compra();
        service_consulta_articulo();
    
    } else if (status == 406) {
        sweet_alert("Error de carga", "warning");
    } else {
        sweet_alert("Prblemas de conexión", "warning");
    }
}

async function borrar_compra(id_compra){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/compras/api_compras/${id_compra}/`

    var respuesta = await fetch(url ,{
        method: "DELETE",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

    })

    var status = await respuesta.status

    return validar_respuesta_consulta_compra_delete(status)
}


function validar_respuesta_consulta_compra_delete(status){
    if (status >= 200 && status <300){

        sweet_alert("Compra borrda", "success");
        service_consulta_compra();
        service_consulta_articulo();
    
    } else {
        sweet_alert("Prblemas de conexión", "warning");
    }
}




