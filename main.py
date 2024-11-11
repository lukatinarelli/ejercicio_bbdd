from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from os import listdir, getcwd
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Configura una clave secreta para la sesión


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        # Si el método es POST, intentamos autenticar
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']
            if user == "admin" and password == "password":
                session['user'] = user  # Guarda el usuario en la sesión
                
                bbdd = listdir(getcwd() + '/databases')                
                return render_template('select_db.html', bbdd=bbdd)  # Redirige a la raíz '/'
            else:
                # Si no se autentica, muestra el error en el login
                return render_template('login.html', error="Usuario o contraseña incorrectos.")
        # Si es GET, mostramos el formulario de login
        return render_template('login.html')

    bbdd = session.get('bbdd')

    if bbdd:
        conn = connect_db()
        cursor = conn.cursor()
        tablas = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';").fetchall()  # Obtener las tablas
        conn.close()
        
        return render_template('index.html', tablas=tablas)   # bbdd=bbdd

    else:
        bbdd = listdir(getcwd() + '/databases')                
        return render_template('select_db.html', bbdd=bbdd)  # Redirige a la raíz '/'


# Ruta para cerrar sesión, ahora acepta el método POST
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)  # Elimina al usuario de la sesión
    return redirect(url_for('index'))  # Redirige al inicio de sesión


@app.route('/select_db', methods=['POST'])
def select_db():
    bbdd = request.form['nombre_bd']
    session['bbdd'] = bbdd

    return redirect(url_for('index'))


def connect_db():
    bbdd = session.get('bbdd')
    if bbdd:
        # Conectar a la base de datos seleccionada en la sesión
        return sqlite3.connect(f'databases/{bbdd}')
    else:
        # Si no hay base de datos seleccionada, lanza un error o retorna None
        raise ValueError("No se ha seleccionado ninguna base de datos.")


@app.route('/eliminar_tabla', methods=['POST'])
def eliminar_tablas():
    data = request.get_json()
    table_name = data.get('table_name')
    
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()
        
    except Exception as e:
        return f"Error: {str(e)}", 400 
    
    finally:
        conn.close()
    
    return redirect(url_for('index'))


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
    
    insert_html = '<form id="inserta" action="/inserta" method="POST"> <h2>Insertar en la tabla: {}</h2>'.format(table_name)

    insert_html += f'<input type="hidden" name="table_name_insertar" value="{table_name}">' # Nombre de la tabla

    for col in columnas:
        col_name = col[1].capitalize()
        col_type = col[2].capitalize()
        is_auto_increment = col[0] == 0 and (col[2].upper() == 'INTEGER' or col[2].upper() == 'INT') and col[5] == 1
        
        if is_auto_increment:
            insert_html += f'<p>{col_name} (Auto Increment, no necesita valor)</p>'
        else:
            insert_html += f'<p>{col_name} ({col_type}):</p>'
            insert_html += f'<input type="text" name="{col_name}" required><br>'
                
    insert_html += '</br> <input id="inserta_dato" type="submit" value="Insertar Datos" /> </form>'
  
    return insert_html  # Devolver el HTML generado


@app.route('/inserta', methods=['POST'])
def inserta_datos():
    table_name = request.form['table_name_insertar']

    conn = connect_db()
    cursor = conn.cursor()
    
    # Obtener columnas de la tabla
    columnas = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
    
    # Preparar un diccionario para insertar los datos
    data_to_insert = {}
    
    for col in columnas:
        col_name = col[1].capitalize()
        is_auto_increment = (col[2].upper() == 'INTEGER' or col[2].upper() == 'INT') and col[5] == 1
        
        if not is_auto_increment:
            data_to_insert[col_name] = request.form[col_name]
    
    columns = ', '.join(data_to_insert.keys())
    placeholders = ', '.join(['?'] * len(data_to_insert))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    try:
        cursor.execute(sql, tuple(data_to_insert.values()))
        conn.commit()
    except Exception as e:
        return f"Error: {str(e)}", 400  # Manejo de errores
    finally:
        conn.close()  # Asegúrate de cerrar la conexión
    
    # Redirigir a la página principal después de la inserción
    return redirect(url_for('index'))  # 'index' es el nombre de la función de tu página principal


@app.route('/eliminar', methods=['POST'])
def eliminar_datos():
    table_name = request.form['table_name_eliminar']  # Obtener el nombre de la tabla del formulario
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

    x = 0

    if datos:
        # Añadir encabezados de columna y aplicar estilo si es Primary Key
        for col in columnas:
            col_name = col[1].capitalize()
            is_primary_key = col[5] == 1  # Verificar si es Primary Key con el índice 5
            if is_primary_key:
                # Añadir clase "primary-key" para aplicar estilo especial
                tabla_html += f'<th title="Clave primaria" class="primary-key">{col_name}</th>'
                x = columnas.index(col)
            else:
                tabla_html += f'<th>{col_name}</th>'
        
        
        tabla_html += '<th>Eliminar registro</th></tr></thead><tbody>'
        
        # Añadir filas de datos
        for fila in datos:
            tabla_html += '<tr>'
            for valor in fila:
                tabla_html += f'<td>{valor}</td>'
            tabla_html += f'<td><button title="Eliminar registro" onclick="elimina_datos({fila[x]}, \'{table_name}\', \'{x}\')" id="boton{fila[x]}">Eliminar</button></td></tr>'
        tabla_html += '</tbody></table>'                          #
    else:
        tabla_html += '<p>No hay datos en esta tabla.</p>'

    return tabla_html  # Devolver el HTML generado


@app.route('/elimina', methods=['POST'])
def elimina_datos():
    data = request.get_json()
    id_registro = data.get('id')      # Obtiene el ID del registro
    nombre_tabla = data.get('tabla')  # Obtiene el nombre de la tabla
    columna = data.get('columna')  # Obtiene el numero de la columna

    if not id_registro or not nombre_tabla or not columna:
        return jsonify({'status': 'error', 'message': 'ID, tabla o columna no proporcionados'}), 400

    conn = connect_db()
    cursor = conn.cursor()
    
    columnas = cursor.execute(f"PRAGMA table_info({nombre_tabla})").fetchall()
    
    try:
        # Puedes usar la columna aquí si necesitas hacer algo específico con ella.
        cursor.execute(f"DELETE FROM {nombre_tabla} WHERE {columnas[int(columna)][1]} = ?;", (id_registro,))
        conn.commit()
        
        # Verificar si se eliminó algún registro
        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': 'Registro no encontrado'}), 404

        return jsonify({'status': 'success', 'message': f'Registro {id_registro} eliminado de {nombre_tabla}'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    finally:
        conn.close()


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    comando = data.get('comando')  
    
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Puedes usar la columna aquí si necesitas hacer algo específico con ella.
        resultado = cursor.execute(comando).fetchall()
        conn.commit()
        
        # Verificar si se eliminó algún registro
        if cursor.rowcount == 0:
            return jsonify({'status': 'error', 'message': 'Registro no encontrado'}), 404

        return jsonify({'status': 'success', 'message': f'Se ha ejecutado correctamente.\n {resultado}'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
