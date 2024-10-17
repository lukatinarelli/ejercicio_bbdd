import os, sys
import sqlite3

conexion = sqlite3.connect("CreatesBiblio.db")
cursor = conexion.cursor()



os.system('cls' if os.name == 'nt' else 'clear')


while True:
    tablas = [nombre[0] for nombre in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    op = False

    op = input("""¿Qué desea hacer?
    1. Crear tabla
    2. Insertar datos
    3. Consultar datos
    4. Modificar datos
    5. Eliminar datos
    6. Salir
Ingrese su opción: """)


    if op == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        
        nombre = input("¿Qué nombre quiere ponerle a la tabla? ")
        
        
        lista_atributos = []
        lista_atributos_tipos = [] 
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(chr(27) + "[1;31m" + "Recuerda que el nombre de los atributos no puede tener espacios ni acentos." + chr(27) + "[;m")
            atributo = input("Introduce los atributos que quieras de uno en uno (o escribe 'salir' para terminar): ")
            
            if atributo == "salir":
                break 
            
            lista_atributos.append(atributo)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        
        for i in lista_atributos:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("¿Cuál es el tipo de dato de cada atributo? (texto o entero)")
            tipo = input(f"{i} --> ")
            
            if tipo.lower() == "texto":
                lista_atributos_tipos.append("TEXT")
                
            elif tipo.lower() == "entero":
                lista_atributos_tipos.append("INTEGER")
                
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(lista_atributos)
        print(lista_atributos_tipos)
        
        
        
        sentencia = f"CREATE TABLE IF NOT EXISTS {nombre} (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        
        for i in range(len(lista_atributos)):
            sentencia += f"{lista_atributos[i]} {lista_atributos_tipos[i]},"
        
        sentencia += ");"
        
        cursor.execute(sentencia)
        
        
        
        

        input("\nQuiéres hacer otra operación? ")
        
    elif op == "2":
        input()



    elif op == "3":
        os.system('cls' if os.name == 'nt' else 'clear')


        print("En que tabla desea consultar información?")
        
        x = 0

        for i in tablas:
            x += 1
            
            print(f"    {x}. {tablas[x - 1]}")









        input("\nQuiéres hacer otra operación? ")

    elif op == "6":
        sys.exit()

        conexion.commit()
        conexion.close()



    else:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(chr(27) + "[1;31m" + "Opción inválida. Intente nuevamente\n" + chr(27) + "[;m")




    #salida = cursor.execute('''SELECT * FROM cliente''').fetchall() 
    

    #for i in salida: 
        #print(i) 


    
