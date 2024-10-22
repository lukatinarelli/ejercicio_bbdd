import os, sys
import sqlite3

conexion = sqlite3.connect("CreatesBiblio.db")
cursor = conexion.cursor()



os.system('cls' if os.name == 'nt' else 'clear')


while True:
    tablas = [nombre[0] for nombre in cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';").fetchall()]
    op = False

    op = input("""¿Qué desea hacer?
    1. Crear tabla
    2. Eliminar tabla
    3. Insertar datos
    4. Consultar datos
    5. Modificar datos
    6. Eliminar datos
    7. Salir
Ingrese su opción: """)


    if op == "1": # Crear tablas:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        nombre = input("¿Qué nombre quiere ponerle a la tabla? ")
        
        
        lista_atributos = []
        lista_atributos_tipos = [] 
        
        while True: # Guardar los atributos de la tabla nueva
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(chr(27) + "[1;31m" + "Recuerda que el nombre de los atributos no puede tener espacios ni acentos." + chr(27) + "[;m")
            atributo = input("Introduce los atributos que quieras de uno en uno (o escribe 'salir' para terminar): ")
            
            if atributo == "salir":
                break 
            
            lista_atributos.append(atributo)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        
        for i in lista_atributos: # Guardar el tipo de cada atributo
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("¿Cuál es el tipo de dato de cada atributo? (texto o entero)")
            tipo = input(f"{i} --> ")
            
            if tipo.lower() == "texto":
                lista_atributos_tipos.append("TEXT")
                
            elif tipo.lower() == "entero":
                lista_atributos_tipos.append("INTEGER")
                
        os.system('cls' if os.name == 'nt' else 'clear')
        
        
        # Hacer la sentencia para crear la tabla
        sentencia = f"CREATE TABLE IF NOT EXISTS {nombre} ( id INTEGER PRIMARY KEY AUTOINCREMENT"
        
        for i in range(len(lista_atributos)):
            sentencia += f", {lista_atributos[i]} {lista_atributos_tipos[i]}"
        
        sentencia += ");"
        
        # Ejecutar la sentencia
        try:
            cursor.execute(sentencia)
            print(chr(27) + "[32m" + "La tabla se ha creado correctamente." + chr(27) + "[0m")  # Texto en verde

        except sqlite3.Error as e:
            print(chr(27) + "[31m" + f"Error al crear la tabla: {e}" + chr(27) + "[0m")  # Texto en rojo

        
        
        if input("\nQuiéres hacer otra operación (S/N)? ").lower() == "s":
            op = "0"
        else:
            op = "7"
        
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
    elif op == "2": # Eliminar tablas
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("¿Qué tabla desea eliminar?")
        
        x = 0

        for i in tablas:
            x += 1
            
            print(f"    {x}. {tablas[x - 1]}")
            
            
        x = int(input("Ingrese su opción: "))
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        
        try:
            # Ejecutar la consulta para eliminar la tabla
            cursor.execute(f"DROP TABLE IF EXISTS {tablas[x - 1]}")
            
            # Confirmación de que la tabla fue eliminada
            print(chr(27) + "[32m" + f"La tabla '{tablas[x - 1]}' ha sido eliminada correctamente." + chr(27) + "[0m")

        except sqlite3.Error as e:
            # Manejo de errores
            print(chr(27) + "[31m" + f"Error al eliminar la tabla: {e}" + chr(27) + "[0m")
        
        
        if input("\nQuiéres hacer otra operación (S/N)? ").lower() == "s":
            op = "0"
        else:
            op = "7"
        
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
    elif op == "3": # Agregar información
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("¿En que tabla desea insertar información?")
        
        x = 0

        for i in tablas:
            x += 1
            
            print(f"    {x}. {tablas[x - 1]}")
            
            
        x = int(input("Ingrese su opción: "))
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        
        datos = []
        columnas = cursor.execute(f"PRAGMA table_info({tablas[x - 1]})").fetchall()
        comando = f"INSERT INTO {tablas[x - 1]} ("

        # Recopilar los nombres de las columnas y los datos del usuario
        for atributos in columnas:
            datos.append(input(f"{atributos[1].capitalize()}: "))
            comando += f'{atributos[1]}, '

        # Eliminar la última coma y espacio
        comando = comando[:-2]
        comando += ') VALUES ('

        # Añadir los placeholders para los valores
        comando += ', '.join(['?'] * len(columnas))  # Crea una cadena con placeholders
        comando += ')'
        
        
        # Ejecutamos el comando para insertar usando placeholders
        try:
            cursor.execute(comando, datos)  # Pasa los datos como segundo argumento
            print(chr(27) + "[32m" + "Registro insertado correctamente." + chr(27) + "[0m")
        except sqlite3.Error as e:
            print(chr(27) + "[31m" + f"Error al insertar el registro: {e}" + chr(27) + "[0m")
        
        
        
        if input("\nQuiéres hacer otra operación (S/N)? ").lower() == "s":
            op = "0"
        else:
            op = "7"


        os.system('cls' if os.name == 'nt' else 'clear')
        
    elif op == "4":
        os.system('cls' if os.name == 'nt' else 'clear')


        print("¿En que tabla desea consultar información?")
        
        x = 0

        for i in tablas:
            x += 1
            
            print(f"    {x}. {tablas[x - 1]}")

        tbl = int(input("Ingrese su opción: "))


        os.system('cls' if os.name == 'nt' else 'clear')


        # Guardamos los atributos en una variable
        columnas = cursor.execute(f"PRAGMA table_info({tablas[tbl - 1]})").fetchall()
        
        # Guardamos la información en una variable
        resultados = cursor.execute(f"SELECT * FROM {tablas[tbl - 1]}").fetchall()
    
        if resultados: # Comprobamos si hay información
            print(chr(27) + "[32m" + f"Resultados encontrados:" + chr(27) + "[0m")
                
            z = "--------------------------------------------------------------------------\n"
            
            for i in range(len(resultados)):
                z += f"{i + 1}. " 
                
                for j in range(len(columnas)):
                    z += f"{columnas[j][1].capitalize()} = {resultados[i][j]}, "
                
                z = z[:-2]
                z += "\n--------------------------------------------------------------------------\n"
            
            z = z[:-1]
            print(z)
        else:
            print(chr(27) + "[33m" + f"No se encontraron registros." + chr(27) + "[0m")
            

        if input("\nQuiéres hacer otra operación (S/N)? ").lower() == "s":
            op = "0"
        else:
            op = "7"
            
            
        os.system('cls' if os.name == 'nt' else 'clear')
        
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(chr(27) + "[1;31m" + "Opción inválida. Intente nuevamente\n" + chr(27) + "[;m")
        

    if op == "7":
        conexion.commit()
        conexion.close()
        
        sys.exit()




"""
tablas


datos = [
    {"Nombre": "Juan", "Edad": 25},
    {"Nombre": "Luka", "Edad": 18}
]


# Imprimir como una tabla
print(f"{'No.':<5} {'Nombre':<10} {'Edad':<5}")
for i, persona in enumerate(datos, start=1):
    print(f"{i:<5} {persona['Nombre']:<10} {persona['Edad']:<5}")
"""
