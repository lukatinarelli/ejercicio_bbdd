from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('database.db')  # Cambia el nombre de tu base de datos

@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    tablas = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';").fetchall() # Obtener las tablas
    conn.close()
    
    return render_template('index.html', tablas=tablas)


@app.route('/consultar', methods=['POST'])
def consultar_datos():
    table_name = request.form['table_name_consultar']  # Obtener el nombre de la tabla del formulario
    conn = connect_db()
    cursor = conn.cursor()
    
    # Obtener las columnas y su información
    columnas = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
    
    # Obtener los datos de la tabla seleccionada
    datos = cursor.execute(f"SELECT * FROM {table_name};").fetchall()
    conn.close()

    # Construir la tabla HTML
    tabla_html = '<h3>Datos de la Tabla: {}</h3>'.format(table_name)
    tabla_html += '<table><thead><tr>'

    if datos:
        # Añadir encabezados de columna y aplicar estilo si es Primary Key
        for col in columnas:
            col_name = col[1].capitalize()
            is_primary_key = col[5] == 1  # Verificar si es Primary Key con el índice 5
            if is_primary_key:
                # Añadir clase "primary-key" para aplicar estilo especial
                tabla_html += f'<th title="Clave primaria" class="primary-key">{col_name}</th>'
            else:
                tabla_html += f'<th>{col_name}</th>'
        
        tabla_html += '</tr></thead><tbody>'
        
        # Añadir filas de datos
        for fila in datos:
            tabla_html += '<tr>'
            for valor in fila:
                tabla_html += f'<td>{valor}</td>'
            tabla_html += '</tr>'
        tabla_html += '</tbody></table>'
    else:
        tabla_html += '<p>No hay datos en esta tabla.</p>'

    return tabla_html  # Devolver el HTML generado


@app.route('/insertar', methods=['POST'])
def insertar_datos():
    table_name = request.form['table_name_insertar']  # Obtener el nombre de la tabla del formulario
    conn = connect_db()
    cursor = conn.cursor()
        
    columnas = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
    conn.close()
    
    
    insert_html = ''

    for col in columnas:
        col_name = col[1].capitalize()
        is_primary_key = col[5] == 1  # Verificar si es Primary Key con el índice 5
        
        insert_html += f'<p>{col_name}: </p> <input type="text">'
                
    
    insert_html += '</br> <input type="button" value="Insertar" />'
  
    return insert_html  # Devolver el HTML generado



if __name__ == '__main__':
    app.run(debug=True)
