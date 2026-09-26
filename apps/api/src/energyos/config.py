from functools import lru_cache
from typing import Annotated, Self

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

SUPPORTED_PROVIDERS = frozenset({"mock"})
_PROVIDER_FIELDS = (
    "address_provider",
    "building_data_provider",
    "solar_potential_provider",
    "weather_provider",
    "tariff_provider",
    "subsidy_provider",
)
_EXAMPLE_DATABASE_MARKERS = (
    "://energyos:energyos@",
    "://postgres:postgres@",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        frozen=True,
    )

    environment: str = "local"
    database_url: str
    cors_origins: Annotated[list[str], NoDecode]
    address_provider: str = "mock"
    building_data_provider: str = "mock"
    solar_potential_provider: str = "mock"
    weather_provider: str = "mock"
    tariff_provider: str = "mock"
    subsidy_provider: str = "mock"
    log_level: str = "info"

    @field_validator("environment")
    @classmethod
    def environment_is_known(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned not in {"local", "test", "production"}:
            raise ValueError("environment must be local, test, or production")
        return cleaned

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("database_url")
    @classmethod
    def database_url_is_present(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("database_url is required")
        return cleaned

    @model_validator(mode="after")
    def providers_and_secrets_are_safe(self) -> Self:
        unknown = [
            f"{field}={getattr(self, field)}"
            for field in _PROVIDER_FIELDS
            if getattr(self, field) not in SUPPORTED_PROVIDERS
        ]
        if unknown:
            raise ValueError("unsupported providers: " + ", ".join(unknown))
        if self.environment == "production":
            if any(marker in self.database_url for marker in _EXAMPLE_DATABASE_MARKERS):
                raise ValueError("production cannot use the example database credentials")
            if not self.database_url.startswith("postgresql"):
                raise ValueError("production requires PostgreSQL")
            if not self.cors_origins:
                raise ValueError("production requires CORS origins")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
