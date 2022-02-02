
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

async function service_comparativa_change(id, estado){

    sweet_alert("Procesando, espere ..", "info");

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    
    const url = `${host}/compras/api_comparativas/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'id' : id,
            'username' : document.getElementById("username").value,
            'estado' : estado,

        })

    })

    var response = await respuesta.json()
    var status = await respuesta.status

    return validar_respuesta_comparativa_change(response, status)
}

function validar_respuesta_comparativa_change(response, status){
    if (status >= 200 && status <300){

        sweet_alert(response.action, "success");
        editar_comparativa_change(response)
    
    } else {

        sweet_alert("Problemas de conexión", "warning");
    }
}

function editar_comparativa_change(response){

    var icono = document.getElementById(`simbolo_${response.id}`)

    console.log(response)

    if (response.action == "Compra autorizada") {

        console.log("Aqui 2")
        
        icono.style = "color: green;";
        icono.className = "fa fa-check";
        icono.title = "Todo listo!";
    } else if(response.action == "Adjunto chequeado") {

        console.log("Aqui 3")

        icono.style = "color: orange;";
        icono.className = "fa fa-check";
        icono.title = "El adjunto fue revisado";
    } else if(response.action == "Compra rechazada") {

        console.log("Aqui 3")

        icono.style = "color: darkred;";
        icono.className = "fa fa-times";
        icono.title = "Rechazada!";
    }

}
function habilitar_autorizacion_gerente(){

    var valor_compra = document.getElementById(`valor_compra`).value
    var contenedor = document.getElementById('contenedor_gerentes')

    if (valor_compra <= 50000){
        contenedor.style = " "
    } else {
        contenedor.style = "display: none;"
    }

}