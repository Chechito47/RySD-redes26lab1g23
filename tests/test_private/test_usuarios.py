import pytest

# Fixture para tener un usuario de base en cada test
@pytest.fixture
def usuario_ejemplo(client):
    res = client.post("/usuarios", json={"nombre": "Juan Carlos"})
    return res.get_json()

# Tests felices :)
def test_listar_usuarios_200(client, usuario_ejemplo):
    """Prueba que el GET /usuarios devuelva una lista y código 200."""
    r = client.get("/usuarios")
    
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)
    assert any(u["id"] == usuario_ejemplo["id"] for u in r.get_json())

def test_obtener_usuario_200(client, usuario_ejemplo):
    """Prueba obtener un usuario existente por ID."""
    uid = usuario_ejemplo["id"]
    r = client.get(f"/usuarios/{uid}")
    
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Juan Carlos"

def test_actualizar_usuario_200(client, usuario_ejemplo):
    """Prueba cambiar el nombre de un usuario existente."""
    uid = usuario_ejemplo["id"]
    r = client.put(f"/usuarios/{uid}", json={"nombre": "Juan Editado"})
    
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Juan Editado"

def test_eliminar_usuario_200(client, usuario_ejemplo):
    """Prueba borrar un usuario existente."""
    uid = usuario_ejemplo["id"]
    r = client.delete(f"/usuarios/{uid}")
    
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

def test_actualizar_usuario_inexistente_404(client):
    """Fuerza el 404 al intentar editar a alguien que no existe."""
    r = client.put("/usuarios/999999", json={"nombre": "Fantasma"})
    
    assert r.status_code == 404

def test_eliminar_usuario_inexistente_404(client):
    """Fuerza el 404 al intentar borrar a alguien que no existe."""
    r = client.delete("/usuarios/999999")
    
    assert r.status_code == 404