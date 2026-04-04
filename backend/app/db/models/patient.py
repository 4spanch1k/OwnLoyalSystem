from sqlalchemy import ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin


class Patient(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "patients"

    branch_id: Mapped[str] = mapped_column(String(36), nullable=False)
    external_patient_code: Mapped[str | None] = mapped_column(String(64))
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_patients_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_patients_tenant_branch_branches",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_patients_tenant_id_id"),
        Index("ix_patients_tenant_id_phone", "tenant_id", "phone"),
    )
