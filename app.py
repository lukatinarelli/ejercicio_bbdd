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
def consultar_tabla():
    table_name = request.form['table_name']  # Obtener el nombre de la tabla del formulario
    conn = connect_db()
    cursor = conn.cursor()
    
    datos = cursor.execute(f"SELECT * FROM {table_name};").fetchall()  # Consulta todos los datos de la tabla seleccionada
    conn.close()

    # Construir la tabla HTML para devolverla
    tabla_html = '<h3>Datos de la Tabla: {}</h3>'.format(table_name)
    tabla_html += '<table><thead><tr>'
    if datos:
        # Añadir encabezados de columna
        x = len(datos[0])
        for col in ______:
            tabla_html += '<th>Columna {}</th>'.format(col + 1)  # Cambia esto para mostrar nombres de columnas reales si es necesario
        tabla_html += '</tr></thead><tbody>'
        
        # Añadir filas de datos
        for fila in datos:
            tabla_html += '<tr>'
            for valor in fila:
                tabla_html += '<td>{}</td>'.format(valor)
            tabla_html += '</tr>'
        tabla_html += '</tbody></table>'
    else:
        tabla_html += '<p>No hay datos en esta tabla.</p>'

    return tabla_html  # Devolver el HTML generado

if __name__ == '__main__':
    app.run(debug=True)
