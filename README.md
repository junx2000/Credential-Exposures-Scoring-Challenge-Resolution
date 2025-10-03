# Credential-Exposures-Scoring-Challenge-Resolution

## Explicación del Proyecto: Credential Exposures Scoring

Este proyecto tiene como objetivo principal consumir una API de alertas de credenciales expuestas, almacenar la información de dichas alertas y generar un scoring por usuario basado en la criticidad de cada exposición. El proyecto fue diseñado para ser containerizado y fácil de desplegar, siguiendo buenas prácticas de desarrollo y considerando escalabilidad y robustez frente a errores de la API.

### Componentes principales

1. Cliente de consumo de API
    - Al iniciar el servicio se invoca reiteradas veces a la API que contiene las alertas hasta traer todas y luego calcula el scoring de cada usuario que posteriormente guarda en la base de datos.
    - Maneja correctamente el rate limiting (429 Throttling Error) respetando el header Retry-After.
    - Se expone: 
        - /scores?email=<email> que permite consultar el scoring de un usuario.
        - /scores que permite consultar todos los scorings de los usuarios.
        - /refresh permite que se actualice completamente el scoring de los usuarios volviendo a traer todas las alertas

2. Base de datos
    - Se utiliza SQLite (por simplicidad y portabilidad) para almacenar el scoring por usuario.

3. Scoring de usuario
    - Se define un score del 0 al 10 basado en la criticidad de las alertas:
        - Alertas con source = "malware" → scoring = 10 inmediatamente.
        - Alertas de tipo data breach:
            - severity = low → +1 punto
            - severity = high → +3 puntos
    - El scoring se calcula sumando los puntos de todas las alertas de un usuario, con un máximo de 10.


Esto facilita la integración con sistemas internos del equipo de ciberinteligencia.

Consideraciones técnicas

Robustez frente a errores: El cliente espera automáticamente el tiempo indicado en Retry-After antes de reintentar en caso de 429.

Escalabilidad: Aunque se usó SQLite, la arquitectura permite fácilmente cambiar a PostgreSQL u otra base de datos si el volumen de alertas crece.

Extensibilidad: Se puede agregar fácilmente nuevos tipos de scoring o fuentes de alertas sin modificar la lógica base.

Containerización: Todo el proyecto corre dentro de Docker, asegurando consistencia entre entornos de desarrollo y producción.

## 🛠️ Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado en tu máquina  

## 🚀 Ejecutar

1. Crear una network:
    ```bash
    docker network create scoring-network
    ```

1. Construir la imagen de la api externa e interna:
   ```bash
   docker build -t  scoring-api-image .
   ```
   ```bash
   docker build -t  scoring-client-image .
   ```

2. Ejecutar ambos contenedores dentro de la red:
    ```bash
    docker run -d   --name scoring-api   --network scoring-network   -p 9000:9000   scoring-api-image
    ```
    ```bash
    docker run -d   --name scoring-client   --network scoring-network   -p 9001:9001   scoring-client-image
    ```

## 🌍 Probar la API

Documentación Swagger UI:
http://localhost:9001/docs

## Bonus:
- Middleware que loggea requests y responses
- Endpoint que permite obtener el scoring de todos los usuarios.

## Posibles mejoras:
- Testing unitario
- Pruebas de estres
- Ordenar los usuarios por score (en el endpoint /score)
- En lugar de hacer de primero traer todas las alertas y luego calcular el score, se puede hacer las dos cosas juntas y en tiempo real se va actualizando el scoring.
- Desplegar contenedores usando docker-compose
- Hacer front que use los endpoints expuestos
