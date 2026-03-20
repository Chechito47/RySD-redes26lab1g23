# Evidencias de Pruebas - Laboratorio 1: Grupo 23


##  Parte 1: Ejercicios de Wikidata (curl)
### Ejercicio 1: Búsqueda de entidades (Zelda)

**Consigna:** Realizar una búsqueda de la entidad "zelda" en español utilizando el módulo `wbsearchentities`. <br>
``` bash
curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=zelda&language=es&format=json" | python3 -m json.tool
```
**Preguntas Guía:** <br>
- **¿Qué valor aparece en la clave `searchinfo.search`?**: Aparece el valor `"zelda"`. <br>

- **Resultado que parece un videojuego**:
  * **id (Q-id)**: `Q12395`.
  * **label**: `The Legend of Zelda`.
  * **description**: `1986 action-adventure video game`.

### Ejemplo 2: Obtener una entidad por ID
**Consigna:** A partir del ID obtenido en el ejercicio anterior (Q12395), obtener las etiquetas y descripciones en español e inglés utilizando el módulo `wbgetentities`.
``` bash
curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q12395&props=labels|descriptions&languages=es|en&format=json" | python3 -m json.tool` 
```

**Preguntas Guía:**  
* **Dentro de `entities.Q12395.labels`, ¿qué `value` aparece para el idioma `es` y para `en`?**:      
    * Para `es`: `"The Legend of Zelda"`.      
    * Para `en`: `"The Legend of Zelda"`.  
* **Dentro de `entities.Q12395.descriptions`, ¿qué descripción en `es` te devuelve para ese juego?**
    * La descripción en `es` es: `"videojuego de 1986"`.

### Ejemplo 3: Búsqueda con otro término y límite
**Consigna:** Realizar una búsqueda con el término "mario" en español, limitando los resultados a 5 elementos utilizando el parámetro `limit=5`.

```bash
curl -A "LabRedes2026/1.0" "[https://www.wikidata.org/w/api.php?action=wbsearchentities&search=mario&language=es&limit=5&format=json](https://www.wikidata.org/w/api.php?action=wbsearchentities&search=mario&language=es&limit=5&format=json)" | python3 -m json.tool
```
**Preguntas Guía:**
* **¿Cuántos elementos hay en la lista `search` cuando usás `limit=5`?**: Aparecen exactamente 5 elementos en la lista.
* **¿Encontrás en los resultados algún videojuego de la saga Mario? ¿Cuál es su id y su descripción?**: 
    * Sí, se identifica al personaje principal de la franquicia.
    * **ID (Q-id)**: `Q12379`.
    * **Descripción**: `fictional character in the Mario video game franchise`.

### Ejercicio 4:
**Consigna:** Realizar una búsqueda de la entidad "Nintendo" utilizando el idioma japonés (`ja`) y limitando los resultados a 2 elementos para verificar el comportamiento de la API con diferentes parámetros de filtrado.

```bash
curl -A "LabRedes2026/1.0" "[https://www.wikidata.org/w/api.php?action=wbsearchentities&search=nintendo&language=ja&limit=2&format=json](https://www.wikidata.org/w/api.php?action=wbsearchentities&search=nintendo&language=ja&limit=2&format=json)" | python3 -m json.tool
```

**Respuesta Obtenida**

```json
{
    "searchinfo": {
        "search": "nintendo"
    },
    "search": [
        {
            "id": "Q8093",
            "title": "Q8093",
            "pageid": 9373,
            "concepturi": "http://www.wikidata.org/entity/Q8093",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q8093",
            "display": {
                "label": {
                    "value": "Nintendo",
                    "language": "mul"
                },
                "description": {
                    "value": "Japanese multinational video game and consumer electronics company",
                    "language": "en"
                }
            },
            "label": "Nintendo",
            "description": "Japanese multinational video game and consumer electronics company",
            "match": {
                "type": "label",
                "language": "mul",
                "text": "Nintendo"
            }
        },
        {
            "id": "Q170323",
            "title": "Q170323",
            "pageid": 170627,
            "concepturi": "http://www.wikidata.org/entity/Q170323",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q170323",
            "display": {
                "label": {
                    "value": "Nintendo DS",
                    "language": "en"
                },
                "description": {
                    "value": "Nintendo handheld game console",
                    "language": "en"
                }
            },
            "label": "Nintendo DS",
            "description": "Nintendo handheld game console",
            "match": {
                "type": "alias",
                "language": "ja",
                "text": "NINTENDO DS"
            },
            "aliases": [
                "NINTENDO DS"
            ]
        }
    ],
    "search-continue": 2,
    "success": 1
}

```

**Preguntas Guía:**
* **¿Cuál es el valor obtenido en la clave `searchinfo.search`?**: El valor obtenido es `"nintendo"`.
* **¿De qué tratan los dos resultados obtenidos?**: 
    1. El primer resultado (`Q8093`) trata sobre la **empresa multinacional japonesa** de videojuegos y electrónica de consumo.
    2. El segundo resultado (`Q170323`) se refiere específicamente a la **consola portátil** de videojuegos Nintendo DS.
    3. **Observación**: A pesar de solicitar la búsqueda en japonés (`language=ja`), la API devolvió las descripciones en inglés/multilingüe.