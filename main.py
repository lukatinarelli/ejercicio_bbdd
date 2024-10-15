import os
import sqlite3
import sys
from replit import db
numcolumnas = 0
tablas = db["tablas"]
#db["tablas"] = tablas
basedatos = sqlite3.connect('CreatesBiblio.db')
cursor = basedatos.cursor()

basedatos.execute("INSERT INTO `Autores`(`Nombre`) VALUES ('Pepe')")

#----------------------PRINCIPIO DEL PROGRAMA--------------------------
while True:
  print(
      '***************************\n**Editor de base de datos**\n***************************'
  )
  print(
      '\n¿Qué desea hacer?\n  1. Crear tabla\n  2. Insertar datos\n  3. Consultar datos\n  4. Modificar datos\n  5. Eliminar datos\n  9. Salir\n'
  )

  opcion = input('Ingrese su opción: ')
  os.system('clear')
  #----------------------OPCIÓN 1--------------------------
  if opcion == '1':
    while True:
      p = True
      nombretabla = input('Ingrese el nombre de la tabla: ')
      for i in tablas:
        if nombretabla.lower() == i.lower():
          p = False
          break
      if p:
        break

    while True:
      ncolumnas = input('Ingrese el número de columnas: ')
      if ncolumnas.isnumeric():
        ncolumnas = int(ncolumnas)
        break

    for i in range(ncolumnas):
      while True:
        if i == 0:
          print("ESTA COLUMNA SERÁ INT Y PRIMARY KEY")
        globals()["fila" + str(i)] = input(f'Ingrese el nombre de la columna {i+1}: ')
        if not globals()["fila" + str(i)].isnumeric():
          break
          
      while True:
        if i == 0:
          break
        globals()["tipofila" + str(i)] = input(f'Ingrese el tipo de dato de la columna {i+1} (INT,TEXT,VARCHAR o DATE): ').upper()
        if globals()["tipofila" + str(i)] == "INT" or globals()["tipofila" + str(i)] == "TEXT" or globals()["tipofila" + str(i)] == "VARCHAR" or globals()["tipofila" + str(i)] == "DATE":
          break

    basedatos.execute(f'''CREATE TABLE {nombretabla}({globals()["fila" + str(0)]} INT PRIMARY KEY);''')

    for i in range(1,ncolumnas):
      basedatos.execute(f'''ALTER TABLE {nombretabla} 
ADD {globals()["fila" + str(i)]} {globals()["tipofila"+str(i)].upper()};''')

    tablas.append(nombretabla)
    db["tablas"] = tablas
    os.system('clear')
  #----------------------OPCIÓN 2--------------------------
  elif opcion == '2':
    while True:
      print(
          '¿En que tabla desea insertar datos?\n  1. Alumnos\n  2. Autores\n  3. Libros\n  4. Ejemplares\n  5. Escribe\n  6. Saca\n  7. Volver'
      )

      opcion = input('Ingrese su opción: ')
      os.system('clear')

      if opcion == '1':  #LO ESTOY HACIENDO EN OTRO REPLIT
        print('EN PROGRESO --> lo estoy haciendo en otro replit')

      elif opcion == '2':
        print('2')
        print("--------------------\n Introduzca los siguientes datos:\nNombre y apellido del autor: ")
        nombreautor = input()

      elif opcion == '3':
        print('3')

      elif opcion == '4':
        print('4')

      elif opcion == '5':
        print('5')

      elif opcion == '6':
        print('6')

      elif opcion == '7':
        break

      else:
        print('\x1b[1;31m' + 'Opción inválida. Intente nuevamente.\n' +
              '\x1b[0m')
  #----------------------OPCIÓN 3--------------------------
  elif opcion == '3':
    print('¿En que tabla desea consultar los datos?')

    for i in range(len(tablas)):
      print(f"{i+1}. {tablas[i]}")
      if i+1 == len(tablas):
        print((f"{i+2}. Volver"))

    while True:
      opcion = input('Ingrese su opción: ')
      if opcion.isnumeric():
        if 0<int(opcion) and int(opcion)<len(tablas)+2:
          opcion = int(opcion)
          break

    if opcion != len(tablas)+1:
      tabla = tablas[opcion-1]
      cursor.execute(f"SELECT * FROM {tabla}")
      resultados = cursor.fetchall()
      # Mostrar los resultados
      print("Resultados de la tabla después de la actualización:")
      for fila in resultados:
        print(fila)
      input()
  #----------------------OPCIÓN 4--------------------------
  elif opcion == '4':
    print('¿En que tabla desea modificar datos?')

    for i in range(len(tablas)):
      print(f"{i+1}. {tablas[i]}")
      if i+1 == len(tablas):
        print((f"{i+2}. Volver"))

    while True:
      opcion = input('Ingrese su opción: ')
      if opcion.isnumeric():
        if 0<int(opcion) and int(opcion)<len(tablas)+2:
          opcion = int(opcion)
          break

    if opcion != len(tablas)+1:
      tabla = tablas[opcion-1]
      cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabla}'")
      existe_tabla = cursor.fetchone()
      cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{tabla}'")
      definicion_tabla = cursor.fetchone()[0]

      # Extraer nombres de columnas y tipos de datos
      columnas = []
      for linea in definicion_tabla.split('\n'):
        if 'CREATE TABLE' in linea:
          continue
        if ')' in linea:
          break
        columna = linea.strip().split()[0].replace('"', '').replace("`","")
        tipo = linea.strip().split()[1]
        columnas.append((columna, tipo))

      consulta_update = f"UPDATE {tabla} SET"

      # Mostrar información sobre las columnas
      w = 0
      for columna, tipo in columnas:
        w+=1
        if w == 1:
          continue
        print(f"Columna: {columna}, Tipo: {tipo}")
        nuevo_valor = input(f"VALOR {w-1}: ")
        consulta_update += f" {columna} = '{nuevo_valor}',"

      consulta_update = consulta_update[:-1]
      
      c = input("Quiere usar una condición? (Si/No): ").lower()
      columcondic = ''
      if c == "si":
        while True:
          nc = input("Con cual columna quiere usar la condición? (1-"+str(len(columnas))+"): ")
          if nc.isnumeric() and 0<int(nc) and int(nc)<len(columnas)+1:
            nc = int(nc)
            break
        w = 0
        for columna, tipo in columnas:
          w+=1
          if w == nc:
            columcondic = columna
            break

        condicion = input("A que tiene que ser igual esa columna?: ")
        consulta_update += f"WHERE {columcondic} = {condicion}"
      
      basedatos.execute(consulta_update)

      # Realizar SELECT de toda la tabla
      cursor.execute(f"SELECT * FROM {tabla}")
      resultados = cursor.fetchall()
      input()
      
    os.system('clear')
  #----------------------OPCIÓN 5--------------------------
  elif opcion == '5':
    print('5')
  #----------------------OPCIÓN 9--------------------------
  elif opcion == '9':
    print('9')

    basedatos.commit()
    basedatos.close()

    sys.exit()

  else:
    print('\x1b[1;31m' + 'Opción inválida. Intente nuevamente.\n' + '\x1b[0m')


