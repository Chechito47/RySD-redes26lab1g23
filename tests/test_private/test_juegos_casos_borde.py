"""Tests que debés implementar: casos borde de la lista de juegos."""
import pytest
from conftest import JUEGO_TEST_ID

JUEGO_OTRO_ID = "Q99998"  # id distinto para tests con dos juegos


@pytest.fixture
def usuario_auth(auth_user):
    """Crea un usuario autenticado y devuelve id + headers."""
    return auth_user(nombre="UsuarioBorde")


# ── 1. POST sin campo obligatorio → 400 ─────────────────────────────────────

def test_agregar_juego_falta_campo_obligatorio_400(client, usuario_auth):
    """POST /usuarios/<id>/juegos sin 'juego_id' debe devolver 400."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]

    # Body intencionalmente sin juego_id
    body = {
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    resp = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=headers)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


# ── 2. PUT con juego_id que no está en la lista → 404 ───────────────────────

def test_actualizar_juego_id_inexistente_404(client, usuario_auth):
    """PUT /usuarios/<id>/juegos/Q99999 con juego no en lista debe devolver 404."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]

    resp = client.put(
        f"/usuarios/{usuario_id}/juegos/Q99999",
        json={"jugado": True},
        headers=headers,
    )
    assert resp.status_code == 404
    assert "error" in resp.get_json()


# ── 3. DELETE con juego no en la lista → 404 ────────────────────────────────

def test_eliminar_juego_no_en_lista_404(client, usuario_auth):
    """DELETE /usuarios/<id>/juegos/<juego_id> con juego no en lista debe devolver 404."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]

    resp = client.delete(
        f"/usuarios/{usuario_id}/juegos/{JUEGO_TEST_ID}",
        headers=headers,
    )
    assert resp.status_code == 404
    assert "error" in resp.get_json()


# ── 4. POST con juego_id que no existe en catálogo ni Wikidata → 404 ────────

def test_agregar_juego_id_inexistente_404(client, usuario_auth, rawg_mock):
    """POST con juego_id que no existe en catálogo ni Wikidata debe devolver 404."""
    from src import store

    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]

    juego_id = "QINEXISTENTE"
    store.CATALOGO_JUEGOS.pop(juego_id, None)

    rawg_mock.get(
        "https://www.wikidata.org/w/api.php",
        json={"entities": {}},
    )

    body = {
        "juego_id": juego_id,
        "tengo": False,
        "quiero": True,
        "jugado": False,
        "me_gusta": False,
    }
    resp = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=headers)
    assert resp.status_code == 404
    assert "error" in resp.get_json()

# ── 5. GET con ordenar=fecha_lanzamiento devuelve lista ordenada ─────────────

def test_ordenar_por_fecha_lanzamiento(client, usuario_auth, rawg_mock):
    """GET ?ordenar=fecha_lanzamiento devuelve juegos ordenados por fecha de lanzamiento."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]

    # Poblar catálogo con dos juegos que tienen fechas distintas:
    # JUEGO_TEST_ID (Q12395) → lanzamiento "1986-02-21" (según mock de búsqueda)
    # JUEGO_OTRO_ID (Q99998) → lanzamiento "2017-03-03" (según _entity_for_id del mock)
    client.get("/juegos?q=zelda&fuente=wikidata")         # carga Q12395
    client.get(f"/juegos/{JUEGO_OTRO_ID}")                # carga Q99998

    body_base = {"tengo": True, "quiero": False, "jugado": False, "me_gusta": False}

    r1 = client.post(
        f"/usuarios/{usuario_id}/juegos",
        json={**body_base, "juego_id": JUEGO_TEST_ID},
        headers=headers,
    )
    assert r1.status_code == 201

    r2 = client.post(
        f"/usuarios/{usuario_id}/juegos",
        json={**body_base, "juego_id": JUEGO_OTRO_ID},
        headers=headers,
    )
    assert r2.status_code == 201

    # Orden ascendente: 1986 antes que 2017
    resp_asc = client.get(f"/usuarios/{usuario_id}/juegos?ordenar=fecha_lanzamiento&orden=asc")
    assert resp_asc.status_code == 200
    data_asc = resp_asc.get_json()
    fechas_asc = [item["lanzamiento"] for item in data_asc]
    assert fechas_asc == sorted(fechas_asc)

    # Orden descendente: 2017 antes que 1986
    resp_desc = client.get(f"/usuarios/{usuario_id}/juegos?ordenar=fecha_lanzamiento&orden=desc")
    assert resp_desc.status_code == 200
    data_desc = resp_desc.get_json()
    fechas_desc = [item["lanzamiento"] for item in data_desc]
    assert fechas_desc == sorted(fechas_desc, reverse=True)