from uuid import UUID, uuid4

import pytest

from energyos.domain.errors import AssessmentNotFound, DomainValidationError, OrganizationNotFound
from energyos.domain.tenancy import Assessment, AssessmentPage, Organization
from energyos.services.assessments import AssessmentService
from energyos.services.organizations import OrganizationService


class MemoryOrganizations:
    def __init__(self) -> None:
        self.rows: dict[UUID, Organization] = {}

    def add(self, organization: Organization) -> Organization:
        self.rows[organization.id] = organization
        return organization

    def get(self, organization_id: UUID) -> Organization | None:
        return self.rows.get(organization_id)


class MemoryAssessments:
    def __init__(self) -> None:
        self.rows: list[Assessment] = []
        self.list_calls = 0

    def add(self, assessment: Assessment) -> Assessment:
        self.rows.append(assessment)
        return assessment

    def get(self, organization_id: UUID, assessment_id: UUID) -> Assessment | None:
        for row in self.rows:
            if row.organization_id == organization_id and row.id == assessment_id:
                return row
        return None

    def list_for_organization(
        self,
        organization_id: UUID,
        *,
        limit: int,
        cursor: str | None,
    ) -> AssessmentPage:
        del limit, cursor
        self.list_calls += 1
        items = tuple(row for row in self.rows if row.organization_id == organization_id)
        return AssessmentPage(items=items, next_cursor=None)


def test_assessment_is_scoped_to_its_organization() -> None:
    organizations = MemoryOrganizations()
    assessments = MemoryAssessments()
    organization_service = OrganizationService(organizations)
    service = AssessmentService(organizations, assessments)
    first = organization_service.create("Alpha AG")
    second = organization_service.create("Beta AG")
    created = service.create(first.id, "  Warehouse roof  ")

    assert created.display_name == "Warehouse roof"
    assert service.get(first.id, created.id).id == created.id
    with pytest.raises(AssessmentNotFound):
        service.get(second.id, created.id)


def test_missing_organization_does_not_list_assessments() -> None:
    assessments = MemoryAssessments()
    service = AssessmentService(MemoryOrganizations(), assessments)
    with pytest.raises(OrganizationNotFound):
        service.list_for_organization(uuid4(), limit=20, cursor=None)
    assert assessments.list_calls == 0


def test_page_limit_is_bounded() -> None:
    organizations = MemoryOrganizations()
    organization = OrganizationService(organizations).create("Alpha AG")
    service = AssessmentService(organizations, MemoryAssessments())
    with pytest.raises(DomainValidationError):
        service.list_for_organization(organization.id, limit=0, cursor=None)
