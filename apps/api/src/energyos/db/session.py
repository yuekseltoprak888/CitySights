from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def build_session_factory(database_url: str) -> tuple[Engine, sessionmaker[Session]]:
    engine = create_engine(database_url, pool_pre_ping=True)
    factory = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
    return engine, factory
