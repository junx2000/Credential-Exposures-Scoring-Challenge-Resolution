
# Credential Exposures Scoring Challenge:

## Introducción:
El equipo de ciberinteligencia nos pide integrar una API de credenciales expuestas y generar un scoring por usuario de acuerdo a los leaks de informacion (explicado mas abajo).

## Detalle del desafio:
Realizar un cliente que consuma la API, traiga todas las alertas y generar un scoring de usuario (mientras más credenciales haya expuesto o más críticas sean esas exposiciones, más alto será su scoring).

Requerimos:

1) Crear un cliente (puede ser una script, una aplicacion con una DB, etc) que se conecte a esta API y guarde la informacion de las alertas.

2) Asignar un scoring por usuario dependiendo de la cantidad de alertas asociadas a su mail y la criticidad de las mismas.
   1) El scoring es un número de 0 a 10.
   2) Las alertas con source malware modifican el scoring automáticamente a 10.
   3) Las alertas de tipo data breach se dividen en 2 niveles de criticidad. Las low suman 1 punto al scoring y las high suman 3.
####
3) Crear alguna forma de saber el scoring dado un usuario. Puede ser una endpoint de una API propia, una DB, o lo que se les ocurra. 

### Documentacion de la api de prueba
Esta es una API que se levanta localmente para hacer la integracion. Corre containerizada en un Docker.

Para buildearla, sobre `/src`:

```
docker build -t challenge-exposure .
```
### Autenticacion

Requiere Autenticacion basica usando el campo `X-API-Key` que se pasa por los headers. 

El token es `XXX-YYY-ZZZ-1234` <small>Nota: Esta hardcodeado porque es una api de prueba, sabemos que asi no se hace ;)</small>

```
X-API-Key: XXX-YYY-ZZZ-1234
```

### Endpoints

Tiene un solo endpoint:
```
GET localhost:9000/alerts
```

El endpoint devuelve alertas paginadas con este formato
```
{
    "alerts": [
        {
            "created_at": "2025-09-17T12:40:33.885198Z",
            "detected_at": "2025-09-17T12:40:25.885198Z",
            "email": "eva.ortiz@email.com",
            "id": "2dfcf5f1-6a1e-407b-9947-de13ad969868",
            "source_info": {
                "severity": "low",
                "source": "data breach"
            }
        },
        {
            "created_at": "2025-09-17T12:56:06.885202Z",
            "detected_at": "2025-09-17T12:55:57.885202Z",
            "email": "karla.alvarez@email.com",
            "id": "19406846-0e99-4c86-8bb8-6a5d28574a9c",
            "source_info": {
                "source": "malware"
            }
        },
        ...
        
    ],
    "page": 1,
    "per_page": 10,
    "total_alerts": 1000,
    "total_pages": 100
}
```

Toma como parametros de query string:
```
page: int El numero de pagina
per_page: int Los resultados por pagina. Hasta 20 resultados por pagina.
```

### Informacion importante

Ocasionalmente devuelve un `429 Throttling Error` si la consultamos muy seguido. Devuelve el tiempo de cooldown/espera para volver a hacer las requests.

Devuleve en el header `Retry-After` la cantidad de segundos que debe esperar para volver a consumir el endpoint


## Opcional Bonus:
Pensar un requerimiento extra que pueda serle útil al equipo de ciberinteligencia.

Además, cualquier herramienta, tecnologia o ideas que implementes, son bienvenidas. Es bienvenido cualquier esfuerzo extra incluido.
Ejemplo: usar una DB, algo que mejore tiempos de procesamiento, algo que haga sencillo la forma de correr, mas robustez, UI, extensibilidad para otras consultas, testing, etc...

## Entregable y Puntos a Evaluar
* Subir la resolución a un repo público.
* Debe de correr containerizado con Docker por lo que se requerira escribir tambien un Dockerfile.
* Escribir documentación del proyecto:
  * Explicación del proyecto
  * Instrucciones de ejecución
  * Pruebas de carga y consulta de información
  * En caso de realizar el punto bonus explicar en qué consiste y por qué decidiste ir por el camino elegido

Vamos a evaluar en base al entregable, principalmente, como solucionaste el problema, como lo pensaste y como lo implementaste. Buscamos profesionales que apunten a la autonomia y resolucion de problemas.

