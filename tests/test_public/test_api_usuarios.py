"""Tests públicos: endpoints de usuarios (contrato API)."""

import pytest


def test_listar_usuarios_vacio_o_con_datos(client):
    """GET /usuarios devuelve 200 y lista (puede estar vacía)."""
    resp = client.get("/usuarios")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_crear_usuario(client):
    """POST /usuarios con nombre devuelve 201 y usuario con id y nombre."""
    resp = client.post("/usuarios", json={"nombre": "Ana"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert "id" in data
    assert data["nombre"] == "Ana"


def test_crear_usuario_sin_nombre_400(client):
    """POST /usuarios sin nombre devuelve 400."""
    resp = client.post("/usuarios", json={})
    assert resp.status_code == 400


def test_obtener_usuario(client):
    """GET /usuarios/<id> devuelve 200 y usuario si existe."""
    r = client.post("/usuarios", json={"nombre": "Bob"})
    assert r.status_code == 201
    uid = r.get_json()["id"]
    resp = client.get(f"/usuarios/{uid}")
    assert resp.status_code == 200
    assert resp.get_json()["nombre"] == "Bob"


def test_obtener_usuario_404(client):
    """GET /usuarios/<id> inexistente devuelve 404."""
    resp = client.get("/usuarios/99999")
    assert resp.status_code == 404


def test_actualizar_usuario_404(client, auth_user):
    """PUT /usuarios/<id> con token de otro usuario devuelve 401."""
    auth = auth_user()
    resp = client.put("/usuarios/99999", json={"nombre": "X"}, headers=auth["headers"])
    assert resp.status_code == 401


def test_actualizar_usuario_body_invalido_400(client, auth_user):
    """PUT /usuarios/<id> con body inválido devuelve 400."""
    auth = auth_user(nombre="Eve")
    uid = auth["usuario_id"]
    resp = client.put(f"/usuarios/{uid}", json={}, headers=auth["headers"])
    assert resp.status_code == 400


def test_eliminar_usuario_404(client, auth_user):
    """DELETE /usuarios/<id> con token de otro usuario devuelve 401."""
    auth = auth_user()
    resp = client.delete("/usuarios/99999", headers=auth["headers"])
    assert resp.status_code == 401


def test_actualizar_usuario(client, auth_user):
    """PUT /usuarios/<id> actualiza nombre."""
    auth = auth_user(nombre="Carlos")
    uid = auth["usuario_id"]
    resp = client.put(f"/usuarios/{uid}", json={"nombre": "Carlos M."}, headers=auth["headers"])
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["nombre"] == "Carlos M."


def test_eliminar_usuario(client, auth_user):
    """DELETE /usuarios/<id> devuelve 200 y mensaje."""
    auth = auth_user(nombre="Diana")
    uid = auth["usuario_id"]
    resp = client.delete(f"/usuarios/{uid}", headers=auth["headers"])
    assert resp.status_code == 200
    assert "mensaje" in resp.get_json()
    assert client.get(f"/usuarios/{uid}").status_code == 404
