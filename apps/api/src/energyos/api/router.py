from fastapi import APIRouter

from energyos.api.assessments import router as assessments_router
from energyos.api.health import router as health_router
from energyos.api.organizations import router as organizations_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(organizations_router)
api_router.include_router(assessments_router)
