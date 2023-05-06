# gestion-agua
Repositorio para el proyecto de gestión de aguas.

## Estructura básica archivos
```
contadores
 ┣ core
 ┃ ┣ controllers
 ┃ ┃ ┣ __init__.py
 ┃ ┃ ┣ contador.py
 ┃ ┃ ┗ lectura.py
 ┃ ┣ models
 ┃ ┃ ┣ __init__.py
 ┃ ┃ ┣ contador.py
 ┃ ┃ ┗ lectura.py
 ┃ ┣ routes
 ┃ ┃ ┣ __init__.py
 ┃ ┃ ┣ contador.py
 ┃ ┃ ┗ lectura.py
 ┃ ┣ __init__.py
 ┃ ┗ prepare_service.py
 ┣ test
 ┃ ┣ controllers
 ┃ ┃ ┣ test_contador.py
 ┃ ┃ ┗ test_lectura.py
 ┃ ┣ models
 ┃ ┃ ┣ test_contador.py
 ┃ ┃ ┗ test_lectura.py
 ┃ ┗ routes
 ┃ ┃ ┣ test_contador.py
 ┃ ┃ ┗ test_lectura.py
 ┗ main.py
```

## Crear imagen
docker build -f dockerfile -t NOMBRE:1 .

## Lanzar contenedor
docker run -dit -p ORIGEN:DESTINO contador:1

## Borrar imágenes que se quedan sueltas
docker rmi $(docker images -f "dangling=true" -q) -f

## Borrar todos los contenedores
docker rm -f $(docker ps -a)
