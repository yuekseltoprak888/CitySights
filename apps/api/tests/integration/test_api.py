import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text

pytestmark = pytest.mark.integration


def test_health_includes_postgis(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"
    assert body["postgis"] == "ok"
    assert body["country"] == "CH"


def test_tenancy_tables_exist(app: FastAPI, client: TestClient) -> None:
    del client
    session = app.state.session_factory()
    try:
        names = set(
            session.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
            ).scalars()
        )
    finally:
        session.close()
    assert {"organization", "app_user", "membership", "assessment"} <= names


def test_assessments_are_hidden_from_other_organizations(client: TestClient) -> None:
    first = client.post("/api/v1/organizations", json={"name": "Alpha AG"})
    second = client.post("/api/v1/organizations", json={"name": "Beta AG"})
    assert first.status_code == 201
    assert second.status_code == 201
    created = client.post(
        f"/api/v1/organizations/{first.json()['id']}/assessments",
        json={"display_name": "  Warehouse roof  "},
    )
    assert created.status_code == 201
    assert created.json()["display_name"] == "Warehouse roof"
    assert created.json()["status"] == "draft"
    hidden = client.get(
        f"/api/v1/organizations/{second.json()['id']}/assessments/{created.json()['id']}"
    )
    assert hidden.status_code == 404
    assert hidden.json()["code"] == "assessment_not_found"


def test_assessment_pages_do_not_cross_organizations(client: TestClient) -> None:
    organization = client.post("/api/v1/organizations", json={"name": "Paged AG"}).json()
    other = client.post("/api/v1/organizations", json={"name": "Other AG"}).json()
    created: list[str] = []
    for index in range(3):
        response = client.post(
            f"/api/v1/organizations/{organization['id']}/assessments",
            json={"display_name": f"Study {index}"},
        )
        assert response.status_code == 201
        created.append(response.json()["id"])
    elsewhere = client.post(
        f"/api/v1/organizations/{other['id']}/assessments",
        json={"display_name": "Elsewhere"},
    )
    assert elsewhere.status_code == 201

    first_page = client.get(
        f"/api/v1/organizations/{organization['id']}/assessments",
        params={"limit": 2},
    )
    assert first_page.status_code == 200
    page = first_page.json()
    assert len(page["items"]) == 2
    assert page["next_cursor"]
    second_page = client.get(
        f"/api/v1/organizations/{organization['id']}/assessments",
        params={"limit": 2, "cursor": page["next_cursor"]},
    )
    assert second_page.status_code == 200
    collected = [item["id"] for item in page["items"]]
    collected.extend(item["id"] for item in second_page.json()["items"])
    assert second_page.json()["next_cursor"] is None
    assert sorted(collected) == sorted(created)
    assert elsewhere.json()["id"] not in collected


def test_invalid_cursor_and_blank_name_are_rejected(client: TestClient) -> None:
    organization = client.post("/api/v1/organizations", json={"name": "Named AG"})
    assert organization.status_code == 201
    blank = client.post("/api/v1/organizations", json={"name": "   "})
    assert blank.status_code == 422
    assert blank.json()["code"] == "validation_error"
    cursor = client.get(
        f"/api/v1/organizations/{organization.json()['id']}/assessments",
        params={"cursor": "not-a-cursor"},
    )
    assert cursor.status_code == 400
    assert cursor.json()["code"] == "invalid_cursor"
