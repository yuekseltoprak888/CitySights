from typing import Literal

from pydantic import BaseModel, ConfigDict


class DatabaseStatus(BaseModel):
    model_config = ConfigDict(frozen=True)

    database: Literal["ok", "unavailable"]
    postgis: Literal["ok", "unavailable"]


class HealthReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: Literal["ok", "degraded"]
    environment: str
    country: Literal["CH"]
    database: Literal["ok", "unavailable"]
    postgis: Literal["ok", "unavailable"]
