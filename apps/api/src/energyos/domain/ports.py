from typing import Protocol
from uuid import UUID

from energyos.domain.assumptions import AssumptionSet
from energyos.domain.health import DatabaseStatus
from energyos.domain.records import (
    AddressMatch,
    BuildingRecord,
    SolarPotentialRecord,
    SubsidyCatalog,
    TariffSchedule,
    WeatherRecord,
)
from energyos.domain.results import Result
from energyos.domain.tenancy import Assessment, AssessmentPage, Organization


class OrganizationRepository(Protocol):
    def add(self, organization: Organization) -> Organization: ...

    def get(self, organization_id: UUID) -> Organization | None: ...


class AssessmentRepository(Protocol):
    def add(self, assessment: Assessment) -> Assessment: ...

    def get(self, organization_id: UUID, assessment_id: UUID) -> Assessment | None: ...

    def list_for_organization(
        self,
        organization_id: UUID,
        *,
        limit: int,
        cursor: str | None,
    ) -> AssessmentPage: ...


class DatabaseProbe(Protocol):
    def check(self) -> DatabaseStatus: ...


class AddressProvider(Protocol):
    def search(self, query: str) -> tuple[AddressMatch, ...]: ...


class BuildingDataProvider(Protocol):
    def get_building(self, external_id: str) -> BuildingRecord | None: ...


class SolarPotentialProvider(Protocol):
    def get_potential(self, building_id: str) -> SolarPotentialRecord: ...


class WeatherProvider(Protocol):
    def get_site_weather(self, building_id: str) -> WeatherRecord: ...


class TariffProvider(Protocol):
    def get_schedule(self, *, municipality_id: str, year: int) -> TariffSchedule: ...


class SubsidyProvider(Protocol):
    def list_programs(self, *, canton: str, year: int) -> SubsidyCatalog: ...


class EnergyEngine(Protocol):
    """Physical energy calculations. Implementations stay out of the finance package."""

    def evaluate(self, assumptions: AssumptionSet) -> Result: ...


class FinancialEngine(Protocol):
    """Investment calculations. They consume energy results and tariff schedules as values."""

    def evaluate(
        self,
        energy: Result,
        tariff: TariffSchedule,
        assumptions: AssumptionSet,
    ) -> Result: ...
