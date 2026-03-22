# PARTE 1
## Ejemplo 1
Comando: `curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=zelda&language=es&format=json" | python3 -m json.tool`  
Valor del campo `searchinfo.search`: **zelda**  
La lista search tiene 7 resultados, el segundo parece un videojuego:
- `id`: Q12395
- `label`: The Legend of Zelda
- `description`: 1986 action-adventure video game

## Ejemplo 2
Comando: `curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q12395&format=json&props=labels|descriptions" | python3 -m json.tool`
- `entities.Q12395.labels` para **es**: The Legend of Zelda
- `entities.Q12395.labels` para **en**: The Legend of Zelda
- `entities.Q12395.description` para **es**: videojuego de 1986

## Ejemplo 3
Comando: `curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=mario&language=es&limit=5&format=json" | python3 -m json.tool`  
En la lista search hay 5 elementos luego de usar `limit=5`  
No hay ningun videojuego de la saga Mario en los resultados

## Busqueda en otro idioma: Minecraft en portugues
`curl -A "LabRedes2026/1.0" "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=minecraft&language=pt&limit=10&format=json" | python3 -m json.tool`  
**Preguntas guia**: Hay resultados correspondientes a videojuegos de la saga Minecraft? Cuantos? Hay alguno que tenga el `label` o `description` en el idioma indicado por el comando?Da un ejemplo  
**Rta**: Hay 5 resultados que son videojuegos de la saga Minecraft. Ninguno de estos tiene el label o description el portugues, todos lo tienen en ingles. Esto es debido a que Wikidata no tiene traducciones al portugues para estos campos, entonces como no encuentra el idioma buscado devuelve por defecto el resultado en ingles.  
Por ejemplo, tomemos Minecraft dungeons:
- **label**: Minecraft Dungeons
- **description**: 2020 video game developed by Mojang and Double Eleven
Para ambos casos sucede **"language": "en"**

