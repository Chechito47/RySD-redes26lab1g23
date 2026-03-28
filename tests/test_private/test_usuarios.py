import pytest

# Fixture para tener un usuario de base en cada test
@pytest.fixture
def usuario_ejemplo(auth_user):
    return auth_user(nombre="Juan Carlos")

# Tests felices :)
def test_listar_usuarios_200(client, usuario_ejemplo):
    """Prueba que el GET /usuarios devuelva una lista y código 200."""
    r = client.get("/usuarios")
    
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)
    assert any(u["id"] == usuario_ejemplo["usuario_id"] for u in r.get_json())

def test_obtener_usuario_200(client, usuario_ejemplo):
    """Prueba obtener un usuario existente por ID."""
    uid = usuario_ejemplo["usuario_id"]
    r = client.get(f"/usuarios/{uid}")
    
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Juan Carlos"

def test_actualizar_usuario_200(client, usuario_ejemplo):
    """Prueba cambiar el nombre de un usuario existente."""
    uid = usuario_ejemplo["usuario_id"]
    r = client.put(f"/usuarios/{uid}", json={"nombre": "Juan Editado"}, headers=usuario_ejemplo["headers"])
    
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Juan Editado"

def test_eliminar_usuario_200(client, usuario_ejemplo):
    """Prueba borrar un usuario existente."""
    uid = usuario_ejemplo["usuario_id"]
    r = client.delete(f"/usuarios/{uid}", headers=usuario_ejemplo["headers"])
    
    assert r.status_code == 200
    assert "mensaje" in r.get_json()
    
    # Verifico que no exista
    r_check = client.get(f"/usuarios/{uid}")
    assert r_check.status_code == 404

# Tests casos borde
def test_obtener_usuario_inexistente_404(client):
    """Fuerza el error 404 al buscar un ID que no existe."""
    r = client.get("/usuarios/999999")
    
    assert r.status_code == 404
    assert "error" in r.get_json()

def test_crear_usuario_sin_nombre_400(client):
    """Fuerza el error 400 al no mandar el campo 'nombre'."""
    r = client.post("/usuarios", json={})
    
    assert r.status_code == 400

def test_actualizar_usuario_inexistente_404(client, auth_user):
    """Con token de otro usuario, editar ID inexistente devuelve 401."""
    auth = auth_user()
    r = client.put("/usuarios/999999", json={"nombre": "Fantasma"}, headers=auth["headers"])

    assert r.status_code == 401

def test_eliminar_usuario_inexistente_404(client, auth_user):
    """Con token de otro usuario, borrar ID inexistente devuelve 401."""
    auth = auth_user()
    r = client.delete("/usuarios/999999", headers=auth["headers"])

    assert r.status_code == 401