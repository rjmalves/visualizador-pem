from src.adapters.orm import registry
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from src.adapters.orm import start_mappers
from src.utils.log import Log
from src.utils.settings import Settings


def sqlite_url():
    return f"sqlite:///{Settings.basedir}/data.db"


def start_db():
    SQLITE_URL = sqlite_url()
    Log.log().info(f"Inicializando DB em {SQLITE_URL}")
    engine = create_engine(SQLITE_URL)
    registry.metadata.create_all(engine)
    start_mappers()


def default_session_factory() -> sessionmaker:
    return sessionmaker(
        bind=create_engine(
            sqlite_url(),
        ),
        autoflush=True,
    )
