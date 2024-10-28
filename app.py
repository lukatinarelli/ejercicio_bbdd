from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta principal: Mostrar todos los usuarios
@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

# Ruta para agregar un nuevo usuario
@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    age = request.form['age']
    conn = get_db_connection()
    conn.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Crear base de datos y tabla si no existen
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
    conn.close()
    # Ejecutar el servidor Flask
    app.run(debug=True)
