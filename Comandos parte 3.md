# Comandos parte 3
Para probar los endpoints se uso **curl**. Las flags son:  
- `-X`: indica el metodo HTTP a usar *(POST, PUT, DELETE)*. Sin esta flag curl hace GET por defecto  
- `-H`: agrega un header a la request. Se usa `Content-Type: application/json` para avisarle al servidor que el body es JSON  
- `-d`: es el body de la request, los datos que se envian al servidor  

Los comandos que usamos son:  

> Nota: desde que se agregó seguridad, **PUT /usuarios/<id>** y **DELETE /usuarios/<id>** requieren
> header `Authorization: Token <TOKEN>`.

**Crear usuario**:  
```bash
curl -X POST http://localhost:5000/usuarios -H "Content-Type: application/json" -d '{"nombre": "Ana"}'
```
**Listar usuarios**:  
```bash
curl http://localhost:5000/usuarios
```

**Obtener usuario por id** *(reemplazar 1 por algun id)*:  
```bash
curl http://localhost:5000/usuarios/1
```

**(Opcional) Obtener token para operaciones protegidas**:
```bash
# 1) Registrar usuario con credenciales
curl -X POST http://localhost:5000/auth/registro \
	-H "Content-Type: application/json" \
	-d '{"username":"ana","nombre":"Ana","password":"1234"}'

# 2) Login (copiar el token que devuelve)
curl -X POST http://localhost:5000/auth/login \
	-H "Content-Type: application/json" \
	-d '{"username":"ana","password":"1234"}'
```

**Actualizar usuario** *(reemplazar 1 por algun id)* y \<TOKEN> por el devuelto antes:  
```bash
curl -X PUT http://localhost:5000/usuarios/1 \
	-H "Authorization: Token <TOKEN>" \
	-H "Content-Type: application/json" \
	-d '{"nombre": "Ana"}'
```

**Eliminar usuario** *(reemplazar 1 por algun id)*:  
```bash
curl -X DELETE http://localhost:5000/usuarios/1 \
	-H "Authorization: Token <TOKEN>"
```