from uuid import UUID

from fastapi import APIRouter, Depends

from energyos.api.deps import get_organization_service
from energyos.api.schemas import CreateOrganizationRequest, OrganizationResponse
from energyos.services.organizations import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", status_code=201, response_model=OrganizationResponse)
def create_organization(
    body: CreateOrganizationRequest,
    service: OrganizationService = Depends(get_organization_service),
) -> OrganizationResponse:
    organization = service.create(body.name)
    return OrganizationResponse.from_domain(organization)


@router.get("/{organization_id}", response_model=OrganizationResponse)
def read_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
) -> OrganizationResponse:
    return OrganizationResponse.from_domain(service.get(organization_id))
