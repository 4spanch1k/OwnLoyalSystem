from datetime import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin


class Visit(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "visits"

    branch_id: Mapped[str] = mapped_column(String(36), nullable=False)
    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    doctor_user_id: Mapped[str | None] = mapped_column(String(36))
    appointment_id: Mapped[str | None] = mapped_column(String(36))
    visit_number: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_visits_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_visits_tenant_branch_branches",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_visits_tenant_patient_patients",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "doctor_user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_visits_tenant_doctor_users",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_visits_tenant_id_id"),
        Index("ix_visits_tenant_id_patient_id", "tenant_id", "patient_id"),
    )
