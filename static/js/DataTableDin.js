// Funcion para retroceder
// function IrAtras() {
//     window.history.back();
// }

// Tabla de resultados
$(document).ready(function() {
    var tabla = $('#tabdatosdin').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            { extend: 'copy', text: 'Copiar' },
            { extend: 'excel', text: 'Excel' },
            { extend: 'pdf', text: 'PDF' },
            { extend: 'print', text: 'Imprimir' },
                ],
        scrollX: true,        
        lengthMenu: [12, 30, 60, 'All'],
        processing: true,         
        language: {
            "emptyTable": "Sin datos a presentar",
            "search":         "Busqueda:",
            "info":           "Mostrando _START_ de _END_ de _TOTAL_ registros",
            "infoEmpty":      "Mostrando 0 to 0 of 0 registros",
            "infoFiltered":   "(filtrados de un total de _MAX_ registros)",
            "lengthMenu":     "Mostrar registros en bloques de _MENU_",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "zeroRecords":    "No se encontraron registos",

            paginate: {
                'first': 'Primero',
                'last': 'Ultimo',
                'next':     'Proximo',
                'previous': 'Anterior'
            }
        }

    });

    $('#tabdatosdin tbody').on( 'click', 'td', function () {
        var filaActual = $(this).closest('tr');
        result = filaActual.find('a').text().trim();

        // var col1Val = 'col1Val: ' + filaActual.find('td:eq(0)').text().trim();
        // var col2Val = 'col2Val: ' + filaActual.find('td:eq(1)').text().trim();
        // var col2Nomb = 'col2Nomb: ' + filaActual.find('a').text().trim();
        // var cliqueado = 'cliqueado: ' +  tabla.cell( this ).data();

        if( result != '' ) {  // Alparecer no esta funcionando la comparacion
            // Almacenar el valor del codigo
            localStorage.setItem('CodigoProd', result);

            // Por el momento retroceder atras dos veces para llegar a la ventana indicada
            window.history.go(-2);
        };

        
    } );
});
