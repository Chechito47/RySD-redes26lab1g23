# Recomendador de Videojuegos — Laboratorio 1 (2026)

## Índice
- [Integrantes](#integrantes)
- [Documentación y Entregables](#documentación-y-entregables)
- [Configuración y uso](#configuración-y-uso)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Glosario](#glosario)
- [Autenticación](#autenticación)
- [Metodología de Trabajo](#metodología-de-trabajo)
- [Preguntas conceptuales y reflexión](#preguntas-conceptuales-y-reflexión)
- [Decisiones de diseño](#decisiones-de-diseño)
- [Uso de IA y Reflexión Conceptual](#uso-de-ia-y-reflexión-conceptual)

## Integrantes 
- Álvarez, Lis Ailín
- Arndt Kiefer
- Pinilla, Lautaro
- Sabino, Lucas

## Documentación y Entregables

### Enunciado
Ver **enunciado.md** en esta carpeta para las fases del laboratorio y entregables. La **Parte 1** del enunciado (ejercicios con curl sobre Wikidata) se hace antes o en paralelo; a partir de la **Parte 2** usás este proyecto (configuración, Swagger, implementación).

### Evidencias de pruebas y comandos (por parte)
Las evidencias de curl, pruebas manuales y resultados parciales del laboratorio se documentan en:

- **Parte 1 (Wikidata con curl + reflexión inicial):** [EVIDENCIAS.md](./EVIDENCIAS.md)
- **Parte 3 (usuarios):** [Comandos parte 3.md](./Comandos%20parte%203.md)
- **Parte 4 (listas de juegos):** [Comandos parte 4.md](./Comandos%20parte%204.md)
- **Parte 5 (integración con Wikidata):** [Parte 5.md](./Parte%205.md)
- **Parte 6 (autenticación y sugerencias con curl):** [Comandos parte 6.md](./Comandos%20parte%206.md)

### Presentación:
[Link al presentación](https://canva.link/4mj3n29u3drpuix)

### Video de Defensa:
[Link al video](http://link.com)

## Configuración y uso

### Requisitos

- **Docker (recomendado)** para ejecutar la API y el grading sin instalar Python localmente.
- Alternativa: Python 3.10 o superior, venv y `pip install -r requirements.txt`.

### Con Docker (recomendado)

```bash
make docker-build
make docker-run
```

Con la API corriendo, abrí **http://localhost:5000/docs**. Para verificar tests, cobertura, lint y complejidad sin tener Python local:

```bash
make docker-grade
```

Necesitás un archivo `.env` en la raíz (copiá desde `.env.example`). Los datos se persisten en SQLite (por defecto `instance/datos.db`). Para volver a empezar con datos vacíos: `make clean-db`.

### Alternativa con venv

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Opcional: WIKIDATA_USER_AGENT para llamadas a Wikidata
make run
```
Si no usás make: `PYTHONPATH=. python3 -m src.app`.

- `make test` — Ejecuta los tests
- `make grade` — Ejecuta el script de grading (tests + cobertura + lint + complejidad)
- `make lint` — Ruff y radon
- `make clean-db` — Borra la base SQLite para empezar de cero con datos vacíos

Los tests en **test_metrics.py** comprueban estilo (ruff) y complejidad ciclomática; si fallan, corregir el código en **src/** (refactorizar funciones demasiado largas o con muchas ramas).

## Estructura del proyecto
El proyecto mantiene la estructura del **kickstarter** de la cátedra y separa la implementación por responsabilidad:

- **openapi.yaml**: contrato formal de la API (métodos, rutas, cuerpos, respuestas y esquemas). Es la referencia principal de comportamiento.
- **src/app.py**: punto de entrada de Flask; registra rutas, documentación (`/docs`, `/openapi.yaml`) y `health check` (`/health`).
- **src/store.py**: capa de persistencia en SQLite y estructuras compartidas (usuarios, credenciales, catálogo y listas).
- **src/usuarios.py**: endpoints de CRUD de usuarios.
- **src/juegos.py**: endpoints de lista de juegos por usuario (agregar, listar, actualizar y eliminar) con filtros y orden.
- **src/sugerencias.py**: endpoint de sugerencia aleatoria entre juegos que el usuario tiene (con filtro opcional por género).
- **src/wikidata.py**: integración con API externa (Wikidata), mapeo de datos y carga/consulta del catálogo local.
- **src/filtros.py**: lógica compartida de filtrado y ordenamiento para listados.
- **src/auth.py** y **src/auth_common.py**: autenticación básica (registro/login), hashing de contraseñas, tokens y expiración.

En pruebas y validación:

- **tests/test_public/**: tests provistos por la cátedra para validar contrato y comportamiento esperado.
- **tests/test_private/**: tests implementados por el grupo (casos borde, filtros, sugerencia por género).
- **tests/conftest.py**: fixtures y configuración común de pytest.
- **grade.py**: evaluación automática integral (tests, cobertura, lint y complejidad ciclomática).
- **Makefile**: comandos para ejecutar API, tests y grading (`run`, `test`, `grade`, `docker-*`).
- **EVIDENCIAS.md** y archivos de comandos por parte: evidencia de pruebas manuales con `curl`.

## Glosario

* **API REST:** Arquitectura de red basada en recursos identificables por URL, que utiliza una comunicación sin estado (stateless).
* **Contrato de API:** Especificación formal (en este caso, OpenAPI/openapi.yaml) que define los métodos, rutas, cuerpos y respuestas esperadas de la aplicación.
* **Recurso:** Entidad identificada por una URL (por ejemplo, un usuario o una lista de juegos) sobre la cual se aplican operaciones REST.
* **Endpoint:** URL o ruta específica que expone una operación de la API, combinando un método HTTP con un path (ej. GET /usuarios).
* **Idempotencia:** Propiedad de una operación que, al ser ejecutada varias veces, produce el mismo resultado que si se ejecutara una sola vez (ej. GET o PUT).
* **Cobertura de tests:** Porcentaje de líneas de código en `src/` que son efectivamente ejecutadas por los tests automatizados; se exige un mínimo del 70%.
* **Complejidad Ciclomática:** Medida del número de caminos independientes que puede seguir una función; en este proyecto el límite máximo es 8 por función.
* **Linters (Ruff):** Herramientas que analizan el código de forma estática (sin ejecutarlo) para detectar errores de estilo, bugs potenciales o malas prácticas.
* **Docker:** Plataforma de contenedores que permite empaquetar la aplicación y sus dependencias para asegurar que se ejecute de la misma forma en cualquier entorno.
* **Health Check:** Endpoint especial (`/health`) utilizado para monitorear que el servidor está levantado y funcionando correctamente.
* **Timeout:** Límite de tiempo máximo que nuestra API espera una respuesta de un servicio externo (como Wikidata) antes de cortar la conexión para no bloquearse indefinidamente.
* **Variables de Entorno:** Valores configurables fuera del código (generalmente en un archivo `.env`) que permiten modificar el comportamiento de la app según el entorno.
* **Hashing de contraseñas:** Proceso criptográfico de una sola vía que transforma una contraseña en una cadena de caracteres irreconocible antes de guardarla en la base de datos.
* **Salt:** Semilla aleatoria única que se mezcla con la contraseña antes del hasheo para evitar que dos usuarios con la misma clave tengan el mismo hash almacenado.
* **Token Opaco:** Identificador único generado al hacer login que sirve como prueba de identidad en peticiones posteriores sin necesidad de enviar la contraseña cada vez.
* **TTL (Time To Live):** Tiempo de vida definido para un token; una vez superado este lapso, el token se considera vencido y la API debe rechazarlo con un error 401.

## Autenticación

### 1) Hashing de contraseñas

La API implementa hashing de contraseñas con **werkzeug.security** para evitar almacenamiento en texto plano.

- En `POST /auth/registro`, la contraseña recibida se transforma con `generate_password_hash(...)` antes de persistirse en `password_hash`.
- En `POST /auth/login`, la validación se realiza con `check_password_hash(...)` contra el hash almacenado.

El algoritmo no solo hashea la clave, sino que genera un "Salt" (una semilla aleatoria única) para cada usuario. Al iniciar sesión, la API recibe la contraseña en texto plano y utiliza check_password_hash para extraer el Salt del hash almacenado y aplicarlo a la clave recibida. Si el nuevo resultado coincide con el registro de la base de datos, se valida la identidad del usuario sin haber guardado nunca la contraseña original.

### 2) Expiración de tokens

Para el login, el backend arma un token y le pone una fecha de vencimiento en UTC sumando los minutos que se definen en la variable AUTH_TOKEN_TTL_MINUTES (por defecto, 60 minutos) a la hora actual. Esa fecha se guarda como token_expira_en en la base de datos.

Después, cuando se quiere utilizar ese token, el sistema chequea que no esté vencido comparándolo con la hora actual. Si el token no existe, está mal formateado o ya pasó la hora de vencimiento, la API devuelve un 401 (No autorizado) y no continúa.

### 3) Guía rápida con curl

#### Registrar usuario (`POST /auth/registro`)

```bash
curl -X POST http://localhost:5000/auth/registro \
    -H "Content-Type: application/json" \
    -d '{
        "username": "lisalv",
        "nombre": "Lis",
        "password": "pass123"
    }'
```

#### Login para obtener token (`POST /auth/login`)

```bash
curl -X POST http://localhost:5000/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "username": "lisalv",
        "password": "pass123"
    }'
```

Respuesta esperada (ejemplo):

```json
{"token":"<TOKEN>"}
```

#### Usar token en header `Authorization: Token <TOKEN>`

Ejemplo de request con token:

```bash
curl -X GET http://localhost:5000/usuarios/1/juegos \
    -H "Authorization: Token <TOKEN>"
```

Ejemplo en endpoint protegido (requiere token válido del mismo usuario):

```bash
curl -X PUT http://localhost:5000/usuarios/1 \
    -H "Content-Type: application/json" \
    -H "Authorization: Token <TOKEN>" \
    -d '{"nombre":"Lis Actualizada"}'
```

Para endpoints protegidos de modificación (por ejemplo `PUT/DELETE /usuarios/<id>` y `POST/PUT/DELETE /usuarios/<id>/juegos...`), si falta token, es inválido, está vencido o no corresponde al mismo `<id>`, la API responde **401**.

## Metodología de Trabajo
Como hubo dos entregas (parcial y final), nos organizamos de forma equitativa en las Partes 4 a 7, en lugar de seguir estrictamente el orden sugerido por la cátedra. En la etapa parcial, cada integrante realizó pruebas y configuraciones iniciales para que todos nos familiarizáramos con la app, y luego integramos una versión común en `main` para entregar. Mantuvimos la coordinación por un grupo privado de WhatsApp, donde fuimos repartiendo pendientes, avisando avances y pidiendo ayuda cuando alguien se trababa. Antes de la entrega final hicimos una reunión de integración para validar que todo funcionara en cada computadora y despejar dudas de trabajos que realizó otro compañero. El flujo de trabajo fue crear una rama por funcionalidad y luego mergear a `main` tras revisión interna. Como mejora a futuro, proponemos formalizar este proceso con pull requests y aprobaciones.

## Preguntas conceptuales y reflexión

* **¿Qué es una API REST y un contrato de API?** Una API REST es un estilo de arquitectura para sistemas distribuidos basado en el protocolo HTTP, donde los recursos (como usuarios o juegos) se manipulan mediante métodos estándar (GET, POST, PUT, DELETE). El **contrato de API** (en este proyecto, el `openapi.yaml`) es el documento que define las reglas: qué rutas existen, qué datos deben enviarse y qué respuestas esperar, permitiendo que el backend y el frontend trabajen de forma sincronizada.

* **¿Para qué sirven los tests y la cobertura?** Los tests sirven para asegurar que el código hace lo que debe y para detectar errores rápidamente al hacer cambios (regresiones). La **cobertura** mide qué porcentaje de nuestro código está siendo verificada por esos tests.

* **¿Qué es la complejidad ciclomática y por qué se limita?** Es una métrica que cuenta la cantidad de caminos lógicos posibles (ifs, loops, excepciones) dentro de una función. Se limita (en este caso a 8) para forzarnos a escribir funciones simples, fáciles de testear y de mantener.

* **¿Qué es un linter?** Es una herramienta de análisis estático que revisa el código sin ejecutarlo para encontrar errores de estilo, variables sin usar o posibles bugs, asegurando que todo el equipo mantenga un mismo estándar de prolijidad.

* **¿Para qué sirve Docker en este proyecto?** Docker nos permite empaquetar la aplicación con todas sus dependencias (Python, librerías, etc.) en un contenedor. Esto garantiza que la API funcione exactamente igual cualquier computadora que lo ejecute.

* **¿Cómo realizaron el debugging cuando algo fallaba?** Utilizamos principalmente el **logging** del sistema para rastrear el flujo de las peticiones en la terminal. Cuando un test fallaba, revisamos los mensajes de error en la terminal y se investigaba y corregía la fuente.

## Decisiones de diseño
- Centralizamos los datos en `store.py` (usuarios, listas, catálogo y credenciales) para evitar duplicación de lógica entre módulos.
- Reutilizamos `filtros.py` para resolver filtrado y ordenamiento en un solo lugar, manteniendo comportamiento consistente en los endpoints.
- En autenticación, priorizamos una solución simple pero segura para el laboratorio: hash de contraseñas y tokens con expiración.

El principal problema fue compatibilizar los tests con la modificación de autenticación; por un error de lectura de consigna se habían modificado tests públicos, pero luego en esta última versión se corrigió el problema y se volvieron los tests a su estado original, otorgados por la cátedra. 

## Uso de IA y Reflexión Conceptual
Cada integrante usó asistentes de IA de forma distinta. El uso más frecuente fue para generar y revisar tests, además de resolver dudas puntuales sobre el código y repasar conceptos teóricos. También se utilizó para proponer fragmentos de implementación, pero siempre con doble chequeo: verificamos que la solución cumpliera la consigna, fuera clara, no agregara complejidad innecesaria y mantuviera una estructura modular.

Además, la IA se usó como apoyo para mejorar redacciones de este README. En esos casos, primero se escribe el contenido base y luego pedimos sugerencias para pulir claridad y organización, y como siempre, revisar el resultado final y hacer las correcciones pertinentes.  