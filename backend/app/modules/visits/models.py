from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.shared.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin
from backend.app.shared.domain.enums import VisitStatus


class Visit(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "visits"

    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey("branches.id"), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    doctor_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    appointment_id: Mapped[str | None] = mapped_column(String(36))
    visit_number: Mapped[str | None] = mapped_column(String(64))
    visit_status: Mapped[VisitStatus] = mapped_column(Enum(VisitStatus), nullable=False)
    scheduled_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
