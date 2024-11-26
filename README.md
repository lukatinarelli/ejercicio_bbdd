# Mi Proyecto de Gestor de Bases de Datos

## Descripción
Este es mi primer proyecto "grande", un gestor de bases de datos que permite a los usuarios realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre sus datos. Además, permite crear y eliminar tablas en la base de datos de forma sencilla. La aplicación incluye:

 - Interfaz gráfica: construida con HTML, CSS y JavaScript para una experiencia de usuario interactiva.
 - Interfaz de texto: implementada en Python para acceder y gestionar los datos mediante comandos directos.

## Tabla de Contenidos
- [Instalación](#instalación)
- [Uso](#uso)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Funcionalidades](#funcionalidades)
- [Contribución](#contribución)


## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/lukatinarelli/gestor_bbdd.git
   cd gestor_bbdd

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

## Uso
1. Para iniciar el servidor, ejecuta:
    ```bash
    python main.py

2. Accede a la aplicación: Entra en tu navegador a http://localhost:5000 para acceder a la interfaz gráfica.


Si unicamente quiere usar la interfaz de texto:
    ```python db_manager.py```


## Tecnologías Utilizadas
 - Python: lenguaje base de la aplicación
 - Flask: framework web para el backend
 - SQLite: para la gestión de la base de datos
 - HTML/CSS/JavaScript: para la interfaz de usuario en el frontend


## Funcionalidades
 - Crear y eliminar bases de datos
 - Importar y exportar bases de datos
 - Crear y eliminar tablas
 - Ver las tablas creadas
 - Editar tablas ya creadas
 - Insertar/Consultar/Modificar/Eliminar información de la base de datos
 - Consola para escribir comandos de SQLITE


## Contribución
¡Las contribuciones son bienvenidas! Como este es mi primer proyecto usando HTML/CSS/JavaScript junto con Python, pueden haber varios errores o mejoras posibles. Si encuentras algún error o tienes sugerencias, abre un issue o envía un pull request. Aprecio cualquier ayuda para mejorar el proyecto.