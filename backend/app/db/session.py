from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend.app.core.config import get_settings


def build_engine(database_url: str | None = None) -> Engine:
    settings = get_settings()
    resolved_url = database_url or settings.database_url
    connect_args: dict[str, object] = {}
    engine_kwargs: dict[str, object] = {"future": True}

    if resolved_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    else:
        engine_kwargs["pool_pre_ping"] = True

    return create_engine(resolved_url, connect_args=connect_args, **engine_kwargs)


engine: Engine | None = None
SessionLocal = sessionmaker(autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)


def get_engine() -> Engine:
    global engine

    if engine is None:
        engine = build_engine()
    return engine


def create_session() -> Session:
    return SessionLocal(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    db = create_session()
    try:
        yield db
    finally:
        db.close()
