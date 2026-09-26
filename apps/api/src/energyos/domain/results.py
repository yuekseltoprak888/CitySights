from pydantic import BaseModel, ConfigDict, model_validator

from energyos.domain.assumptions import AssumptionSet
from energyos.domain.units import Quantity


class Result(BaseModel):
    """A calculation output bound to the assumptions and engine that produced it."""

    model_config = ConfigDict(frozen=True)

    quantity: Quantity
    assumptions: AssumptionSet
    engine_version: str

    @model_validator(mode="after")
    def result_is_auditable(self) -> "Result":
        if not self.assumptions.assumptions:
            raise ValueError("result requires at least one assumption")
        if not self.engine_version.strip():
            raise ValueError("engine version is required")
        return self
