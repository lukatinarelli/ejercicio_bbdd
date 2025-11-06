> [!WARNING]
> # :construction: Proyecto en construcción :construction:
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
   git clone https://github.com/lukatinarelli/ejercicio_bbdd.git
   cd ejercicio_bbdd

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

## Uso
1. Para iniciar el servidor, ejecuta:
    ```bash
    python main.py

2. Accede a la aplicación: Entra en tu navegador a http://localhost:5000 para acceder a la interfaz gráfica.

3. El programa tiene un login por seguridad. Por defecto, el nombre de usuario es "admin" y la contraseña "password".


Si unicamente quiere usar la interfaz de texto (con menos funcionalidades):
    ```python db_manager.py```


## Tecnologías Utilizadas
 - Python: lenguaje base de la aplicación
 - Flask: framework web para el backend
 - Flask-Login: almacenar el ID del usuario en la sesión y mecanismos para hacer login y logout.
 - SQLite: para la gestión de la base de datos
 - HTML/CSS/JavaScript: para la interfaz de usuario en el frontend


## :hammer:Funcionalidades del proyecto
 - Crear y eliminar bases de datos
 - Importar y exportar bases de datos
 - Crear y eliminar tablas
 - Ver las tablas creadas
 - Modificar tablas ya creadas [EN PROCESO] 
 - Insertar/Consultar/Modificar [EN PROCESO]/Eliminar información de la base de datos
 - Consola para escribir comandos de SQLITE


## Contribución
¡Las contribuciones son bienvenidas! Como este es mi primer proyecto usando HTML/CSS/JavaScript junto con Python, pueden haber varios errores o mejoras posibles. Si encuentras algún error o tienes sugerencias, abre un issue o envía un pull request. Aprecio cualquier ayuda para mejorar el proyecto.
