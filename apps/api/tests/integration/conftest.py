import os
from collections.abc import Iterator

import pytest
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from energyos.config import Settings
from energyos.main import create_app


def _reachable(url: str) -> bool:
    engine = create_engine(url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError:
        return False
    finally:
        engine.dispose()


def _migrate(url: str) -> None:
    os.environ["DATABASE_URL"] = url
    config = Config("alembic.ini")
    command.upgrade(config, "head")


def _truncate(app: FastAPI) -> None:
    session = app.state.session_factory()
    try:
        session.execute(
            text(
                "TRUNCATE TABLE assessment, membership, app_user, organization "
                "RESTART IDENTITY CASCADE"
            )
        )
        session.commit()
    finally:
        session.close()


@pytest.fixture(scope="session")
def database_url() -> str:
    url = os.environ.get("DATABASE_URL", "").strip()
    require = os.environ.get("REQUIRE_DATABASE") == "1"
    if not url or not _reachable(url):
        if require:
            pytest.fail("PostgreSQL with PostGIS is required")
        pytest.skip("PostgreSQL with PostGIS is not reachable")
    _migrate(url)
    return url


@pytest.fixture
def app(database_url: str) -> Iterator[FastAPI]:
    application = create_app(
        Settings(
            environment="test",
            database_url=database_url,
            cors_origins=["http://localhost:3000"],
        )
    )
    yield application


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    _truncate(app)
    with TestClient(app) as test_client:
        yield test_client
        _truncate(app)
