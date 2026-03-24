"""Cliente Wikidata: búsqueda, obtención por id y población del catálogo local.

Qué es este módulo:
    Integración con la API de Wikidata para buscar y obtener videojuegos (Q7889).
    Los resultados se mapean a un formato común (id, nombre, genero, lanzamiento,
    plataforma, descripcion) y se guardan en store.CATALOGO_JUEGOS.

Para qué sirve:
    - Permitir búsqueda de juegos por texto (GET /juegos?q=...&fuente=wikidata).
    - Resolver un juego por Q-id si no está en catálogo (obtener_juego).
    - Poblar/ampliar el catálogo local con datos de Wikidata, usando
      `store.CATALOGO_JUEGOS` como estructura central (análogo a `store.USUARIOS`
      para los usuarios).

Qué hace:
    - buscar(q): busca en Wikidata, filtra videojuegos, mapea y guarda en catálogo; None si falla API.
    - obtener_juego(juego_id): devuelve juego desde catálogo o Wikidata; None si no existe o falla.
    - listar_o_buscar_juegos: GET /juegos (lista catálogo, búsqueda local o wikidata); 502 si falla Wikidata.
    - obtener_juego_endpoint: GET /juegos/<id>; 404 si no encontrado.

Qué se espera que hagas:
    En el kickstarter las funciones públicas pueden venir con stubs. Implementá
    buscar y obtener_juego usando las helpers _request, _mapear_entidad,
    _obtener_labels, etc., y devolved None cuando la API falle; el endpoint
    debe responder 502 cuando buscar devuelve None.
"""

import logging
import os
import requests
from flask import request, jsonify

from .store import CATALOGO_JUEGOS, _persist_catalogo
from . import filtros

logger = logging.getLogger(__name__)

WIKIDATA_BASE = "https://www.wikidata.org/w/api.php"
WIKIDATA_TIMEOUT = 10
VIDEO_GAME_QID = "Q7889"
LANG = "es"
P_DATE = "P577"
P_GENRE = "P136"
P_PLATFORM = "P400"
P_INSTANCE_OF = "P31"


def _get_user_agent() -> str:
    """Devuelve el User-Agent para las peticiones a Wikidata (env WIKIDATA_USER_AGENT o default)."""
    return os.environ.get("WIKIDATA_USER_AGENT", "LabRedes2026/1.0").strip() or "LabRedes2026/1.0"


