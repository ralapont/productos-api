from productos_api.core.vault import client

secret = client.secrets.kv.v2.read_secret_version(
    mount_point="productos_api",
    path="database"
)

db = secret["data"]["data"]

class Settings:

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{db['username']}:{db['password']}"
            f"@{db['host']}:{db['port']}"
            f"/{db['database']}"
        )

settings = Settings()