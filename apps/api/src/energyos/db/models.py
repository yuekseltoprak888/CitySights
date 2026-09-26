from datetime import datetime
from enum import Enum as PyEnum
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from energyos.db.base import Base
from energyos.domain.tenancy import AssessmentStatus, MembershipRole


def _enum_values(enum_type: type[PyEnum]) -> list[str]:
    return [str(member.value) for member in enum_type]


class OrganizationModel(Base):
    __tablename__ = "organization"
    __table_args__ = (
        CheckConstraint("char_length(btrim(name)) > 0", name="ck_organization_name_not_blank"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AppUserModel(Base):
    __tablename__ = "app_user"
    __table_args__ = (
        UniqueConstraint("email", name="uq_app_user_email"),
        CheckConstraint("char_length(btrim(email)) > 3", name="ck_app_user_email_not_blank"),
        CheckConstraint(
            "char_length(btrim(display_name)) > 0",
            name="ck_app_user_display_name_not_blank",
        ),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(320))
    display_name: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class MembershipModel(Base):
    __tablename__ = "membership"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "organization_id",
            name="uq_membership_user_id_organization_id",
        ),
        Index("ix_membership_organization_id", "organization_id"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("app_user.id", name="fk_membership_user_id_app_user", ondelete="CASCADE"),
    )
    organization_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "organization.id",
            name="fk_membership_organization_id_organization",
            ondelete="CASCADE",
        ),
    )
    role: Mapped[MembershipRole] = mapped_column(
        Enum(
            MembershipRole,
            name="membership_role",
            values_callable=_enum_values,
            native_enum=True,
        ),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AssessmentModel(Base):
    __tablename__ = "assessment"
    __table_args__ = (
        CheckConstraint(
            "char_length(btrim(display_name)) > 0",
            name="ck_assessment_display_name_not_blank",
        ),
        Index(
            "ix_assessment_organization_id_created_at_id",
            "organization_id",
            "created_at",
            "id",
        ),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    organization_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "organization.id",
            name="fk_assessment_organization_id_organization",
            ondelete="CASCADE",
        ),
    )
    display_name: Mapped[str] = mapped_column(String(200))
    status: Mapped[AssessmentStatus] = mapped_column(
        Enum(
            AssessmentStatus,
            name="assessment_status",
            values_callable=_enum_values,
            native_enum=True,
        ),
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