Respuesta obtenida:
```json
{
    "searchinfo": {
        "search": "minecraft"
    },
    "search": [
        {
            "id": "Q25445348",
            "title": "Q25445348",
            "pageid": 27398163,
            "concepturi": "http://www.wikidata.org/entity/Q25445348",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q25445348",
            "display": {
                "label": {
                    "value": "Minecraft",
                    "language": "en"
                },
                "description": {
                    "value": "media franchise",
                    "language": "en"
                }
            },
            "label": "Minecraft",
            "description": "media franchise",
            "match": {
                "type": "label",
                "language": "pt",
                "text": "Minecraft"
            }
        },
        {
            "id": "Q49740",
            "title": "Q49740",
            "pageid": 51784,
            "concepturi": "http://www.wikidata.org/entity/Q49740",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q49740",
            "display": {
                "label": {
                    "value": "Minecraft",
                    "language": "en"
                },
                "description": {
                    "value": "2011 video game",
                    "language": "en"
                }
            },
            "label": "Minecraft",
            "description": "2011 video game",
            "match": {
                "type": "label",
                "language": "mul",
                "text": "Minecraft"
            }
        },
        {
            "id": "Q112863331",
            "title": "Q112863331",
            "pageid": 107715615,
            "concepturi": "http://www.wikidata.org/entity/Q112863331",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q112863331",
            "display": {
                "label": {
                    "value": "Minecraft",
                    "language": "en"
                },
                "description": {
                    "value": "video game series",
                    "language": "en"
                }
            },
            "label": "Minecraft",
            "description": "video game series",
            "match": {
                "type": "label",
                "language": "mul",
                "text": "Minecraft"
            }
        },
        {
            "id": "Q40083273",
            "title": "Q40083273",
            "pageid": 41427757,
            "concepturi": "http://www.wikidata.org/entity/Q40083273",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q40083273",
            "display": {
                "label": {
                    "value": "A Minecraft Movie",
                    "language": "en"
                },
                "description": {
                    "value": "2025 film directed by Jared Hess",
                    "language": "en"
                }
            },
            "label": "A Minecraft Movie",
            "description": "2025 film directed by Jared Hess",
            "match": {
                "type": "alias",
                "language": "pt",
                "text": "Minecraft: The Movie"
            },
            "aliases": [
                "Minecraft: The Movie"
            ]
        },
        {
            "id": "Q105729297",
            "title": "Q105729297",
            "pageid": 101090914,
            "concepturi": "http://www.wikidata.org/entity/Q105729297",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q105729297",
            "display": {
                "label": {
                    "value": "Minecraft: Java Edition",
                    "language": "mul"
                },
                "description": {
                    "value": "2011 sandbox game developed by Mojang",
                    "language": "en"
                }
            },
            "label": "Minecraft: Java Edition",
            "description": "2011 sandbox game developed by Mojang",
            "match": {
                "type": "label",
                "language": "mul",
                "text": "Minecraft: Java Edition"
            }
        },
        {
            "id": "Q56884780",
            "title": "Q56884780",
            "pageid": 56801850,
            "concepturi": "http://www.wikidata.org/entity/Q56884780",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q56884780",
            "display": {
                "label": {
                    "value": "Minecraft Dungeons",
                    "language": "en"
                },
                "description": {
                    "value": "2020 video game developed by Mojang and Double Eleven",
                    "language": "en"
                }
            },
            "label": "Minecraft Dungeons",
            "description": "2020 video game developed by Mojang and Double Eleven",
            "match": {
                "type": "label",
                "language": "pt",
                "text": "Minecraft Dungeons"
            }
        },
        {
            "id": "Q63927755",
            "title": "Q63927755",
            "pageid": 63633207,
            "concepturi": "http://www.wikidata.org/entity/Q63927755",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q63927755",
            "display": {
                "label": {
                    "value": "Minecraft Earth",
                    "language": "en"
                },
                "description": {
                    "value": "2019 augmented reality spin-off video game of Minecraft",
                    "language": "en"
                }
            },
            "label": "Minecraft Earth",
            "description": "2019 augmented reality spin-off video game of Minecraft",
            "match": {
                "type": "label",
                "language": "pt",
                "text": "Minecraft Earth"
            }
        },
        {
            "id": "Q20888644",
            "title": "Q20888644",
            "pageid": 22631893,
            "concepturi": "http://www.wikidata.org/entity/Q20888644",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q20888644",
            "display": {
                "label": {
                    "value": "Minecraft: Story Mode",
                    "language": "en"
                },
                "description": {
                    "value": "2015 video game",
                    "language": "en"
                }
            },
            "label": "Minecraft: Story Mode",
            "description": "2015 video game",
            "match": {
                "type": "label",
                "language": "pt",
                "text": "Minecraft: Story Mode"
            }
        },
        {
            "id": "Q125765048",
            "title": "Q125765048",
            "pageid": 119871152,
            "concepturi": "http://www.wikidata.org/entity/Q125765048",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q125765048",
            "display": {
                "label": {
                    "value": "Minecraft",
                    "language": "en"
                },
                "description": {
                    "value": "song by C418",
                    "language": "en"
                }
            },
            "label": "Minecraft",
            "description": "song by C418",
            "match": {
                "type": "label",
                "language": "mul",
                "text": "Minecraft"
            }
        },
        {
            "id": "Q125765049",
            "title": "Q125765049",
            "pageid": 119871153,
            "concepturi": "http://www.wikidata.org/entity/Q125765049",
            "repository": "wikidata",
            "url": "//www.wikidata.org/wiki/Q125765049",
            "display": {
                "label": {
                    "value": "Minecraft",
                    "language": "en"
                },
                "description": {
                    "value": "instrumental track by C418; 2011 studio recording",
                    "language": "en"
                }
            },
            "label": "Minecraft",
            "description": "instrumental track by C418; 2011 studio recording",
            "match": {
                "type": "label",
                "language": "mul",
                "text": "Minecraft"
            }
        }
    ],
    "search-continue": 10,
    "success": 1
}
```

# PARTE 2
Se corrieron los siguientes comandos:
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env`
5. `make docker-build`
6. `make docker-run`
7. `make docker-run` (*Luego se probo con `make run`)
8. `make test`

Los resultados que se obtuvieron del test son:  
Cobertura: 54%  
Tests: 22 fallidos, 17 pasados, 2 skipped, 2 warnings, 18 errors  

Principales tipos de error encontrados:  
- Assert 501: Aparece muchas veces, es el error codigo de error que se devuelve cuando algo no esta implementado
- sqlite3.OperationalError: Intenta escribir en una base de datos la cual solo tiene habilitados los permisos de lectura, probablemente por docker
- Errores de ruff: Librerias importadas pero no usadas, seguramente haya que usarlas a lo largo del laboratorio
