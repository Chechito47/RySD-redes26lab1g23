"""Tests públicos: endpoints de lista de juegos por usuario (por juego_id del catálogo, Wikidata Q-id)."""

import pytest
import requests_mock

from conftest import JUEGO_TEST_ID


@pytest.fixture
def usuario_auth(auth_user):
    """Crea un usuario autenticado y devuelve id + headers."""
    return auth_user(nombre="TestUser")


def test_listar_juegos_usuario_vacio(client, usuario_auth):
    """GET /usuarios/<id>/juegos devuelve 200 y lista vacía."""
    usuario_id = usuario_auth["usuario_id"]
    resp = client.get(f"/usuarios/{usuario_id}/juegos")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_agregar_juego_usuario(client, usuario_auth, rawg_mock):
    """POST /usuarios/<id>/juegos con juego_id (catálogo) devuelve 201 e ítem con id."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]
    r = client.get("/juegos?q=zelda&fuente=wikidata")
    assert r.status_code == 200
    body = {
        "juego_id": JUEGO_TEST_ID,
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    resp = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["id"] == JUEGO_TEST_ID
    assert data["nombre"] == "Zelda"
    assert data["tengo"] is True
    assert "fecha_agregado" in data


def test_agregar_juego_duplicado_409(client, usuario_auth, rawg_mock):
    """POST /usuarios/<id>/juegos con juego_id ya en la lista devuelve 409."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]
    client.get("/juegos?q=zelda&fuente=wikidata")
    body = {
        "juego_id": JUEGO_TEST_ID,
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    r1 = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=headers)
    assert r1.status_code == 201
    r2 = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=headers)
    assert r2.status_code == 409
    assert "error" in r2.get_json()


def test_listar_juegos_con_filtro_orden(client, usuario_auth, rawg_mock):
    """GET /usuarios/<id>/juegos?genero=X&ordenar=nombre devuelve 200."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]
    client.get("/juegos?q=zelda&fuente=wikidata")
    client.post(
        f"/usuarios/{usuario_id}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        },
        headers=headers,
    )
    resp = client.get(f"/usuarios/{usuario_id}/juegos?genero=Aventura&ordenar=nombre")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_listar_juegos_orden_desc(client, usuario_auth, rawg_mock):
    """GET /usuarios/<id>/juegos?orden=desc devuelve 200 y lista en orden descendente."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]
    client.get("/juegos?q=zelda&fuente=wikidata")
    client.post(
        f"/usuarios/{usuario_id}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        },
        headers=headers,
    )
    resp = client.get(f"/usuarios/{usuario_id}/juegos?ordenar=nombre&orden=desc")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    nombres = [item.get("nombre") or "" for item in data]
    assert nombres == sorted(nombres, reverse=True, key=str.lower)


def test_actualizar_juego_usuario(client, usuario_auth, rawg_mock):
    """PUT /usuarios/<id>/juegos/<juego_id> actualiza booleanos."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]
    client.get("/juegos?q=zelda&fuente=wikidata")
    client.post(
        f"/usuarios/{usuario_id}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        },
        headers=headers,
    )
    resp = client.put(
        f"/usuarios/{usuario_id}/juegos/{JUEGO_TEST_ID}",
        json={"jugado": True, "me_gusta": True},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.get_json()["jugado"] is True
    assert resp.get_json()["me_gusta"] is True


def test_eliminar_juego_usuario(client, usuario_auth, rawg_mock):
    """DELETE /usuarios/<id>/juegos/<juego_id> devuelve 200."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]
    client.get("/juegos?q=zelda&fuente=wikidata")
    client.post(
        f"/usuarios/{usuario_id}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": False,
            "quiero": True,
            "jugado": False,
            "me_gusta": False,
        },
        headers=headers,
    )
    resp = client.delete(f"/usuarios/{usuario_id}/juegos/{JUEGO_TEST_ID}", headers=headers)
    assert resp.status_code == 200


def test_listar_juegos_otro_usuario(client, usuario_auth):
    """GET /usuarios/<id>/juegos devuelve la lista de ese usuario."""
    usuario_id = usuario_auth["usuario_id"]
    resp = client.get(f"/usuarios/{usuario_id}/juegos")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_listar_juegos_usuario_inexistente_404(client):
    """GET /usuarios/<id>/juegos con usuario inexistente devuelve 404."""
    resp = client.get("/usuarios/99999/juegos")
    assert resp.status_code == 404


def test_agregar_juego_usuario_inexistente_404(client, auth_user, rawg_mock):
    """POST /usuarios/<id>/juegos con token de otro usuario devuelve 401."""
    auth = auth_user()
    client.get("/juegos?q=zelda&fuente=wikidata")
    body = {
        "juego_id": JUEGO_TEST_ID,
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    resp = client.post("/usuarios/99999/juegos", json=body, headers=auth["headers"])
    assert resp.status_code == 401


def test_agregar_juego_usuario_fallo_wikidata_404(client, usuario_auth):
    """POST /usuarios/<id>/juegos cuando Wikidata falla devuelve 404 (no se pudo obtener el juego)."""
    usuario_id = usuario_auth["usuario_id"]
    headers = usuario_auth["headers"]
    with requests_mock.Mocker() as m:
        m.get(
            "https://www.wikidata.org/w/api.php",
            status_code=500,
        )
        body = {
            "juego_id": "QERROR",
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        }
        resp = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=headers)
        assert resp.status_code == 404
