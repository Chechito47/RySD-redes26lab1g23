# Comandos parte 3
Para probar los endpoints se uso **curl**. Las flags son:  
- `-X`: indica el metodo HTTP a usar *(POST, PUT, DELETE)*. Sin esta flag curl hace GET por defecto  
- `-H`: agrega un header a la request. Se usa `Content-Type: application/json` para avisarle al servidor que el body es JSON  
- `-d`: es el body de la request, los datos que se envian al servidor  

Los comandos que usamos son:  

**Crear usuario**:  
`curl -X POST http://localhost:5000/usuarios -H "Content-Type: application/json" -d '{"nombre": "Ana"}'`  

**Listar usuarios**:  
`curl http://localhost:5000/usuarios`  

**Obtener usuario por id** *(reemplazar 1 por algun id)*:  
`curl http://localhost:5000/usuarios/1`  

**Actualizar usuario** *(reemplazar 1 por algun id)*:  
`curl -X PUT http://localhost:5000/usuarios/1 -H "Content-Type: application/json" -d '{"nombre": "Ana"}'`  

**Eliminar usuario** *(reemplazar 1 por algun id)*:  
`curl -X DELETE http://localhost:5000/usuarios/1`
