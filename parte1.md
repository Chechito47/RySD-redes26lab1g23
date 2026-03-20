## Ejemplo 1 — Búsqueda de entidades en Wikidata
curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=zelda&language=es&format=json | python3 -m json.tool

¿Qué valor aparece en la clave searchinfo.search?
Aparece el valor "zelda"

En la lista search, elegí un resultado que parezca un videojuego: ¿cuál es su id (Q-id), label y description?
Su id (Q-id): "Q12395", label:"The Legend of Zelda", description: "1986 action-adventure video game"


## Ejemplo 2 — Obtener una entidad por ID
curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q12395&format=json&props=labels|descriptions" | python3 -m json.tool

Dentro de entities.<QID>.labels, ¿qué value aparece para el idioma es y para en?
Para el idioma es aparece "The Legend of Zelda"
Para el idioma en aparece "The Legend of Zelda"

Dentro de entities.<QID>.descriptions, ¿qué descripción en es te devuelve para ese juego?
Devuelve "videojuego de 1986" para descripcion en es


## Ejemplo 3 — Búsqueda con otro término y límite
curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=mario&language=es&limit=5&format=json" | python3 -m json.tool

¿Cuántos elementos hay en la lista search cuando usás limit=5?
Hay 5 elementos en la lista search usando ese limite

¿Encontrás en los resultados algún videojuego de la saga Mario? ¿Cuál es su id y su description?
No se encuentra un videojuego en si pero el personaje principal de la saga Mario.
Id (Q-id): "Q12379", description: "fictional character in the Mario video game franchise"


## Ejemplo 4 - Consigna propia.
curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=pokemon&language=en&limit=10&format=json" | python3 -m json.tool

