"""Tests: sugerencia con filtro por género."""
import pytest
from conftest import JUEGO_TEST_ID


@pytest.fixture
def usuario_con_juego(auth_user, client, rawg_mock):
    """Usuario autenticado con un juego (tengo=True) en su lista."""
    auth = auth_user(nombre="UsuarioSugerencia")
    usuario_id = auth["usuario_id"]
    headers = auth["headers"]

    # Poblar catálogo y agregar juego con tengo=True
    client.get("/juegos?q=zelda&fuente=wikidata")
    r = client.post(
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
    assert r.status_code == 201

    return {"usuario_id": usuario_id, "headers": headers, "genero": r.get_json()["genero"]}


def test_sugerencia_con_genero_solo_devuelve_ese_genero(client, usuario_con_juego):
    """GET /usuarios/<id>/sugerencia?genero=X devuelve un juego de ese género."""
    usuario_id = usuario_con_juego["usuario_id"]
    genero = usuario_con_juego["genero"]  # "Aventura" según el mock

    resp = client.get(f"/usuarios/{usuario_id}/sugerencia?genero={genero}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["genero"] == genero
    assert "nombre" in data
    assert "descripcion" in data


def test_sugerencia_genero_sin_coincidencias_404(client, usuario_con_juego):
    """GET /usuarios/<id>/sugerencia?genero=X sin juegos de ese género devuelve 404."""
    usuario_id = usuario_con_juego["usuario_id"]

    resp = client.get(f"/usuarios/{usuario_id}/sugerencia?genero=GeneroQueNoExiste")
    assert resp.status_code == 404
    assert "error" in resp.get_json()