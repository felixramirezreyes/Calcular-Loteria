// Tabla de resultados
$(document).ready(function () {

    var tabla = $('#tabdatos');

    tabla.css("border", "1px solid #000");

    tabla.DataTable({
        // dom: 'Bfrtip',
        // buttons: [
        //     { extend: 'copy', text: 'Copiar' },
        //     { extend: 'excel', text: 'Excel' },
        //     { extend: 'pdf', text: 'PDF' },
        //     { extend: 'print', text: 'Imprimir' },
        //         ],

        // Hacer que colapsen todas las filas constridas
        responsive: {
            details: {
                display: $.fn.dataTable.Responsive.display.childRowImmediate,
                type: ''
            }
        },

        fixedHeader: {
            header: true,
            footer: true
        },

        scrollX: true,
        // responsive: true,
        bLengthChange: false,
        lengthMenu: [13, 30, 60, 'All'],
        language: {
            "emptyTable": "Sin datos a presentar",
            "search":         "Busqueda",
            "info":           "Mostrando _START_ de _END_ de _TOTAL_ registros",
            "infoEmpty":      "Mostrando 0 to 0 of 0 registros",
            "infoFiltered":   "(filtrados de un total de _MAX_ registros)",
            "lengthMenu":     "Mostrar registros en bloques de _MENU_",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "zeroRecords":    "No se encontraron registos",
            "searchPlaceholder": "Escriba aqui el texto a filtrar",

            paginate: {
                'first': 'Primero',
                'last': 'Ultimo',
                'next':     'Proximo',
                'previous': 'Anterior'
            }
        }
    });

} );
