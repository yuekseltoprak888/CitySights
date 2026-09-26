from uuid import UUID

from sqlalchemy import select, tuple_
from sqlalchemy.orm import Session

from energyos.db.mappers import to_assessment, to_organization
from energyos.db.models import AssessmentModel, OrganizationModel
from energyos.domain.pagination import decode_cursor, encode_cursor
from energyos.domain.tenancy import Assessment, AssessmentPage, Organization


class SqlAlchemyOrganizationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, organization: Organization) -> Organization:
        row = OrganizationModel(
            id=organization.id,
            name=organization.name,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
        )
        self._session.add(row)
        self._session.flush()
        return to_organization(row)

    def get(self, organization_id: UUID) -> Organization | None:
        row = self._session.get(OrganizationModel, organization_id)
        if row is None:
            return None
        return to_organization(row)


class SqlAlchemyAssessmentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, assessment: Assessment) -> Assessment:
        row = AssessmentModel(
            id=assessment.id,
            organization_id=assessment.organization_id,
            display_name=assessment.display_name,
            status=assessment.status,
            created_at=assessment.created_at,
            updated_at=assessment.updated_at,
        )
        self._session.add(row)
        self._session.flush()
        return to_assessment(row)

    def get(self, organization_id: UUID, assessment_id: UUID) -> Assessment | None:
        statement = select(AssessmentModel).where(
            AssessmentModel.organization_id == organization_id,
            AssessmentModel.id == assessment_id,
        )
        row = self._session.scalar(statement)
        if row is None:
            return None
        return to_assessment(row)

    def list_for_organization(
        self,
        organization_id: UUID,
        *,
        limit: int,
        cursor: str | None,
    ) -> AssessmentPage:
        statement = (
            select(AssessmentModel)
            .where(AssessmentModel.organization_id == organization_id)
            .order_by(AssessmentModel.created_at.desc(), AssessmentModel.id.desc())
        )
        if cursor is not None:
            created_at, entity_id = decode_cursor(cursor)
            statement = statement.where(
                tuple_(AssessmentModel.created_at, AssessmentModel.id)
                < tuple_(created_at, entity_id)
            )
        rows = list(self._session.scalars(statement.limit(limit + 1)))
        has_more = len(rows) > limit
        visible = rows[:limit]
        next_cursor = None
        if has_more and visible:
            last = visible[-1]
            next_cursor = encode_cursor(last.created_at, last.id)
        return AssessmentPage(
            items=tuple(to_assessment(row) for row in visible),
            next_cursor=next_cursor,
        )
