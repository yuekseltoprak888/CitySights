from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MembershipRole(StrEnum):
    OWNER = "owner"
    MEMBER = "member"


class AssessmentStatus(StrEnum):
    DRAFT = "draft"


class Organization(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime


class AppUser(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    email: str
    display_name: str
    created_at: datetime
    updated_at: datetime


class Membership(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    user_id: UUID
    organization_id: UUID
    role: MembershipRole
    created_at: datetime


class Assessment(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    organization_id: UUID
    display_name: str
    status: AssessmentStatus
    created_at: datetime
    updated_at: datetime


class AssessmentPage(BaseModel):
    model_config = ConfigDict(frozen=True)

    items: tuple[Assessment, ...]
    next_cursor: str | None
