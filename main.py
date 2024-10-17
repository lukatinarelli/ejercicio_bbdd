import os, sys
import sqlite3

conexion = sqlite3.connect("CreatesBiblio.db")
cursor = conexion.cursor()


while True:
op = False

while op not in ["1", "2", "3", "4", "5", "6"]:
    os.system('cls' if os.name == 'nt' else 'clear')

    op = input("""¿Qué desea hacer?
    1. Crear tabla
    2. Insertar datos
    3. Consultar datos
    4. Modificar datos
    5. Eliminar datos
    9. Salir)
  Ingrese su opción: """)


if op == "1":
    input()


elif op == "2":
    input()



elif op == "3":



    tablas = [nombre[0] for nombre in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]

    print(tablas)










elif op == "9":
    sys.exit()








salida = cursor.execute('''SELECT * FROM cliente''').fetchall() 
  

for i in salida: 
  print(i) 


conexion.commit()
conexion.close()
