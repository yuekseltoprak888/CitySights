import pytest

from energyos.composition import build_providers
from energyos.config import Settings
from energyos.domain.errors import ConfigurationError
from energyos.integrations.mock_providers import MockSolarPotentialProvider, MockTariffProvider


def test_mock_providers_do_not_invent_tariffs_or_yields() -> None:
    schedule = MockTariffProvider().get_schedule(municipality_id="261", year=2026)
    potential = MockSolarPotentialProvider().get_potential("synthetic")
    assert schedule.periods == ()
    assert schedule.source == "mock"
    assert schedule.assumptions.assumptions[0].source == "mock"
    assert potential.annual_yield is None
    assert potential.assumptions.assumptions[0].name == "solar_potential_not_configured"


def test_provider_factory_rejects_unregistered_adapters() -> None:
    settings = Settings.model_construct(
        environment="test",
        database_url="postgresql+psycopg://example",
        cors_origins=["http://localhost"],
        address_provider="sonnendach",
        building_data_provider="mock",
        solar_potential_provider="mock",
        weather_provider="mock",
        tariff_provider="mock",
        subsidy_provider="mock",
        log_level="info",
    )
    with pytest.raises(ConfigurationError):
        build_providers(settings)


def test_provider_factory_wires_mocks() -> None:
    settings = Settings(
        environment="test",
        database_url="postgresql+psycopg://energyos:energyos@localhost:5432/energyos",
        cors_origins=["http://localhost:3000"],
    )
    providers = build_providers(settings)
    assert providers.tariff.get_schedule(municipality_id="1", year=2026).periods == ()
