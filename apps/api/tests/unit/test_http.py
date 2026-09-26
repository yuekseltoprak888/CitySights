from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from energyos.api.deps import get_health_service, get_organization_service
from energyos.config import Settings
from energyos.domain.health import DatabaseStatus
from energyos.domain.tenancy import Organization
from energyos.main import create_app
from energyos.services.health import HealthService
from energyos.services.organizations import OrganizationService


def settings() -> Settings:
    return Settings(
        environment="test",
        database_url="postgresql+psycopg://energyos:energyos@localhost:5432/energyos",
        cors_origins=["http://localhost:3000"],
    )


class StaticProbe:
    def __init__(self, status: DatabaseStatus) -> None:
        self._status = status

    def check(self) -> DatabaseStatus:
        return self._status


class MissingOrganizations:
    def add(self, organization: Organization) -> Organization:
        return organization

    def get(self, organization_id: UUID) -> Organization | None:
        del organization_id
        return None


def test_health_reports_switzerland_and_request_id() -> None:
    application = create_app(settings())
    application.dependency_overrides[get_health_service] = lambda: HealthService(
        StaticProbe(DatabaseStatus(database="ok", postgis="ok")),
        environment="test",
    )
    with TestClient(application) as client:
        response = client.get("/api/v1/health", headers={"X-Request-Id": "req-123"})
    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-123"
    assert response.json()["country"] == "CH"
    assert response.json()["status"] == "ok"


def test_degraded_health_returns_503() -> None:
    application = create_app(settings())
    application.dependency_overrides[get_health_service] = lambda: HealthService(
        StaticProbe(DatabaseStatus(database="unavailable", postgis="unavailable")),
        environment="test",
    )
    with TestClient(application) as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 503
    assert response.json()["status"] == "degraded"
    assert response.json()["database"] == "unavailable"


def test_missing_organization_uses_the_error_shape() -> None:
    application = create_app(settings())
    application.dependency_overrides[get_organization_service] = lambda: OrganizationService(
        MissingOrganizations()
    )
    with TestClient(application) as client:
        response = client.get(f"/api/v1/organizations/{uuid4()}")
    body = response.json()
    assert response.status_code == 404
    assert body["code"] == "organization_not_found"
    assert body["message"] == "Organization not found"
    assert body["details"] == {}
    assert body["request_id"]


def test_openapi_lists_foundation_routes() -> None:
    application = create_app(settings())
    paths = set(application.openapi()["paths"])
    application.state.engine.dispose()
    assert "/api/v1/health" in paths
    assert "/api/v1/organizations" in paths
    assert "/api/v1/organizations/{organization_id}" in paths
    assert "/api/v1/organizations/{organization_id}/assessments" in paths
    assert "/api/v1/organizations/{organization_id}/assessments/{assessment_id}" in paths
