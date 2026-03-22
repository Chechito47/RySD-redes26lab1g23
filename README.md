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

## Glosario

Deben completar en el README (o en un archivo referenciado desde él) un **glosario** con definiciones de los conceptos del laboratorio. Incluir al menos: API REST, endpoint, recurso, idempotencia, contrato de API, cobertura de tests, complejidad ciclomática, linters, Docker, health check, timeout, variables de entorno, y los que se mencionan en el enunciado (por ejemplo en "Antes de empezar: conceptos de red"). Agregar además otros términos que les parezcan relevantes para el proyecto.

Deben armar un glosario con de niciones de los conceptos del laboratorio (por ejemplo: API REST, endpoint, recurso, idempotencia,
contrato de API, cobertura de tests, complejidad ciclomática, linters, Docker, health check, timeout, variables de entorno, y los que guren en el
enunciado). Incluir además otros términos que les parezcan relevantes para el proyecto.


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
