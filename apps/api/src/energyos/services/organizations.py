from uuid import UUID, uuid4

from energyos.domain.clock import utcnow
from energyos.domain.errors import OrganizationNotFound
from energyos.domain.names import require_name
from energyos.domain.ports import OrganizationRepository
from energyos.domain.tenancy import Organization


class OrganizationService:
    def __init__(self, organizations: OrganizationRepository) -> None:
        self._organizations = organizations

    def create(self, name: str) -> Organization:
        now = utcnow()
        organization = Organization(
            id=uuid4(),
            name=require_name(name),
            created_at=now,
            updated_at=now,
        )
        return self._organizations.add(organization)

    def get(self, organization_id: UUID) -> Organization:
        found = self._organizations.get(organization_id)
        if found is None:
            raise OrganizationNotFound
        return found
