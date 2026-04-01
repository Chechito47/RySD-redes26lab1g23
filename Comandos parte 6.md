# Comandos parte 6
Para probar el endpoint de sugerencias se usa **curl**. Recordá que para que una sugerencia sea válida, el usuario debe tener al menos un juego con la propiedad `"tengo": true`.

Los comandos que usamos son:

**Obtener sugerencia aleatoria**:  
```bash
curl http://localhost:5000/usuarios/1/sugerencia
``` 

**Obtener sugerencia filtrada por género** *(ejemplo: género Acción)*:  
```bash
curl "http://localhost:5000/usuarios/1/sugerencia?genero=Accion"
```

**Probar error de usuario inexistente** *(reemplazar 999 por un id que no exista)*:  
```bash
curl http://localhost:5000/usuarios/999/sugerencia
```

**Probar error cuando no hay juegos con "tengo: true"**:  
```bash
curl http://localhost:5000/usuarios/1/sugerencia
``` 
*(Este comando devolverá 404 si previamente vaciaste la lista o pusiste todos los juegos en "tengo: false")*