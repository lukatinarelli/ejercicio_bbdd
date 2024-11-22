from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from os import listdir, getcwd
import sqlite3, os
import logging
logging.basicConfig(level=logging.DEBUG) # logging.info("")


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
                return render_template('bbdd/select_db.html', bbdd=bbdd)  # Redirige a la raíz '/'
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
        
        return render_template('index.html', tablas=tablas)

    else:
        bbdd = listdir(getcwd() + '/databases')                
        return render_template('bbdd/select_db.html', bbdd=bbdd)  # Redirige a la raíz '/'


# Ruta para cerrar sesión, ahora acepta el método POST
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)  # Elimina al usuario de la sesión
    return redirect(url_for('index'))  # Redirige al inicio de sesión


@app.route('/select_db', methods=['POST'])
def select_db():
    bbdd = request.form['nombre_bd']

    if bbdd == "nueva_db":
        return render_template('bbdd/crear_bbdd.html')
    
    elif bbdd == "borrar_db":
        bbdd = listdir(getcwd() + '/databases') 
        return render_template('bbdd/eliminar_bbdd.html', bbdd=bbdd)

    else:
        session['bbdd'] = bbdd

        return redirect(url_for('index'))
    

@app.route('/crear_bbdd', methods=['POST'])
def crear_bbdd():
    bbdd = request.form['nombre_bd_crear']

    session['bbdd'] = f"{bbdd}.db"

    return redirect(url_for('index'))


@app.route('/eliminar_db', methods=['POST'])
def eliminar_db():
    bbdd = request.form['eliminar_ddb']

    os.remove(getcwd() + '/databases/' + bbdd)

    session.pop('user', None)  # Elimina al usuario de la sesión
    return redirect(url_for('index'))  # Redirige al inicio de sesión  # problema ------------------------------------------------


def connect_db():
    bbdd = session.get('bbdd')
    if bbdd:
        # Conectar a la base de datos seleccionada en la sesión
        return sqlite3.connect(f'databases/{bbdd}')
    else:
        # Si no hay base de datos seleccionada, lanza un error o retorna None
        raise ValueError("No se ha seleccionado ninguna base de datos.")
    

@app.route('/create_table', methods=['POST'])
def create_table():
    table_name = request.form['table_name']
    column_names = request.form.getlist('column_names[]')
    column_types = request.form.getlist('column_types[]')
    not_nulls = request.form.getlist('not_nulls[]')
    primary_keys = request.form.getlist('primary_keys[]')

    # Asegurarse de que todas las listas tengan el mismo tamaño
    # Rellenar `primary_keys` y `not_nulls` con valores predeterminados
    not_nulls = ['off' if i >= len(not_nulls) else not_nulls[i] for i in range(len(column_names))]
    primary_keys = ['off' if i >= len(primary_keys) else primary_keys[i] for i in range(len(column_names))]

    if not table_name or not column_names:
        return "El nombre de la tabla y las columnas son obligatorios.", 400

    columns_sql = []
    primary_key_set = False

    for i in range(len(column_names)):
        column_definition = f"{column_names[i]} {column_types[i]}"

        if primary_keys[i] == 'on':
            if primary_key_set:
                return "Solo una columna puede ser la Primary Key.", 400
            primary_key_set = True
            column_definition += " PRIMARY KEY"
            if column_types[i] == "INTEGER":  # Agregar AUTOINCREMENT si es PRIMARY KEY e INTEGER
                column_definition += " AUTOINCREMENT"

        if not_nulls[i] == 'on':
            column_definition += " NOT NULL"

        columns_sql.append(column_definition)

    create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns_sql)});"

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except sqlite3.Error as e:
        return f"Error al crear la tabla: {e}", 500


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
    tabla_html = '<h3>Datos de la Tabla: {}</h3>'.format(table_name.capitalize())
    tabla_html += '<table><thead><tr>'

    if datos:
        # Añadir encabezados de columna y aplicar estilo si es Primary Key
        col_types = []  # Lista para almacenar los tipos de columna
        for col in columnas:
            col_name = col[1].capitalize()
            
            if col[2].upper() == 'TEXT':
                col_type = 'Texto'
            
            elif col[2].upper() == 'INTEGER':
                col_type = 'Número entero'
            
            elif col[2].upper() == 'REAL':
                col_type = 'Número decimal'
                
            elif col[2].upper() == 'BOOLEAN':
                col_type = 'Valor booleano'
            
            col_types.append(col[2].upper())  # Guardar el tipo de columna
            
            is_primary_key = col[5] == 1  # Verificar si es Primary Key con el índice 5
            
            if is_primary_key:
                # Añadir clase "primary-key" para aplicar estilo especial
                tabla_html += f'<th title="Clave primaria" class="primary-key">{col_name.upper()}</th>'
            else:
                tabla_html += f'<th style="width: 250px;">{col_name}<br>Tipo: {col_type}</th>'
        
        tabla_html += '</tr></thead><tbody>'
        
        # Añadir filas de datos
        for fila in datos:
            tabla_html += '<tr>'
            for idx, valor in enumerate(fila):
                # Convertir valores booleanos
                if col_types[idx] == 'BOOLEAN':
                    valor = 'true' if valor == 1 else 'false'
                tabla_html += f'<td>{valor}</td>'
            tabla_html += '</tr>'
        tabla_html += '</tbody></table></div>'
    else:
        tabla_html += '<p>No hay datos en esta tabla.</p>'

    return tabla_html  # Devolver el HTML generado



