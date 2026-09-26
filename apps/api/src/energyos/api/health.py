from fastapi import APIRouter, Depends, Response

from energyos.api.deps import get_health_service
from energyos.api.schemas import HealthResponse
from energyos.services.health import HealthService

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def read_health(
    response: Response,
    service: HealthService = Depends(get_health_service),
) -> HealthResponse:
    report = service.check()
    if report.status != "ok":
        response.status_code = 503
    return HealthResponse.from_domain(report)
