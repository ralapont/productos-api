import os
from unittest.mock import MagicMock
import sys

# 1. Mockeamos la librería hvac para que no intente conectar a Vault real al importar config.py
mock_hvac = MagicMock()
mock_client = MagicMock()
mock_client.secrets.kv.v2.read_secret_version.return_value = {
    "data": {
        "data": {
            "username": "test_user",
            "password": "test_password",
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "db_name": "test_db"
        }
    }
}
mock_hvac.Client.return_value = mock_client
sys.modules["hvac"] = mock_hvac

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

# IMPORTANTE: Ajusta estas importaciones a la ruta de tu proyecto
from productos_api.main import app
from productos_api.core.database import get_session  # get_session es la función usada con Depends() en los endpoints

# SQLite en memoria para pruebas
SQLITE_TEST_URL = "sqlite:///:memory:"

@pytest.fixture(name="session")
def session_fixture():
    # connect_args={"check_same_thread": False} y StaticPool permiten compartir 
    # la BD en memoria entre hilos del cliente de pruebas
    engine = create_engine(
        SQLITE_TEST_URL, 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Sobrescribimos la dependencia de producción con nuestra sesión de SQLite
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()