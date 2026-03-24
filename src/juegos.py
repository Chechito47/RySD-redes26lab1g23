"""Lista de juegos por usuario: agregar, listar, actualizar y eliminar ítems; filtros y ordenación.

Qué es este módulo:
    Implementa los endpoints de la lista de juegos de cada usuario: GET/POST
    /usuarios/<id>/juegos y GET/PUT/DELETE /usuarios/<id>/juegos/<juego_id>.
    Cada ítem referencia un juego del catálogo (por juego_id, Q-id de Wikidata)
    y tiene flags: tengo, quiero, jugado, me_gusta, más fecha_agregado.

Para qué sirve:
    Permite que cada usuario tenga su propia lista de videojuegos con estado
    (lo tengo, lo quiero, lo jugué, me gusta). La lista se filtra y ordena
    según query params (genero, ordenar, orden).

Qué hace:
    - listar_juegos_usuario: devuelve la lista enriquecida con datos del catálogo; acepta genero, ordenar, orden.
    - agregar_juego_usuario: agrega un juego por juego_id (debe existir en catálogo o Wikidata); 409 si ya está.
    - actualizar_juego_usuario: actualiza los flags del ítem; 404 si el juego no está en la lista.
    - eliminar_juego_usuario: quita el juego de la lista; 404 si no está.

Qué se espera que hagas:
    En el kickstarter las funciones vienen con stubs. Implementá la lógica
    usando store.LISTAS_JUEGOS, store.CATALOGO_JUEGOS, wikidata.obtener_juego
    y filtros.filtrar_y_ordenar. Respetá los códigos 400, 404, 409 del contrato.
    Podés tomar como referencia el endpoint de ejemplo `crear_usuario` en
    `src/usuarios.py` para ver cómo se actualizan estructuras de `store`
    y se persisten los cambios antes de devolver la respuesta JSON.
"""

from datetime import datetime, timezone
from flask import request, jsonify

from .store import USUARIOS, LISTAS_JUEGOS, CATALOGO_JUEGOS, _persist_listas, _persist_catalogo
from .filtros import ORDEN_VALIDOS_LISTA
from . import wikidata
from . import filtros


def _lista_usuario(usuario_id: int):
    """Devuelve la lista de ítems del usuario o None si el usuario no existe.

    Args:
        usuario_id: Id del usuario.

    Returns:
        Lista de ítems (dict con juego_id, tengo, quiero, jugado, me_gusta, fecha_agregado)
        o None si el usuario no existe.
    """

    usuario = any(u["id"] == usuario_id for u in USUARIOS)

    if not usuario:
        return None # Retorna 404 si el usuario no existe

    # Retorna la lista del usuario, si no tiene retorna []
    return LISTAS_JUEGOS.get(usuario_id, [])


def _enriquecer_item(item: dict) -> dict | None:
    """Combina un ítem de la lista (juego_id + flags) con los datos del juego en el catálogo.

    Args:
        item: Dict con juego_id, tengo, quiero, jugado, me_gusta, fecha_agregado.

    Returns:
        Dict con todos los campos del juego (id, nombre, genero, etc.) más los flags;
        None si el juego_id no está en el catálogo.
    """
    juego = CATALOGO_JUEGOS.get(item["juego_id"])
    if not juego:
        return None
    return {
        "id": item["juego_id"],
        "nombre": juego.get("nombre", ""),
        "genero": juego.get("genero", ""),
        "lanzamiento": juego.get("lanzamiento", ""),
        "plataforma": juego.get("plataforma", ""),
        "descripcion": juego.get("descripcion", ""),
        "tengo": item.get("tengo", False),
        "quiero": item.get("quiero", False),
        "jugado": item.get("jugado", False),
        "me_gusta": item.get("me_gusta", False),
        "fecha_agregado": item.get("fecha_agregado", ""),
    }


def listar_juegos_usuario(usuario_id: int):
    """Lista los juegos del usuario con filtro y ordenación; enriquecidos con datos del catálogo.

    Query params: genero (opcional), ordenar (nombre, fecha_lanzamiento, fecha_agregado), orden (asc, desc).

    Args:
        usuario_id: Id del usuario.

    Returns:
        Response: JSON con lista de juegos (cada uno con id, nombre, flags, etc.) y 200;
        404 si el usuario no existe.
    """
    
    # Obtener la lista y valido existencia del usuario
    lista = _lista_usuario(usuario_id)

    if lista is None:
        return jsonify({"error": "usuario no encontrado"}), 404
    
    # Uso la funcion _enriquecer_item para enriquecer cada item de la lista 
    lista_enriquecida = []
    for item in lista:
        item_completo = _enriquecer_item(item)
        if item_completo:
            lista_enriquecida.append(item_completo)

    # Obtener los query params
    genero = request.args.get("genero")
    ordenar = request.args.get("ordenar", "nombre")
    orden = request.args.get("orden", "asc")

    # Aplico los filtros y el orden 
    resultado = filtros.filtrar_y_ordenar(
        lista_enriquecida,
        genero = genero,
        ordenar = ordenar,
        orden = orden,
        ordenes_validos = ORDEN_VALIDOS_LISTA
    )

    return jsonify(resultado), 200