Respuesta:
{
    "searchinfo": {
        "search": "pokemon"
    },
    "search": [
        {
            "id": "Q864",
            "title": "Q864",
            "pageid": 1184,
            "concepturi": "http://www.wikidata.org/entity/Q864",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q864",
            "display": {
                "label": {
                    "value": "Pok\u00e9mon",
                    "language": "en"
                },
                "description": {
                    "value": "Japanese media franchise",
                    "language": "en"
                }
            },
            "label": "Pok\u00e9mon",
            "description": "Japanese media franchise",
            "match": {
                "type": "label",
                "language": "en",
                "text": "Pok\u00e9mon"
            }
        },
        {
            "id": "Q239937",
            "title": "Q239937",
            "pageid": 233264,
            "concepturi": "http://www.wikidata.org/entity/Q239937",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q239937",
            "display": {
                "label": {
                    "value": "Pok\u00e9mon",
                    "language": "en"
                },
                "description": {
                    "value": "Japanese anime television series",
                    "language": "en"
                }
            },
            "label": "Pok\u00e9mon",
            "description": "Japanese anime television series",
            "match": {
                "type": "label",
                "language": "en",
                "text": "Pok\u00e9mon"
            }
        },
        {
            "id": "Q18040230",
            "title": "Q18040230",
            "pageid": 19574063,
            "concepturi": "http://www.wikidata.org/entity/Q18040230",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q18040230",
            "display": {
                "label": {
                    "value": "ZBTB7A",
                    "language": "en"
                },
                "description": {
                    "value": "protein-coding gene in the species Homo sapiens",
                    "language": "en"
                }
            },
            "label": "ZBTB7A",
            "description": "protein-coding gene in the species Homo sapiens",
            "match": {
                "type": "alias",
                "language": "en",
                "text": "pokemon"
            },
            "aliases": [
                "pokemon"
            ]
        },
        {
            "id": "Q3966183",
            "title": "Q3966183",
            "pageid": 3781964,
            "concepturi": "http://www.wikidata.org/entity/Q3966183",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q3966183",
            "display": {
                "label": {
                    "value": "Pok\u00e9mon species",
                    "language": "en"
                },
                "description": {
                    "value": "kind of fictional species from the Pok\u00e9mon franchise",
                    "language": "en"
                }
            },
            "label": "Pok\u00e9mon species",
            "description": "kind of fictional species from the Pok\u00e9mon franchise",
            "match": {
                "type": "label",
                "language": "en",
                "text": "Pok\u00e9mon species"
            }
        },
        {
            "id": "Q20966579",
            "title": "Q20966579",
            "pageid": 23018442,
            "concepturi": "http://www.wikidata.org/entity/Q20966579",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q20966579",
            "display": {
                "label": {
                    "value": "Pok\u00e9mon Go",
                    "language": "en"
                },
                "description": {
                    "value": "augmented reality mobile game based on the Pok\u00e9mon franchise",
                    "language": "en"
                }
            },
            "label": "Pok\u00e9mon Go",
            "description": "augmented reality mobile game based on the Pok\u00e9mon franchise",
            "match": {
                "type": "label",
                "language": "en",
                "text": "Pok\u00e9mon Go"
            }
        },
        {
            "id": "Q24558579",
            "title": "Q24558579",
            "pageid": 26524664,
            "concepturi": "http://www.wikidata.org/entity/Q24558579",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q24558579",
            "display": {
                "label": {
                    "value": "Pok\u00e9mon",
                    "language": "en"
                },
                "description": {
                    "value": "Japanese video game series",
                    "language": "en"
                }
            },
            "label": "Pok\u00e9mon",
            "description": "Japanese video game series",
            "match": {
                "type": "label",
                "language": "en",
                "text": "Pok\u00e9mon"
            }
        },
        {
            "id": "Q1079748",
            "title": "Q1079748",
            "pageid": 1027909,
            "concepturi": "http://www.wikidata.org/entity/Q1079748",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q1079748",
            "display": {
                "label": {
                    "value": "Pok\u00e9mon video games",
                    "language": "en"
                },
                "description": {
                    "value": "video game series",
                    "language": "en"
                }
            },
            "label": "Pok\u00e9mon video games",
            "description": "video game series",
            "match": {
                "type": "label",
                "language": "en",
                "text": "Pok\u00e9mon video games"
            }
        },
        {
            "id": "Q1156046",
            "title": "Q1156046",
            "pageid": 1102353,
            "concepturi": "http://www.wikidata.org/entity/Q1156046",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q1156046",
            "display": {
                "label": {
                    "value": "The Pok\u00e9mon Company",
                    "language": "en"
                },
                "description": {
                    "value": "Japanese brand management, production, and marketing company responsible for marketing and licensing the Pok\u00e9mon franchise",
                    "language": "en"
                }
            },
            "label": "The Pok\u00e9mon Company",
            "description": "Japanese brand management, production, and marketing company responsible for marketing and licensing the Pok\u00e9mon franchise",
            "match": {
                "type": "alias",
                "language": "en",
                "text": "Pok\u00e9mon Company"
            },
            "aliases": [
                "Pok\u00e9mon Company"
            ]
        },
        {
            "id": "Q16773658",
            "title": "Q16773658",
            "pageid": 18376555,
            "concepturi": "http://www.wikidata.org/entity/Q16773658",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q16773658",
            "display": {
                "label": {
                    "value": "Pok\u00e9mon Omega Ruby and Alpha Sapphire",
                    "language": "en"
                },
                "description": {
                    "value": "2014 video game",
                    "language": "en"
                }
            },
            "label": "Pok\u00e9mon Omega Ruby and Alpha Sapphire",
            "description": "2014 video game",
            "match": {
                "type": "label",
                "language": "en",
                "text": "Pok\u00e9mon Omega Ruby and Alpha Sapphire"
            }
        }
    ],
    "search-continue": 9,
    "success": 1
}


Solicite resultados usando "pokemon" para ver si devolvia los juegos, la serie, peliculas, las especie de pokemons, etc.
Y se puede ver varios resultados.
Por ejemplo:
ID (Q-ID): "Q864" es la franquicia japonesa pokemon como nos dice la descripcion: "Japanese media franchise"
ID (Q-ID): "Q239937" es el anime de pokemon, "description": "Japanese anime television series"
ID (Q-ID): "Q20966579" y "Q16773658" son juegos de pokemon (Pokemon GO y Omega Ruby and Alpha Sapphire), description: "augmented reality mobile game based on the Pok\u00e9mon franchise y "2014 video game" respectivamente



