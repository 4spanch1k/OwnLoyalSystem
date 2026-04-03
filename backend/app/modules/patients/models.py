from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.shared.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin
from backend.app.shared.domain.enums import ConsentChannel, ConsentStatus, ConsentType


class Patient(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "patients"

    primary_branch_id: Mapped[str] = mapped_column(String(36), ForeignKey("branches.id"), nullable=False)
    external_patient_code: Mapped[str | None] = mapped_column(String(64))
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(120))
    birth_date: Mapped[date | None] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    registered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    preferred_language: Mapped[str | None] = mapped_column(String(8))
    household_id: Mapped[str | None] = mapped_column(String(36))
    source_channel: Mapped[str | None] = mapped_column(String(64))


class PatientConsent(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "patient_consents"

    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    channel: Mapped[ConsentChannel] = mapped_column(Enum(ConsentChannel), nullable=False)
    consent_type: Mapped[ConsentType] = mapped_column(Enum(ConsentType), nullable=False)
    status: Mapped[ConsentStatus] = mapped_column(Enum(ConsentStatus), nullable=False)
    granted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
