from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator


class Unit(StrEnum):
    KWH = "kWh"
    KW = "kW"
    KWP = "kWp"
    M2 = "m2"
    CHF = "CHF"
    CHF_PER_KWH = "CHF/kWh"
    PERCENT = "percent"
    DIMENSIONLESS = "1"


class Quantity(BaseModel):
    """A numeric value that cannot leave the domain without a unit."""

    model_config = ConfigDict(frozen=True)

    value: Decimal
    unit: Unit

    @field_validator("value")
    @classmethod
    def value_is_finite(cls, value: Decimal) -> Decimal:
        if not value.is_finite():
            raise ValueError("value must be finite")
        return value
