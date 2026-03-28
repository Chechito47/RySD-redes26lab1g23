# Recomendador de Videojuegos — Laboratorio 1 (2026)

Proyecto base para implementar la API según el contrato en `openapi.yaml`. El archivo **openapi.yaml** define los endpoints; las rutas están registradas en **app.py** y la lógica de cada una se implementa en los módulos de **src/** (usuarios, juegos, sugerencias, wikidata, filtros).

## Integrantes 
- Álvarez, Lis Ailín
- Arndt Kiefer
- Pinilla, Lautaro
- Sabino, Lucas

## Requisitos

- **Docker (recomendado)** para ejecutar la API y el grading sin instalar Python localmente.
- Alternativa: Python 3.10 o superior, venv y `pip install -r requirements.txt`.

## Orden sugerido de trabajo

1. **Configurar entorno y explorar el proyecto:** usá Docker (`make docker-build`, `make docker-run`) o venv y `make run`. Abrí http://localhost:5000/docs, leé el contrato de la API y probá los endpoints (aunque respondan 501). Ejecutá `make test` (o `make grade`) y leé los errores para entender qué esperan los tests. Luego implementá usuarios, lista de juegos, Wikidata y completá tests en `test_private` hasta que `make grade` pase.
2. **Usuarios:** implementar CRUD de usuarios y probar con curl.
3. **Lista de juegos:** implementar lista de juegos por usuario y filtros.
4. **Wikidata:** integrar búsqueda y mapeo desde Wikidata.
5. **Tests y calidad:** completar tests en `test_private` y asegurar que `make grade` (o `make docker-grade`) pase.

## Configuración y uso

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

## Glosario

Deben completar en el README (o en un archivo referenciado desde él) un **glosario** con definiciones de los conceptos del laboratorio. Incluir al menos: API REST, endpoint, recurso, idempotencia, contrato de API, cobertura de tests, complejidad ciclomática, linters, Docker, health check, timeout, variables de entorno, y los que se mencionan en el enunciado (por ejemplo en "Antes de empezar: conceptos de red"). Agregar además otros términos que les parezcan relevantes para el proyecto.

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

## Documentación y Entregables

### Enunciado
Ver **enunciado.md** en esta carpeta para las fases del laboratorio y entregables. La **Parte 1** del enunciado (ejercicios con curl sobre Wikidata) se hace antes o en paralelo; a partir de la **Parte 2** usás este proyecto (configuración, Swagger, implementación).

### Evidencias de Pruebas:
Los resultados de los ejercicios de curl (Parte 1) y las pruebas manuales de la API (Parte 3 en adelante) se encuentran en el archivo [EVIDENCIAS.md](./EVIDENCIAS.md). Además se puede encontrar la reflexión sobre los testeos iniciales. 

### Presentación:
[Link al presentación](http://link.com)]

### Video de Defensa:
[Link al video](http://link.com)

## Metodología de Trabajo
Metodología de trabajo en equipo (cómo se repartieron tareas, revisiones, etc.).

## Estuctura del proyecto 
Breve descripción de los archivos o módulos principales del proyecto.

## Preguntas conceptuales y reflexión
incluir respuestas breves (o un apartado en el README) sobre: qué es una API REST y un contrato de API,
para qué sirven los tests y la cobertura, qué es la complejidad ciclomática y por qué se limita, qué es un linter, para qué sirve Docker en este
proyecto, y cómo realizaron el debugging cuando algo fallaba.

## Decisiones de diseño
qué decisiones de diseño tomaron (por ejemplo estructura de datos, uso de ltros compartidos) y qué problemas
encontraron y cómo los resolvieron.

## Uso de IA y Reflexión Conceptual
ómo utilizaron asistentes de IA (ChatGPT, Copilot, Cursor, etc.) en el proyecto: en qué partes (código, tests,
documentación, debugging), de qué forma (consultas, generación de código, explicaciones) y qué criterios usaron para revisar o adaptar lo
generado. Si no usaron IA, indicarlo explícitamente.
