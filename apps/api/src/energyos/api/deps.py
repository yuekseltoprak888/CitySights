from collections.abc import Iterator
from typing import cast

from fastapi import Depends, Request
from sqlalchemy.orm import Session, sessionmaker

from energyos.composition import (
    build_assessment_service,
    build_health_service,
    build_organization_service,
)
from energyos.config import Settings
from energyos.services.assessments import AssessmentService
from energyos.services.health import HealthService
from energyos.services.organizations import OrganizationService


def get_app_settings(request: Request) -> Settings:
    return cast(Settings, request.app.state.settings)


def get_session(request: Request) -> Iterator[Session]:
    factory = cast(sessionmaker[Session], request.app.state.session_factory)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_health_service(
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_app_settings),
) -> HealthService:
    return build_health_service(session, settings)


def get_organization_service(session: Session = Depends(get_session)) -> OrganizationService:
    return build_organization_service(session)


def get_assessment_service(session: Session = Depends(get_session)) -> AssessmentService:
    return build_assessment_service(session)
