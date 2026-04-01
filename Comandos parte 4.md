# Comandos parte 4
Para probar los endpoints de la gestión de listas de juegos se usó **curl**. Las flags son:  
- `-X`: indica el método HTTP a usar *(POST, PUT, DELETE)*.  
- `-H`: agrega un header a la request. Se usa `Content-Type: application/json` para avisarle al servidor que el body es JSON.  
- `-d`: es el body de la request, los datos que se envían al servidor.  

Los comandos que usamos son:  

**Listar juegos de un usuario** *(reemplazar 1 por algún id)*:  
```bash
curl http://localhost:5000/usuarios/1/juegos
``` 

**Filtrar y ordenar lista** *(ejemplo: género Acción y orden descendente)*:  
```bash
curl "http://localhost:5000/usuarios/1/juegos?genero=Accion&ordenar=nombre&orden=desc"
```  

**Agregar juego a la lista** *(reemplazar Q-id por uno de Wikidata)*:  
```bash
curl -X POST http://localhost:5000/usuarios/1/juegos -H "Content-Type: application/json" -d '{"juego_id": "Q380", "tengo": true, "quiero": false, "jugado": true, "me_gusta": true}'
```

**Actualizar estado de un juego** *(reemplazar 1 y Q-id)*:  
```bash
curl -X PUT http://localhost:5000/usuarios/1/juegos/Q380 -H "Content-Type: application/json" -d '{"jugado": true, "me_gusta": false}'
```

**Eliminar juego de la lista** *(reemplazar 1 y Q-id)*:  
```bash
curl -X DELETE http://localhost:5000/usuarios/1/juegos/Q380
```