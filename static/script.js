function showSection(sectionId) {
    const sections = document.querySelectorAll('.form-section');
    sections.forEach(section => {
        section.style.display = 'none'; // Ocultar todas las secciones
    });

    const currentSection = document.getElementById(sectionId);
    currentSection.style.display = 'block'; // Mostrar la sección seleccionada

    // Si la sección es "consultar-datos", restablece el select y limpia los resultados
    if (sectionId === 'consultar-datos') {
        const tableSelect = document.getElementById('table_name_consultar');
        tableSelect.selectedIndex = 0; // Restablece a la opción en blanco
        
        // Limpia los resultados
        const resultadosDiv = document.getElementById('resultados');
        resultadosDiv.innerHTML = ''; // Elimina el contenido de los resultados

    } else if (sectionId === 'insertar-datos') {
        const tableSelect = document.getElementById('table_name_insertar');
        tableSelect.selectedIndex = 0; // Restablece a la opción en blanco
        
        // Limpia los resultados
        const resultadosDiv = document.getElementById('insertar');
        resultadosDiv.innerHTML = ''; // Elimina el contenido de los resultados
    } else if (sectionId === 'eliminar-datos') {
        const tableSelect = document.getElementById('table_name_eliminar');
        tableSelect.selectedIndex = 0; // Restablece a la opción en blanco
        
        // Limpia los resultados
        const resultadosDiv = document.getElementById('eliminar');
        resultadosDiv.innerHTML = ''; // Elimina el contenido de los resultados
    }
}

$(document).ready(function(){
    $('#table_name_consultar').change(function() {
        var tableName = $(this).val(); // Obtener el valor seleccionado

        $.ajax({
            url: '/consultar',  // URL a la que se enviarán los datos
            type: 'POST',  // Método de la solicitud
            data: { table_name_consultar: tableName },  // Enviar el nombre de la tabla
            success: function(response) {
                $('#resultados').html(response);  // Insertar la respuesta en el div "resultados"
            }
        });
    });
});

$(document).ready(function(){
    $('#table_name_insertar').change(function() {
        var tableName = $(this).val(); // Obtener el valor seleccionado

        $.ajax({
            url: '/insertar',  // URL a la que se enviarán los datos
            type: 'POST',  // Método de la solicitud
            data: { table_name_insertar: tableName },  // Enviar el nombre de la tabla
            success: function(response) {
                $('#insertar').html(response);  // Insertar la respuesta en el div "resultados"
            }
        });
    });
});

$(document).ready(function(){
    $('#table_name_eliminar').change(function() {
        var tableName = $(this).val(); // Obtener el valor seleccionado

        $.ajax({
            url: '/eliminar',  // URL a la que se enviarán los datos
            type: 'POST',  // Método de la solicitud
            data: { table_name_eliminar: tableName },  // Enviar el nombre de la tabla
            success: function(response) {
                $('#eliminar').html(response);  // Insertar la respuesta en el div "resultados"
            }
        });
    });
});


/*const button = document.getElementById('#boton_{fila}');
button.addEventListener("click", (event) => {
    console.log("Button clicked!");
});*/
