from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from energyos.domain.units import Unit


class Assumption(BaseModel):
    """One named input that a later calculation must be able to show."""

    model_config = ConfigDict(frozen=True)

    name: str
    value: Decimal
    unit: Unit
    source: str
    effective_on: date

    @field_validator("name", "source")
    @classmethod
    def text_is_present(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned

    @field_validator("value")
    @classmethod
    def value_is_finite(cls, value: Decimal) -> Decimal:
        if not value.is_finite():
            raise ValueError("value must be finite")
        return value


class AssumptionSet(BaseModel):
    model_config = ConfigDict(frozen=True)

    assumptions: tuple[Assumption, ...]
