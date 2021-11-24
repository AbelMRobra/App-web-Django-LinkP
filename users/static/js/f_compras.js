// Deshabilitar refresh por form

document.getElementById("form_create").addEventListener("click", function(event){
    event.preventDefault()
    });

document.getElementById("form_upload").addEventListener("click", function(event){
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


