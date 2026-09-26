from dataclasses import dataclass

from sqlalchemy.orm import Session

from energyos.config import Settings
from energyos.db.probe import SqlAlchemyDatabaseProbe
from energyos.db.repositories import (
    SqlAlchemyAssessmentRepository,
    SqlAlchemyOrganizationRepository,
)
from energyos.domain.errors import ConfigurationError
from energyos.domain.ports import (
    AddressProvider,
    BuildingDataProvider,
    SolarPotentialProvider,
    SubsidyProvider,
    TariffProvider,
    WeatherProvider,
)
from energyos.integrations.mock_providers import (
    MockAddressProvider,
    MockBuildingDataProvider,
    MockSolarPotentialProvider,
    MockSubsidyProvider,
    MockTariffProvider,
    MockWeatherProvider,
)
from energyos.services.assessments import AssessmentService
from energyos.services.health import HealthService
from energyos.services.organizations import OrganizationService


@dataclass(frozen=True)
class ProviderRegistry:
    address: AddressProvider
    building_data: BuildingDataProvider
    solar_potential: SolarPotentialProvider
    weather: WeatherProvider
    tariff: TariffProvider
    subsidy: SubsidyProvider


def build_providers(settings: Settings) -> ProviderRegistry:
    selected = {
        "address": settings.address_provider,
        "building_data": settings.building_data_provider,
        "solar_potential": settings.solar_potential_provider,
        "weather": settings.weather_provider,
        "tariff": settings.tariff_provider,
        "subsidy": settings.subsidy_provider,
    }
    unknown = {name: value for name, value in selected.items() if value != "mock"}
    if unknown:
        joined = ", ".join(f"{name}={value}" for name, value in sorted(unknown.items()))
        raise ConfigurationError(f"unsupported providers: {joined}")
    return ProviderRegistry(
        address=MockAddressProvider(),
        building_data=MockBuildingDataProvider(),
        solar_potential=MockSolarPotentialProvider(),
        weather=MockWeatherProvider(),
        tariff=MockTariffProvider(),
        subsidy=MockSubsidyProvider(),
    )


def build_health_service(session: Session, settings: Settings) -> HealthService:
    return HealthService(probe=SqlAlchemyDatabaseProbe(session), environment=settings.environment)


def build_organization_service(session: Session) -> OrganizationService:
    return OrganizationService(SqlAlchemyOrganizationRepository(session))


def build_assessment_service(session: Session) -> AssessmentService:
    return AssessmentService(
        organizations=SqlAlchemyOrganizationRepository(session),
        assessments=SqlAlchemyAssessmentRepository(session),
    )
