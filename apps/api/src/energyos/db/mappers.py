from energyos.db.models import AssessmentModel, OrganizationModel
from energyos.domain.tenancy import Assessment, Organization


def to_organization(row: OrganizationModel) -> Organization:
    return Organization(
        id=row.id,
        name=row.name,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def to_assessment(row: AssessmentModel) -> Assessment:
    return Assessment(
        id=row.id,
        organization_id=row.organization_id,
        display_name=row.display_name,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
