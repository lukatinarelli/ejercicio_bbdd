function showSection(sectionId) {
    const sections = document.querySelectorAll('.form-section');
    sections.forEach(section => {
        section.style.display = 'none'; // Ocultar todas las secciones
    });

    const currentSection = document.getElementById(sectionId);
    currentSection.style.display = 'block'; // Mostrar la sección seleccionada

    // Si la sección es "consultar-datos", restablece el select y limpia los resultados
    if (sectionId === 'consultar-datos') {
        const tableSelect = document.getElementById('table_name');
        tableSelect.selectedIndex = 0; // Restablece a la opción en blanco
        
        // Limpia los resultados
        const resultadosDiv = document.getElementById('resultados');
        resultadosDiv.innerHTML = ''; // Elimina el contenido de los resultados
    }
}

$(document).ready(function(){
    $('#table_name').change(function() {
        var tableName = $(this).val(); // Obtener el valor seleccionado

        $.ajax({
            url: '/consultar',  // URL a la que se enviarán los datos
            type: 'POST',  // Método de la solicitud
            data: { table_name: tableName },  // Enviar el nombre de la tabla
            success: function(response) {
                $('#resultados').html(response);  // Insertar la respuesta en el div "resultados"
            }
        });
    });
});