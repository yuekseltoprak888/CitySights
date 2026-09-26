from uuid import UUID, uuid4

from energyos.domain.clock import utcnow
from energyos.domain.errors import AssessmentNotFound, DomainValidationError, OrganizationNotFound
from energyos.domain.names import require_name
from energyos.domain.ports import AssessmentRepository, OrganizationRepository
from energyos.domain.tenancy import Assessment, AssessmentPage, AssessmentStatus

MAX_PAGE_SIZE = 100


class AssessmentService:
    def __init__(
        self,
        organizations: OrganizationRepository,
        assessments: AssessmentRepository,
    ) -> None:
        self._organizations = organizations
        self._assessments = assessments

    def create(self, organization_id: UUID, display_name: str) -> Assessment:
        self._require_organization(organization_id)
        now = utcnow()
        assessment = Assessment(
            id=uuid4(),
            organization_id=organization_id,
            display_name=require_name(display_name, field="Display name"),
            status=AssessmentStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )
        return self._assessments.add(assessment)

    def get(self, organization_id: UUID, assessment_id: UUID) -> Assessment:
        self._require_organization(organization_id)
        found = self._assessments.get(organization_id, assessment_id)
        if found is None:
            raise AssessmentNotFound
        return found

    def list_for_organization(
        self,
        organization_id: UUID,
        *,
        limit: int,
        cursor: str | None,
    ) -> AssessmentPage:
        if limit < 1 or limit > MAX_PAGE_SIZE:
            raise DomainValidationError(f"Limit must be between 1 and {MAX_PAGE_SIZE}")
        self._require_organization(organization_id)
        return self._assessments.list_for_organization(
            organization_id,
            limit=limit,
            cursor=cursor,
        )

    def _require_organization(self, organization_id: UUID) -> None:
        if self._organizations.get(organization_id) is None:
            raise OrganizationNotFound
