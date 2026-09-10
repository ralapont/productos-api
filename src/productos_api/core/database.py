from sqlmodel import Session, create_engine

from productos_api.core.config import settings


engine = create_engine(
    settings.database_url,
    echo=True,
)


def get_session():
    with Session(engine) as session:
        yield session