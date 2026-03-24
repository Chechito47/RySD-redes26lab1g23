# Parte 5: Integracion con Wikidata
## Comandos usados  
Los comandos usados para testear el funcionamiento fueron:

### Buscar en Wikidata  
**Comando:** `curl "http://localhost:5000/juegos?q=zelda&fuente=wikidata" | python3 -m json.tool`  
**Respuesta:**
```json
[
    {
        "descripcion": "videojuego de 1986",
        "genero": "acci\u00f3n-aventura",
        "id": "Q12395",
        "lanzamiento": "1986-02-21",
        "nombre": "The Legend of Zelda",
        "plataforma": "Game Boy Advance"
    }
]
```

### Ver catalogo local  
**Comando:** `curl "http://localhost:5000/juegos" | python3 -m json.tool`  
**Respuesta:**
```json
[
    {
        "descripcion": "videojuego de 1986",
        "genero": "acci\u00f3n-aventura",
        "id": "Q12395",
        "lanzamiento": "1986-02-21",
        "nombre": "The Legend of Zelda",
        "plataforma": "Game Boy Advance"
    }
]
```

### Obtener juego por id  
**Comando:** `curl "http://localhost:5000/juegos/Q12395" | python3 -m json.tool`  
**Respuesta:**
```json
{
    "descripcion": "videojuego de 1986",
    "genero": "acci\u00f3n-aventura",
    "id": "Q12395",
    "lanzamiento": "1986-02-21",
    "nombre": "The Legend of Zelda",
    "plataforma": "Game Boy Advance"
}
```

### Buscar con ordenacion  
**Comando:** `curl "http://localhost:5000/juegos?ordenar=nombre&orden=asc" | python3 -m json.tool`  
**Respuesta:**
```json
[
    {
        "descripcion": "videojuego de 1986",
        "genero": "acci\u00f3n-aventura",
        "id": "Q12395",
        "lanzamiento": "1986-02-21",
        "nombre": "The Legend of Zelda",
        "plataforma": "Game Boy Advance"
    }
]
```

### Buscar un id que no existe (debe devolver 404)  
**Comando:** `curl "http://localhost:5000/juegos/Q99999999" | python3 -m json.tool`  
**Respuesta:**
```json
{
    "error": "Juego no encontrado"
}
```

---

## Resultados del make test
| Name               | Stmts | Miss | Cover | Missing |
|--------------------|------:|-----:|------:|---------|
| src/__init__.py    | 0     | 0    | 100%  | - |
| src/app.py         | 77    | 16   | 79%   | 77-79, 88, 134-138, 154-157, 234-236 |
| src/auth.py        | 53    | 23   | 57%   | 29-34, 45, 55-61, 72, 79, 84, 90, 99-107 |
| src/auth_common.py | 44    | 17   | 61%   | 35, 43, 48-52, 66, 74, 80-86, 91 |
| src/filtros.py     | 20    | 3    | 85%   | 45, 60, 89 |
| src/juegos.py      | 34    | 20   | 41%   | 47, 60-63, 99-105, 119-123, 138, 153, 166 |
| src/store.py       | 121   | 43   | 64%   | 103-106, 120, 136-137, 174-188, 206, 230, 237-256, 261-268, 273-292, 300-312, 325, 340 |
| src/sugerencias.py | 19    | 11   | 42%   | 39-42, 55-57, 73-76 |
| src/usuarios.py    | 39    | 17   | 56%   | 55, 78-82, 99, 108-114, 135-145 |
| src/wikidata.py    | 173   | 21   | 88%   | 83, 112, 122-126, 141, 157, 181, 255, 276, 336, 359, 365, 389, 406-409, 429-431, 475 |
| **TOTAL**          | **580** | **171** | **71%** | - |

**Required test coverage of 70% reached. Total coverage: 70.52%**  
**21 failed, 18 passed, 2 skipped, 3 warnings, 18 errors**

Como se puede apreciar, ahora tenemos un coverage del 70.52%, superando asi el umbral minimo del 70%