def _validar_body_agregar_juego():
    """Valida el body JSON de POST para agregar juego.

    Returns:
        (error_response, None) si hay error (400); (None, (juego_id, req)) si es válido.
    """
    if not request.json:
        return (jsonify({"error": "Datos inválidos"}), 400), None
    req = request.json
    for key in ("juego_id", "tengo", "quiero", "jugado", "me_gusta"):
        if key not in req:
            return (jsonify({"error": f"Datos inválidos: falta {key}"}), 400), None
    return None, (str(req["juego_id"]).strip(), req)


def _lista_y_existente(usuario_id: int, juego_id: str) -> tuple[list[dict] | None, dict | None]:
    """Obtiene la lista del usuario y el ítem existente (si el juego ya está en la lista).

    Args:
        usuario_id: Id del usuario.
        juego_id: Q-id del juego.

    Returns:
        (lista, item_existente). lista es None si el usuario no existe;
        item_existente es el dict del ítem si ya está en la lista, sino None.
    """
    if next((u for u in USUARIOS if u["id"] == usuario_id), None) is None:
        return None, None
    lista = LISTAS_JUEGOS.setdefault(usuario_id, [])
    existente = next((i for i in lista if i["juego_id"] == juego_id), None)
    return lista, existente


def agregar_juego_usuario(usuario_id: int):
    """Agrega un juego a la lista del usuario. El juego debe existir en catálogo o Wikidata.

    Request body (JSON): juego_id (str), tengo, quiero, jugado, me_gusta (bool).

    Args:
        usuario_id: Id del usuario.

    Returns:
        Response: JSON del ítem creado (enriquecido) y 201; 400 si falta campo, 404 si usuario
        o juego no existe, 409 si el juego ya está en la lista.
    """

    # Valido el body
    valid_body, datos = _validar_body_agregar_juego()
    if valid_body:
        return valid_body # Devuelve jsonify con 404
    
    juego_id, req = datos
    
    # Obtengo la lista y veo si el juego ya existe
    lista, existe = _lista_y_existente(usuario_id, juego_id)

    if lista is None:
        return jsonify({"error": "Usuario no encotrado"}), 404

    if existe:
        return jsonify({"error": "El juego ya esta en la lista"}), 409

    # Chequeo existencia del juego en el catalogo local o wikidata
    info_juego = CATALOGO_JUEGOS.get(juego_id)

    # Si no esta local chequeo en wikidata
    if not info_juego:
        info_juego = wikidata.obtener_juego(juego_id)
        if not info_juego:
            return jsonify({"error": "Juego no encontrado en el catalogo ni wikidata"}), 404
        
        # Si wikidata lo encontro, lo guado en el catalogo local para el futuro
        CATALOGO_JUEGOS[juego_id] = info_juego
    
    # Creo el nuevo item para la lista del usuario
    nuevo_item = {
        "juego_id": juego_id,
        "tengo": bool(req.get("tengo", False)),
        "quiero": bool(req.get("quiero", False)),
        "jugado": bool(req.get("jugado", False)),
        "me_gusta": bool(req.get("me_gusa", False)),
        "fecha_agregado": datetime.now(timezone.utc).isoformat()
    }

    # Persistencia
    lista.append(nuevo_item)
    _persist_listas()
    _persist_catalogo()

    return jsonify(_enriquecer_item(nuevo_item)), 201



def actualizar_juego_usuario(usuario_id: int, juego_id: str):
    """Actualiza los flags (tengo, quiero, jugado, me_gusta) de un ítem de la lista.

    Args:
        usuario_id: Id del usuario.
        juego_id: Q-id del juego en la lista.

    Request body (JSON): campos opcionales tengo, quiero, jugado, me_gusta (bool).

    Returns:
        Response: JSON del ítem actualizado y 200; 404 si usuario o juego en lista no existe.
    """
    
    lista, existente = _lista_y_existente(usuario_id, juego_id)

    if lista is None:
        return jsonify({"error": "Usuario no enconrtado"}), 404
    if not existente:
        return jsonify({"error": "El juego no esta en la lista del usuario"}), 404
    
    if not request.json:
        return jsonify({"error": "Datos invalidos"}), 400

    req = request.json

    # Actualizar solo los campos que vengan en el json
    existente["tengo"] = bool(req.get("tengo", existente.get("tengo", False)))
    existente["quiero"] = bool(req.get("quiero", existente.get("quiero", False)))
    existente["jugado"] = bool(req.get("jugado", existente.get("jugado", False)))
    existente["me_gusta"] = bool(req.get("me_gusta", existente.get("me_gusta", False)))

    # Persistir
    _persist_listas()

    return jsonify(_enriquecer_item(existente)), 200


def eliminar_juego_usuario(usuario_id: int, juego_id: str):
    """Elimina un juego de la lista del usuario.

    Args:
        usuario_id: Id del usuario.
        juego_id: Q-id del juego a quitar de la lista.

    Returns:
        Response: JSON con mensaje de éxito y 200; 404 si usuario o juego en lista no existe.
    """
    lista, existente = _lista_y_existente(usuario_id, juego_id)
    
    if lista is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    if not existente:
        return jsonify({"error": "El juego no está en la lista del usuario"}), 404

    # 3. Eliminar el ítem de la lista
    lista.remove(existente)

    _persist_listas()

    return jsonify({"mensaje": "Juego eliminado de la lista"}), 200