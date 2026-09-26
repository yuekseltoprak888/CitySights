from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from energyos.domain.assumptions import AssumptionSet
from energyos.domain.results import Result
from energyos.domain.units import Quantity


class AddressMatch(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    source: str
    longitude_wgs84: Decimal | None = None
    latitude_wgs84: Decimal | None = None
    easting_lv95: Decimal | None = None
    northing_lv95: Decimal | None = None
    assumptions: AssumptionSet


class BuildingRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str
    external_id: str
    display_name: str
    assumptions: AssumptionSet


class SolarPotentialRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str
    annual_yield: Result | None
    assumptions: AssumptionSet


class WeatherRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str
    assumptions: AssumptionSet


class TariffPeriod(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    rate: Quantity


class TariffSchedule(BaseModel):
    """A time-of-use schedule supplied by a tariff provider.

    Periods stay empty until a real utility dataset is connected. The domain
    does not invent Swiss tariff rates.
    """

    model_config = ConfigDict(frozen=True)

    source: str
    periods: tuple[TariffPeriod, ...]
    assumptions: AssumptionSet


class SubsidyProgram(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    name: str
    assumptions: AssumptionSet


class SubsidyCatalog(BaseModel):
    model_config = ConfigDict(frozen=True)

    source: str
    programs: tuple[SubsidyProgram, ...]
    assumptions: AssumptionSet
