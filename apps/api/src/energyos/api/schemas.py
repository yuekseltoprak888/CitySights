from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from energyos.domain.health import HealthReport
from energyos.domain.tenancy import Assessment, Organization


class CreateOrganizationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, organization: Organization) -> "OrganizationResponse":
        return cls(
            id=organization.id,
            name=organization.name,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
        )


class CreateAssessmentRequest(BaseModel):
    display_name: str = Field(min_length=1, max_length=200)


class AssessmentResponse(BaseModel):
    id: UUID
    organization_id: UUID
    display_name: str
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, assessment: Assessment) -> "AssessmentResponse":
        return cls(
            id=assessment.id,
            organization_id=assessment.organization_id,
            display_name=assessment.display_name,
            status=assessment.status.value,
            created_at=assessment.created_at,
            updated_at=assessment.updated_at,
        )


class AssessmentListResponse(BaseModel):
    items: list[AssessmentResponse]
    next_cursor: str | None


class HealthResponse(BaseModel):
    status: str
    environment: str
    country: str
    database: str
    postgis: str

    @classmethod
    def from_domain(cls, report: HealthReport) -> "HealthResponse":
        return cls(
            status=report.status,
            environment=report.environment,
            country=report.country,
            database=report.database,
            postgis=report.postgis,
        )
