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
    2. Insertar datos
    3. Consultar datos
    4. Modificar datos
    5. Eliminar datos
    6. Salir
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
            op = "6"
        
        
        os.system('cls' if os.name == 'nt' else 'clear')
    elif op == "2": # Agregar información
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("¿En que tabla desea insertar información?")
        
        x = 0

        for i in tablas:
            x += 1
            
            print(f"    {x}. {tablas[x - 1]}")
            
            
        tbl = int(input("Ingrese su opción: "))
        
        
        
        
        
        
        if input("\nQuiéres hacer otra operación (S/N)? ").lower() == "s":
            op = "0"
        else:
            op = "6"


        os.system('cls' if os.name == 'nt' else 'clear')
    elif op == "3":
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
                
            y = 0
            
            for i in range(len(columnas)):
                print(f"{columnas[y][1].capitalize()} = {resultados[0][y]}")
                
                y += 1
        else:
            print(chr(27) + "[33m" + f"No se encontraron registros." + chr(27) + "[0m")
            

        if input("\nQuiéres hacer otra operación (S/N)? ").lower() == "s":
            op = "0"
        else:
            op = "6"
            
            
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(chr(27) + "[1;31m" + "Opción inválida. Intente nuevamente\n" + chr(27) + "[;m")
        

    if op == "6":
        sys.exit()

        conexion.commit()
        conexion.close()



    




    #salida = cursor.execute('''SELECT * FROM cliente''').fetchall() 
    

    #for i in salida: 
        #print(i) 


    
