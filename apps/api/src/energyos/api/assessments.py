from uuid import UUID

from fastapi import APIRouter, Depends, Query

from energyos.api.deps import get_assessment_service
from energyos.api.schemas import (
    AssessmentListResponse,
    AssessmentResponse,
    CreateAssessmentRequest,
)
from energyos.services.assessments import MAX_PAGE_SIZE, AssessmentService

router = APIRouter(
    prefix="/organizations/{organization_id}/assessments",
    tags=["assessments"],
)


@router.post("", status_code=201, response_model=AssessmentResponse)
def create_assessment(
    organization_id: UUID,
    body: CreateAssessmentRequest,
    service: AssessmentService = Depends(get_assessment_service),
) -> AssessmentResponse:
    assessment = service.create(organization_id, body.display_name)
    return AssessmentResponse.from_domain(assessment)


@router.get("", response_model=AssessmentListResponse)
def list_assessments(
    organization_id: UUID,
    limit: int = Query(default=20, ge=1, le=MAX_PAGE_SIZE),
    cursor: str | None = Query(default=None),
    service: AssessmentService = Depends(get_assessment_service),
) -> AssessmentListResponse:
    page = service.list_for_organization(organization_id, limit=limit, cursor=cursor)
    return AssessmentListResponse(
        items=[AssessmentResponse.from_domain(item) for item in page.items],
        next_cursor=page.next_cursor,
    )


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def read_assessment(
    organization_id: UUID,
    assessment_id: UUID,
    service: AssessmentService = Depends(get_assessment_service),
) -> AssessmentResponse:
    assessment = service.get(organization_id, assessment_id)
    return AssessmentResponse.from_domain(assessment)