def _request(params: dict) -> dict | None:
    """Hace GET a la API de Wikidata con los params dados. Añade format=json y User-Agent.

    Args:
        params: Parámetros de query para w/api.php (action, ids, etc.).

    Returns:
        Dict con la respuesta JSON; None si hay error de red, timeout o JSON inválido.
    """
    params = {**params, "format": "json"}
    headers = {"User-Agent": _get_user_agent()}
    try:
        response = requests.get(
            WIKIDATA_BASE, params=params, headers=headers, timeout=WIKIDATA_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def _extraer_fecha(time_value: str) -> str:
    """Convierte un valor time de Wikidata (ej. +2020-01-15T00:00:00Z) a string YYYY-MM-DD.

    Args:
        time_value: Valor time tal como viene en claims.

    Returns:
        String de fecha (hasta 10 caracteres) o cadena vacía.
    """
    if not time_value:
        return ""
    s = time_value.replace("T00:00:00Z", "").replace("T00:00:00Z", "").strip()
    if s.startswith("+"):
        s = s[1:]
    return s[:10] if len(s) >= 10 else s


def _obtener_labels(qids: list[str]) -> dict[str, str]:
    """Obtiene los labels (nombres) en español o inglés para una lista de Q-ids.

    Args:
        qids: Lista de Q-ids (máx. 50).

    Returns:
        Dict qid -> valor del label (string).
    """
    # Si la lista esta vacia devuelvo lista vacia
    if not qids:
        return {}

    # Traemos los labels en espanol e ingles
    data = _request({"action": "wbgetentities",
                     "ids": "|".join(qids),
                     "props": "labels",
                     "languages": "es|en",
                     })

    # Si _request devuelve None entonces devuelvo None
    if data is None:
        return {}

    # Si no, devuelvo el dict qid -> label
    resultado = {}
    for qid, entidad in data["entities"].items():
        labels = entidad.get("labels", {})
        # Priorizamos espanol
        if "es" in labels:
            resultado[qid] = labels["es"]["value"]
        # Si no hay en espanol usamos ingles
        elif "en" in labels:
            resultado[qid] = labels["en"]["value"]
        # Si no hay ninguno devuelvo string vacio
        else:
            resultado[qid] = ""
    return resultado


def _claim_value_id(claims: dict, prop: str) -> str:
    """Extrae el id (Q-id) del primer claim de una propiedad.

    Args:
        claims: Dict de claims de la entidad.
        prop: Id de propiedad (ej. P136, P400).

    Returns:
        Q-id del valor o cadena vacía.
    """
    if prop not in claims or not claims[prop]:
        return ""
    c = claims[prop][0]
    return c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id", "") or ""


def _claim_value_time(claims: dict, prop: str) -> str:
    """Extrae el valor time del primer claim de una propiedad (ej. P577 fecha lanzamiento).

    Args:
        claims: Dict de claims de la entidad.
        prop: Id de propiedad.

    Returns:
        Valor time (string) o cadena vacía.
    """
    if prop not in claims or not claims[prop]:
        return ""
    c = claims[prop][0]
    return c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time", "") or ""


def _mapear_entidad(ent: dict, labels_cache: dict[str, str]) -> dict:
    """Convierte una entidad Wikidata a dict juego (id, nombre, genero, lanzamiento, plataforma, descripcion).

    Args:
        ent: Entidad tal como viene de wbgetentities.
        labels_cache: Dict Q-id -> label para resolver género y plataforma.

    Returns:
        Dict con id, nombre, genero, lanzamiento, plataforma, descripcion.
    """
    labels = ent.get("labels", {})
    descriptions = ent.get("descriptions", {})
    claims = ent.get("claims", {})
    qid = ent.get("id", "")
    for lang in (LANG, "en"):
        if lang in labels:
            nombre = labels[lang].get("value", "")
            break
    else:
        nombre = ""
    desc = ""
    for lang in (LANG, "en"):
        if lang in descriptions:
            desc = descriptions[lang].get("value", "")
            break
    lanzamiento = _extraer_fecha(_claim_value_time(claims, P_DATE))
    genero_q = _claim_value_id(claims, P_GENRE)
    plataforma_q = _claim_value_id(claims, P_PLATFORM)
    genero = labels_cache.get(genero_q, "") if genero_q else ""
    plataforma = labels_cache.get(plataforma_q, "") if plataforma_q else ""
    return {
        "id": qid,
        "nombre": nombre,
        "genero": genero,
        "lanzamiento": lanzamiento,
        "plataforma": plataforma,
        "descripcion": desc,
    }


def _es_videojuego(ent: dict) -> bool:
    """Indica si la entidad tiene P31=Q7889 (instance of video game).

    Args:
        ent: Entidad Wikidata (con claims).

    Returns:
        True si es videojuego, False si no.
    """
    # P_INSTANCE_OF=P31, {} valor de defecto para diccionario vacio
    return (_claim_value_id(ent.get("claims", {}), P_INSTANCE_OF) == VIDEO_GAME_QID)


def _buscar_ids_wikidata(q: str) -> list[str] | None:
    """Busca entidades en Wikidata por texto y devuelve sus ids.

    Args:
        q: Texto de búsqueda.

    Returns:
        Lista de Q-ids encontrados; None si falla la API; [] si sin resultados.
    """
    # Llamamos a la API de Wikidata con el texto de busqueda
    data = _request({"action": "wbsearchentities",
                     "search": q,
                     "language": LANG
                     })

    # Si _request devuelve None, hubo un error de red o timeout
    if data is None:
        return None

    # Extraemos los ids de cada resultado
    return [entidad["id"] for entidad in data["search"]]


def _filtrar_ids_videojuegos(ids: list[str]) -> list[str] | None:
    """Filtra la lista de ids dejando solo los que son videojuegos (P31=Q7889).

    Args:
        ids: Lista de Q-ids a comprobar.

    Returns:
        Lista de ids que son videojuegos; None si falla la API; [] si ninguno.
    """
    # Traemos los claims para verificar P31=Q7889
    data = _request({"action": "wbgetentities",
                     "ids": "|".join(ids),
                     "props": "claims"
                     })

    # Si _request devuelve None, hubo un error de red o timeout
    if data is None:
        return None

    # Filtramos quedando solo los ids que son videojuegos
    resultado = []
    for qid, entidad in data["entities"].items():
        if _es_videojuego(entidad):
            resultado.append(qid)
    return resultado


def _entidades_completas_videojuegos(video_game_ids: list[str]) -> dict | None:
    """Obtiene entidades completas (labels, descriptions, claims) para los ids dados.

    Args:
        video_game_ids: Lista de Q-ids de videojuegos.

    Returns:
        Dict qid -> entidad; None si falla la API; {} si la lista está vacía.
    """
    # Si la lista esta vacia devuelvo lista vacia
    if not video_game_ids:
        return {}

    # Traemos los labels, descriptions y claims
    data = _request({"action": "wbgetentities",
                     "ids": "|".join(video_game_ids),
                     "props": "labels|descriptions|claims"
                     })

    # Si _request devuelve None entonces devuelvo None
    if data is None:
        return None

    # Si no, devuelvo la lista de entidades
    return data["entities"]


def _colectar_ref_qids(entities: dict) -> set:
    """Extrae los Q-ids de género (P136) y plataforma (P400) de las entidades.

    Args:
        entities: Dict qid -> entidad con claims.

    Returns:
        Set de Q-ids a resolver para labels (genero, plataforma).
    """
    ref_qids = set()
    for ent in entities.values():
        if "missing" in ent:
            continue
        claims = ent.get("claims", {})
        for q in (_claim_value_id(claims, P_GENRE), _claim_value_id(claims, P_PLATFORM)):
            if q:
                ref_qids.add(q)
    return ref_qids


def _mapear_y_guardar_resultados(
    video_game_ids: list[str], entities: dict, labels_cache: dict[str, str]
) -> list[dict]:
    """Mapea entidades a formato juego, las guarda en CATALOGO_JUEGOS y devuelve la lista.

    Args:
        video_game_ids: Orden de ids a incluir.
        entities: Dict qid -> entidad.
        labels_cache: Dict Q-id -> label para género/plataforma.

    Returns:
        Lista de dicts de juegos (id, nombre, genero, etc.); se omiten entidades missing.
    """
    resultados = []
    for qid in video_game_ids:
        ent = entities.get(qid, {})
        if "missing" in ent:
            continue
        ent = dict(ent)
        ent["id"] = qid
        juego = _mapear_entidad(ent, labels_cache)
        CATALOGO_JUEGOS[qid] = juego
        resultados.append(juego)
    _persist_catalogo()
    return resultados


def buscar(q: str) -> list[dict] | None:
    """Busca en Wikidata por texto, filtra videojuegos, mapea y guarda en catálogo.

    Args:
        q: Texto de búsqueda.

    Returns:
        Lista de juegos (dict con id, nombre, genero, etc.); None si falla la API;
        [] si no hay resultados o ninguno es videojuego.
    """
    # Busco ids en Wikidata por texto
    data = _buscar_ids_wikidata(q)
    # Si falla devuelvo None
    if data is None:
        return None

    # Filtro los ids que son de videojuegos
    video_game_ids = _filtrar_ids_videojuegos(data)
    # Si falla devuelvo None
    if video_game_ids is None:
        return None

    # Traigo las entidades completas (labels, descriptions, claims)
    entities = _entidades_completas_videojuegos(video_game_ids)
    # Si falla devuelvo None
    if entities is None:
        return None

    # Recolecto qids de genero y platadormas
    ref_qids = _colectar_ref_qids(entities)

    # Transformo los qids a texto
    labels_cache = _obtener_labels(list(ref_qids))

    # Mapeo y guardo
    return _mapear_y_guardar_resultados(video_game_ids, entities, labels_cache)


def obtener_juego(juego_id: str) -> dict | None:
    """Obtiene un juego por Q-id: primero catálogo local, si no está consulta Wikidata y guarda.

    Args:
        juego_id: Q-id del juego (ej. Q12345).

    Returns:
        Dict del juego (id, nombre, genero, lanzamiento, plataforma, descripcion);
        None si no existe o falla la API.
    """
    # Busco el juego en el catalogo local, si esta lo devuelvo
    if juego_id in CATALOGO_JUEGOS:
        return CATALOGO_JUEGOS[juego_id]

    # Busco la entidad en Wikidata
    entities = _entidades_completas_videojuegos([juego_id])
    # Si falla o no existe devuelvo None
    if not entities or juego_id not in entities:
        return None

    # Resuelvo labels de genero y plataforma
    ref_qids = _colectar_ref_qids(entities)
    # Transformo los qids a texto
    labels_cache = _obtener_labels(list(ref_qids))

    # Mapeo y guardo
    resultados = _mapear_y_guardar_resultados(
        [juego_id], entities, labels_cache)
    # Si no hay resultados devuelvo None
    if not resultados:
        return None
    # Si existe devuelvo el primer resultado
    return resultados[0]


def _obtener_lista_juegos_para_get() -> tuple[list[dict] | None, tuple | None]:
    """Resuelve la lista de juegos para GET /juegos según query params q y fuente.

    Sin q: devuelve todo el catálogo. Con q y fuente=local: filtra por nombre en catálogo.
    Con q y fuente=wikidata: llama a buscar(q); si falla devuelve error 502.

    Returns:
        (lista, None) con la lista de juegos a devolver; o (None, (response, 502)) si falla Wikidata.
    """
    q = request.args.get("q", "").strip()
    fuente = request.args.get("fuente", "local").strip().lower()
    if not q:
        return list(CATALOGO_JUEGOS.values()), None
    if fuente == "wikidata":
        resultados = buscar(q)
        if resultados is None:
            return None, (jsonify({"error": "Error al consultar Wikidata"}), 502)
        return list(resultados or []), None
    q_lower = q.lower()
    return [j for j in CATALOGO_JUEGOS.values() if q_lower in (j.get("nombre") or "").lower()], None


def listar_o_buscar_juegos():
    """Handler GET /juegos: listar catálogo o buscar por q con fuente local o wikidata.

    Query params: q (opcional), fuente (local|wikidata), genero, ordenar, orden.

    Returns:
        Response: JSON con lista de juegos y 200; 502 si fuente=wikidata y falla la API.
    """
    # Obtengo la lista de juegos
    lista, error = _obtener_lista_juegos_para_get()
    # Si hay error devuelvo el error
    if error:
        return error

    # Aplico filtros y ordenamiento
    lista_nueva = filtros.filtrar_y_ordenar(lista, genero=request.args.get("genero"),
                                            ordenar=request.args.get(
                                                "ordenar", "id"),
                                            orden=request.args.get(
                                                "orden", "asc"),
                                            ordenes_validos=filtros.ORDEN_VALIDOS_CATALOGO)

    # Devuelvo la lista de juegos
    return jsonify(lista_nueva), 200


def obtener_juego_endpoint(juego_id: str):
    """Handler GET /juegos/<id>: devuelve un juego por Q-id (catálogo o Wikidata).

    Args:
        juego_id: Q-id del juego.

    Returns:
        Response: JSON del juego y 200; 404 si no encontrado o falla la API.
    """
    # Busco el juego
    juego = obtener_juego(juego_id)
    # Si no existe devuelvo 404
    if juego is None:
        return jsonify({"error": "Juego no encontrado"}), 404
    # Si existe devuelvo el juego y 200
    return jsonify(juego), 200