@app.route('/insertar', methods=['POST'])
def insertar_datos():
    table_name = request.form['table_name_insertar']  # Obtener el nombre de la tabla del formulario
    conn = connect_db()
    cursor = conn.cursor()
        
    columnas = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
    
    insert_html = '<form id="inserta" action="/inserta" method="POST"> <h2>Insertar en la tabla: {}</h2>'.format(table_name.capitalize())

    insert_html += f'<input type="hidden" name="table_name_insertar" value="{table_name}">' # Nombre de la tabla

    for col in columnas:
        col_name = col[1].capitalize()
        col_type = col[2].capitalize()
        not_null = col[3]  # Si es NOT NULL (1 = Sí, 0 = No)
        is_auto_increment = col[0] == 0 and (col[2].upper() == 'INTEGER' or col[2].upper() == 'INT') and col[5] == 1
        
        if is_auto_increment:
            insert_html += f'<p style="background-color: yellow; display: inline-block; font-size:18px;">{col_name.upper()} (Auto Increment, no necesita valor)</p></br>'
        else:
            if not_null == 1:         
                if col_type == 'Text':
                    insert_html += f'<p>{col_name} (Texto):</p>'
                    insert_html += f'<input type="text" name="{col_name}" required><br>'

                elif col_type == 'Integer':
                    insert_html += f'<p>{col_name} (Número entero):</p>'
                    insert_html += f'<input type="number" name="{col_name}" title="Solo se aceptan números enteros" step="1" required><br>'

                elif col_type == 'Real':
                    insert_html += f'<p>{col_name} (Número entero):</p>'
                    insert_html += f'<input type="number" name="{col_name}" title="Solo se aceptan números" step="any" required><br>'
                    
                elif col_type == 'Boolean':
                    insert_html += f'<p>{col_name} (Valor booleano):</p>'
                    insert_html += f'<input type="checkbox" />'
            
            elif not_null == 0:
                if col[5] == 1:
                    if col_type == 'Text':
                        insert_html += f'<p style="background-color: yellow; display: inline-block; font-size:18px;">{col_name} (Texto y Clave primaria):</p></br>'
                        insert_html += f'<input type="text" name="{col_name}" required><br>'

                    elif col_type == 'Integer':
                        insert_html += f'<p style="background-color: yellow; display: inline-block; font-size:18px;">{col_name} (Número entero y Clave primaria):</p></br>'
                        insert_html += f'<input type="number" name="{col_name}" title="Solo se aceptan números enteros" step="1" required><br>'

                    elif col_type == 'Real':
                        insert_html += f'<p style="background-color: yellow; display: inline-block; font-size:18px;">{col_name} (Número entero y Clave primaria):</p></br>'
                        insert_html += f'<input type="number" name="{col_name}" title="Solo se aceptan números" step="any" required><br>'

                    elif col_type == 'Boolean':
                        insert_html += f'<p style="background-color: yellow; display: inline-block; font-size:18px;">{col_name} (Valor boolean y Clave primaria):</p></br>'
                        insert_html += f'<input type="checkbox" />'

                elif col[5] == 0:
                    if col_type == 'Text':
                        insert_html += f'<p>{col_name} (Texto):</p>'
                        insert_html += f'<input type="text" name="{col_name}"><br>'

                    elif col_type == 'Integer':
                        insert_html += f'<p>{col_name} (Número entero):</p>'
                        insert_html += f'<input type="number" name="{col_name}" title="Solo se aceptan números enteros" step="1"><br>'

                    elif col_type == 'Real':
                        insert_html += f'<p>{col_name} (Número entero):</p>'
                        insert_html += f'<input type="number" name="{col_name}" title="Solo se aceptan números" step="any"><br>'

                    elif col_type == 'Boolean':
                        insert_html += f'<p>{col_name} (Valor boolean):</p>'
                        insert_html += f'<input type="checkbox" />'
                
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
        col_type = col[2].upper()  # Tipo de la columna
        is_auto_increment = (col_type == 'INTEGER' or col_type == 'INT') and col[5] == 1
        
        if not is_auto_increment:
            # Si es BOOLEAN y el input es un checkbox
            if col_type == 'BOOLEAN':
                # Checkbox envía 'on' si está marcado, nada si no lo está
                data_to_insert[col_name] = 1 if col_name in request.form else 0
            else:
                data_to_insert[col_name] = request.form.get(col_name)
    
    # Preparar la consulta SQL
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
            tabla_html += f'<td><button title="Eliminar registro" onclick="elimina_datos(\'{fila[x]}\', \'{table_name}\', \'{x}\')" id="boton{fila[x]}">Eliminar</button></td></tr>'
        tabla_html += '</tbody></table>'                          #
    else:
        tabla_html += '<p>No hay datos en esta tabla.</p>'

    return tabla_html  # Devolver el HTML generado


@app.route('/elimina', methods=['POST'])
def elimina_datos():
    data = request.get_json()
    id_registro = data.get('id')    # Obtiene el ID del registro
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
