from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from energyos.domain.assumptions import Assumption, AssumptionSet
from energyos.domain.results import Result
from energyos.domain.units import Quantity, Unit


def test_quantity_serializes_value_as_a_string() -> None:
    payload = Quantity(value=Decimal("1.50"), unit=Unit.KWH).model_dump(mode="json")
    assert payload == {"value": "1.50", "unit": "kWh"}


def test_quantity_rejects_non_finite_values() -> None:
    with pytest.raises(ValidationError):
        Quantity(value=Decimal("NaN"), unit=Unit.KWH)


def test_result_requires_assumptions_and_engine_version() -> None:
    quantity = Quantity(value=Decimal("10"), unit=Unit.KWH)
    with pytest.raises(ValidationError):
        Result(
            quantity=quantity,
            assumptions=AssumptionSet(assumptions=()),
            engine_version="energy-0",
        )
    with pytest.raises(ValidationError):
        Result(
            quantity=quantity,
            assumptions=AssumptionSet(
                assumptions=(
                    Assumption(
                        name="performance_ratio",
                        value=Decimal("0.8"),
                        unit=Unit.DIMENSIONLESS,
                        source="fixture",
                        effective_on=date(2026, 1, 1),
                    ),
                )
            ),
            engine_version="  ",
        )
