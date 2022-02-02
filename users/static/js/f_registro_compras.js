var proveedores_seleccionados = []
var articulos_seleccionados = []
var proyectos_seleccionados = []


async function service_consulta_compras(){

    host = document.getElementById("host").value;
    token = document.getElementById("token").value;
    const url = `${host}/compras/api_compras/consulta_compras_completa/`

    var respuesta = await fetch(url ,{
        method: "POST",
        headers: {
            'X-CSRFToken' : `${token}`,
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            'proyectos_seleccionados' : proyectos_seleccionados,
            'articulos_seleccionados' : articulos_seleccionados,
            'proveedores_seleccionados' : proveedores_seleccionados,

        })
    })

    var response = await respuesta.json()
    var status = await respuesta.status
    return validar_respuesta_consulta_completa(response, status)
    
}
function validar_respuesta_consulta_completa(response, status){
    if (status >= 200 && status <300){
        console.log(response.data)
        if (document.getElementById("tabla_detalle")){
            list = document.getElementById("tabla_detalle");
            list.remove();
        }

        if (document.getElementById("tabla_detalle_filter")){
            filter = document.getElementById("tabla_detalle_filter");
            filter.remove();
        }

        var presentacion = document.getElementById("presentacion");
        presentacion.style = 'display: none;'
        var contenedor = document.getElementById("contenedor_detalle_compras");
        contenedor.style = ' '
        var tabla = document.createElement("table");
        tabla.className = 'table table-bordered';
        tabla.id = 'tabla_detalle';

        var tabla_encabezado = document.createElement("thead");
        tabla.appendChild(tabla_encabezado);

        var tabla_cuerpo = document.createElement("tbody");
        tabla.appendChild(tabla_cuerpo);

        var fila = document.createElement("tr");
        fila.id = 'cabeza_tabla';
        fila.className = "font-bold";
        var celda_fecha = document.createElement("td");
        celda_fecha.innerHTML = 'Fecha';
        var celda_proyecto= document.createElement("td");
        celda_proyecto.innerHTML = 'Proyecto';
        var celda_nombre = document.createElement("td");
        celda_nombre.innerHTML = 'Analisis';
        var celda_precio_unitario = document.createElement("td");
        celda_precio_unitario.innerHTML = '$ unit';
        var celda_cantidad = document.createElement("td");
        celda_cantidad.innerHTML = 'Cantidad';
        var celda_precio_total = document.createElement("td");
        celda_precio_total.innerHTML = 'Total';

        fila.appendChild(celda_fecha);
        fila.appendChild(celda_proyecto);
        fila.appendChild(celda_nombre);
        fila.appendChild(celda_precio_unitario);
        fila.appendChild(celda_cantidad);
        fila.appendChild(celda_precio_total);

        tabla_encabezado.appendChild(fila);

        for (let i=0; i <= response.data.length -1; i++) {
            var fila = document.createElement("tr");
            fila.id = response.data[i].id;
            fila.className = "box";
            fila.onclick = function() {
                abrir_consola_edicion_modelo(response.data[i].id);
            }
            fila.style = "font-size: 13px"

            var celda_fecha = document.createElement("td")
            celda_fecha.innerHTML = response.data[i].fecha_c
            var celda_proyecto = document.createElement("td")
            celda_proyecto.innerHTML = response.data[i].proyecto.nombre
            var celda_nombre = document.createElement("td")
            celda_nombre.innerHTML = `${response.data[i].articulo.nombre} (${response.data[i].articulo.unidad})<div><small>Documento: ${response.data[i].documento}, ${response.data[i].proveedor.name}</small></div> `
            var celda_precio_unitario = document.createElement("td")
            celda_precio_unitario.innerHTML = Intl.NumberFormat().format(response.data[i].precio)
            var celda_cantidad = document.createElement("td")
            celda_cantidad.innerHTML = Intl.NumberFormat().format(response.data[i].cantidad)
            var celda_precio_total = document.createElement("td")
            celda_precio_total.innerHTML = Intl.NumberFormat().format(response['data'][i].precio * response['data'][i].cantidad)

            fila.appendChild(celda_fecha);
            fila.appendChild(celda_proyecto);
            fila.appendChild(celda_nombre);
            fila.appendChild(celda_precio_unitario);
            fila.appendChild(celda_cantidad);
            fila.appendChild(celda_precio_total);

            tabla_cuerpo.appendChild(fila)

        }
        contenedor.appendChild(tabla)

        $(document).ready(function () {
            $('#tabla_detalle').DataTable({
                "language": {
                    "lengthMenu": "Mostar _MENU_ documentos",
                    "zeroRecords": "Sin resultados",
                    "info": "Pagina _PAGE_ de _PAGES_",
                    "infoEmpty": "Sin registros disponibles",
                    "infoFiltered": "(filtrado de _MAX_ registros totales)",
                    "search": "Buscar"
                },
                "paging": false,
                "ordering": false,
                "info": false
            });
        });


    } else {
        sweet_alert("Problemas de conexión", "error");
    }     
}
function agregar_proyecto_lista(){
    var lista = document.getElementById("proyectos_list");
    var proyecto = document.getElementById("proyecto") ;

    var listaArray = Array.prototype.map.call(lista.options, function(option) {
        return option.value;
      });


    if (listaArray.indexOf(proyecto.value) >= 0){
        var contenedor = document.getElementById('filter_conteiner')
        var etiqueta = document.createElement('span')
        etiqueta.className = "label label-inverse m-1"
        etiqueta.innerHTML = proyecto.value
        contenedor.appendChild(etiqueta)
        proyectos_seleccionados.push(`${proyecto.value}`)
        proyecto.value = ""
        console.log(proyectos_seleccionados)

    } else {
        console.log("no pego")
    }
}
function agregar_articulo_lista(){
    var lista = document.getElementById("articulos_list");
    var articulo = document.getElementById("articulos") ;

    var listaArray = Array.prototype.map.call(lista.options, function(option) {
        return option.value;
      });

    console.log(listaArray)

    if (listaArray.indexOf(articulo.value) >= 0){
        var contenedor = document.getElementById('filter_conteiner')
        var etiqueta = document.createElement('span')
        etiqueta.className = "label label-inverse m-1"
        etiqueta.innerHTML = articulo.value
        articulos_seleccionados.push(`${articulo.value}`)
        contenedor.appendChild(etiqueta)
        articulo.value = ""

    } else {
        console.log("no pego")
    }
}
function agregar_proveedor_lista(){
    var lista = document.getElementById("proveedores_list");
    var proveedor = document.getElementById("proveedor") ;

    var listaArray = Array.prototype.map.call(lista.options, function(option) {
        return option.value;
      });

    console.log(listaArray)

    if (listaArray.indexOf(proveedor.value) >= 0){
        var contenedor = document.getElementById('filter_conteiner')
        var etiqueta = document.createElement('span')
        etiqueta.className = "label label-inverse m-1"
        etiqueta.innerHTML = proveedor.value
        proveedores_seleccionados.push(`${proveedor.value}`)
        contenedor.appendChild(etiqueta)
        proveedor.value = ""

    } else {
        console.log("no pego")
    }
}

    
