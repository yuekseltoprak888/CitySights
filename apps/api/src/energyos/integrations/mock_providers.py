"""Synthetic provider fixtures.

These adapters prove the port boundary. They do not contain surveyed Swiss
data, tariff rates, subsidy amounts, or engineering assumptions.
"""

from datetime import date
from decimal import Decimal

from energyos.domain.assumptions import Assumption, AssumptionSet
from energyos.domain.records import (
    AddressMatch,
    BuildingRecord,
    SolarPotentialRecord,
    SubsidyCatalog,
    TariffSchedule,
    WeatherRecord,
)
from energyos.domain.units import Unit


def _synthetic(name: str) -> AssumptionSet:
    return AssumptionSet(
        assumptions=(
            Assumption(
                name=name,
                value=Decimal("1"),
                unit=Unit.DIMENSIONLESS,
                source="mock",
                effective_on=date(2026, 1, 1),
            ),
        )
    )


class MockAddressProvider:
    def search(self, query: str) -> tuple[AddressMatch, ...]:
        if not query.strip():
            return ()
        return (
            AddressMatch(
                label="Synthetic address",
                source="mock",
                assumptions=_synthetic("geocoding_not_configured"),
            ),
        )


class MockBuildingDataProvider:
    def get_building(self, external_id: str) -> BuildingRecord | None:
        if not external_id.strip():
            return None
        return BuildingRecord(
            source="mock",
            external_id=external_id.strip(),
            display_name="Synthetic building",
            assumptions=_synthetic("building_register_not_configured"),
        )


class MockSolarPotentialProvider:
    def get_potential(self, building_id: str) -> SolarPotentialRecord:
        del building_id
        return SolarPotentialRecord(
            source="mock",
            annual_yield=None,
            assumptions=_synthetic("solar_potential_not_configured"),
        )


class MockWeatherProvider:
    def get_site_weather(self, building_id: str) -> WeatherRecord:
        del building_id
        return WeatherRecord(
            source="mock",
            assumptions=_synthetic("weather_not_configured"),
        )


class MockTariffProvider:
    def get_schedule(self, *, municipality_id: str, year: int) -> TariffSchedule:
        del municipality_id, year
        return TariffSchedule(
            source="mock",
            periods=(),
            assumptions=_synthetic("tariff_not_configured"),
        )


class MockSubsidyProvider:
    def list_programs(self, *, canton: str, year: int) -> SubsidyCatalog:
        del canton, year
        return SubsidyCatalog(
            source="mock",
            programs=(),
            assumptions=_synthetic("subsidies_not_configured"),
        )
