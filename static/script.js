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
    } else if (sectionId === 'eliminar-tabla') {
        const tableSelect = document.getElementById('table_name_para_eliminar');
        tableSelect.selectedIndex = 0; // Restablece a la opción en blanco
    }




    // AQUI ------------------------------------ ????????????




}


document.querySelectorAll('.capitalize').forEach(element => {
    if (element.tagName.toLowerCase() === 'select') {
        element.querySelectorAll('option').forEach(option => {
            option.innerHTML = option.innerHTML.toLowerCase().replace(/\b\w/g, (letra) => letra.toUpperCase());
        });
    } else {
        element.innerHTML = element.innerHTML.toLowerCase().replace(/\b\w/g, (letra) => letra.toUpperCase());
    }
});


// Manejar añadir columnas
document.getElementById('boton_crear_columna').addEventListener('click', function () {
    const tableBody = document.querySelector('#columnas_tabla tbody');
    const numColumns = tableBody.children.length;

    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td><input type="text" name="column_names[]" placeholder="Nombre columna" required></td>
        <td>
            <select name="column_types[]" required>
                <option value="TEXT">TEXT</option>
                <option value="INTEGER">INTEGER</option>
                <option value="REAL">REAL</option>
                <option value="BOOLEAN">BOOLEAN</option>
            </select>
        </td>
        <td><input type="checkbox" name="not_nulls[]"></td>
        <td>
            <input type="checkbox" name="primary_keys[]" class="primary-key" ${numColumns === 0 ? '' : 'disabled'}>
        </td>
        <td><button type="button" class="foreignkey_columna">Añadir</button></td>
        <td><button type="button" class="eliminar_columna">Eliminar</button></td>
    `;
    tableBody.appendChild(newRow);
});

// Manejar eliminar columnas y habilitar Primary Key en la primera fila
document.getElementById('columnas_tabla').addEventListener('click', function (event) {
    if (event.target.classList.contains('eliminar_columna')) {
        const row = event.target.closest('tr');
        row.remove();

        // Asegurarnos de habilitar la casilla de Primary Key en la primera fila después de eliminar
        const rows = document.querySelectorAll('#columnas_tabla tbody tr');
        rows.forEach((row, index) => {
            const pkCheckbox = row.querySelector('.primary-key');
            pkCheckbox.disabled = index !== 0; // Solo habilitar en la primera fila
        });
    }
});


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

function elimina_datos(id, tabla, columna) {
    // Enviar la solicitud POST al servidor para eliminar el registro
    fetch("/elimina", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id: id, tabla: tabla, columna: columna }) // Enviar los tres parámetros
    }) 
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);  // Muestra mensaje de éxito
            window.location.href = '/';
        } else {
            alert(data.message);  // Muestra mensaje de error
        }
    })
    .catch(error => console.error('Error:', error));
}


document.getElementById('boton_eliminar_tabla').addEventListener('click', function(event) {
    event.preventDefault(); 

    const table_name = document.getElementById('table_name_para_eliminar').value;

    fetch('/eliminar_tabla', {
        method: 'POST',
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({ table_name: table_name})
    })
    .then(response => {
        if (response.ok) {
            alert(`La tabla ${table_name} se ha eliminado correctamente`);
            window.location.href = '/';
        } else {
            alert("Error al eliminar la tabla");
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('boton_consola').addEventListener('click', function(event) {
    event.preventDefault();

    const comando = document.getElementById('comando').value;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify({ comando: comando })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = '/';
    })
    .catch(error => console.error('Error:', error));
});


// Referencias al botón y al modal
const botonAyuda = document.getElementById('boton_ayuda');
const modalAyuda = document.getElementById('modal-ayuda');
const closeModal = document.querySelector('.close');

// Mostrar el modal al hacer clic en el botón
botonAyuda.addEventListener('click', () => {
    modalAyuda.style.display = 'block';
});

// Cerrar el modal al hacer clic en la "X"
closeModal.addEventListener('click', () => {
    modalAyuda.style.display = 'none';
});

// Cerrar el modal al hacer clic fuera de la ventana modal
window.addEventListener('click', (event) => {
    if (event.target === modalAyuda) {
        modalAyuda.style.display = 'none';
    }
});


const modalForeign = document.getElementById('modal-foreignkey');
const closeModal2 = document.querySelector('.closee');

document.getElementById('columnas_tabla').addEventListener('click', function (event) {
    if (event.target.classList.contains('foreignkey_columna')) {
        console.log("hello world :)")
        modalForeign.style.display = 'block';
    }
});

// Cerrar el modal al hacer clic en la "X"
closeModal2.addEventListener('click', () => {
    modalForeign.style.display = 'none';
});


document.getElementById('tabla_referencia').addEventListener('change', function() {
    const tableName = this.value;

    // Realizar la solicitud al servidor
    fetch('/get_columns', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ table_name: tableName }), // Enviar el nombre de la tabla
    })
    .then(response => response.json())
    .then(data => {
        const columnaReferencia = document.getElementById('columna_referencia');
        columnaReferencia.innerHTML = ''; // Limpiar las opciones previas

        if (data.status === 'success') {
            // Agregar las nuevas opciones al select
            data.columns.forEach(columna => {
                const option = document.createElement('option');
                option.value = columna;
                option.textContent = columna;
                columnaReferencia.appendChild(option);
            });
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error al obtener columnas:', error);
        alert('Hubo un error al cargar las columnas. Verifica la consola para más detalles.');
    });
});
