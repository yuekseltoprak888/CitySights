import pytest
from pydantic import ValidationError

from energyos.config import Settings


def test_comma_separated_cors_origins_are_read_from_the_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://energyos:energyos@localhost:5432/energyos",
    )
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000, http://127.0.0.1:3000")
    settings = Settings()
    assert settings.cors_origins == ["http://localhost:3000", "http://127.0.0.1:3000"]


def test_local_settings_accept_example_credentials() -> None:
    settings = Settings.model_validate(
        {
            "environment": "local",
            "database_url": "postgresql+psycopg://energyos:energyos@localhost:5432/energyos",
            "cors_origins": "http://localhost:3000, http://127.0.0.1:3000",
        }
    )
    assert settings.cors_origins == ["http://localhost:3000", "http://127.0.0.1:3000"]
    assert settings.building_data_provider == "mock"


def test_production_rejects_example_database_credentials() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="production",
            database_url="postgresql+psycopg://energyos:energyos@db:5432/energyos",
            cors_origins=["https://app.energyos.example"],
        )


def test_unknown_provider_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(
            environment="test",
            database_url="postgresql+psycopg://energyos:energyos@localhost:5432/energyos",
            cors_origins=["http://localhost:3000"],
            tariff_provider="elcom",
        )
