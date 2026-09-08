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

