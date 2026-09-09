# Servicio de productos

* Framework de la API
    FastAPI

* Endpoint real de productos
    http://localhost:8000

    | verbo | endpoint | descripción |
    |-------|----------|-------------|
    | GET   | /products | Obtiene todos los productos |
    | GET   | /products/{id} | Obtiene un producto por su ID |
    | POST  | /products | Crea un nuevo producto |
    | PUT   | /products/{id} | Actualiza un producto existente por su ID |
    | DELETE | /products/{id} | Elimina un producto por su ID |
    | PATCH | /products/{id} | Actualiza parcialmente un producto por su ID |

* Ejemplo de solicitud GET para obtener todos los productos

    ```bash
    curl -X GET "http://localhost:8000/products" -H "accept: application/json"
    ```
* Ejemplo de solicitud GET para obtener un producto por su ID

    ```bash
    curl -X GET "http://localhost:8000/products/1" -H "accept: application/json"
    ```
* Ejemplo de solicitud POST para crear un nuevo producto

    ```bash
    curl -X POST "http://localhost:8000/products" -H "accept: application/json" -H "Content-Type: application/json" -d '{"name":"Producto 1","description":"Descripción del producto 1","price":10.99,"stock":100}'
    ```
* Ejemplo de solicitud PUT para actualizar un producto existente por su ID

    ```bash
    curl -X PUT "http://localhost:8000/products/1" -H "accept: application/json" -H "Content-Type: application/json" -d '{"name":"Producto 1 actualizado","description":"Descripción actualizada del producto 1","price":12.99,"stock":80}'
    ```
* Ejemplo de solicitud DELETE para eliminar un producto por su ID

    ```bash
    curl -X DELETE "http://localhost:8000/products/1" -H "accept: application/json"
    ```            
* Estructura JSON que devuelve

    ```json
    {
        "id": 1,
        "name": "Producto 1",
        "description": "Descripción del producto 1",
        "price": 10.99,
        "stock": 100
    }
    ```

## Ejecutar el servicio

1. Crear las variables de entorno

```bash
export VAULT_URL=http://localhost:8200
export VAULT_TOKEN=myroottoken
```

2. Crear los secretos en vault

* Creo el mount point para el secreto y el path donde se guardará el secreto

```bash
docker exec -it -e VAULT_ADDR='http://127.0.0.1:8200' vault-server vault secrets enable -path=productos_api kv-v2
docker exec -it -e VAULT_ADDR='http://127.0.0.1:8200' vault-server vault secrets list
```

* Creo el secreto con la información de la base de datos

```bash
docker exec -it -e VAULT_ADDR='http://127.0.0.1:8200' vault-server vault kv put productos_api/database username="postgres" password="postgres123" host="localhost" port="5432" database="productos_db"
```
3. Crear tabla con alembic

```bash
uv run alembic -x db_url="postgresql://postgres:postgres123@localhost:5432/productos_db" upgrade head
```

4. Ejecutar uvicorn

```bash
source .venv/bin/activate

uv run uvicorn src.productos_api.main:app --reload
uv run uvicorn src.productos_api.main:app --host 0.0.0.0 --port 8000
```

