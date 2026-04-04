from decimal import Decimal
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin, ZERO_MONEY, money_column


class Payment(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "payments"

    branch_id: Mapped[str] = mapped_column(String(36), nullable=False)
    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    visit_id: Mapped[str] = mapped_column(String(36), nullable=False)
    payment_number: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    total_amount: Mapped[Decimal] = money_column()
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    refunded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_payments_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_payments_tenant_branch_branches",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_payments_tenant_patient_patients",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "visit_id"],
            ["visits.tenant_id", "visits.id"],
            name="fk_payments_tenant_visit_visits",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_payments_tenant_id_id"),
        UniqueConstraint("tenant_id", "payment_number", name="uq_payments_tenant_payment_number"),
        CheckConstraint("total_amount >= 0", name="payments_total_amount_non_negative"),
        Index("ix_payments_tenant_id_patient_id", "tenant_id", "patient_id"),
        Index("ix_payments_tenant_id_status", "tenant_id", "status"),
    )


class PaymentLine(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "payment_lines"

    payment_id: Mapped[str] = mapped_column(String(36), nullable=False)
    service_code: Mapped[str] = mapped_column(String(64), nullable=False)
    service_category: Mapped[str] = mapped_column(String(64), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    unit_price: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    line_total: Mapped[Decimal] = money_column(default=ZERO_MONEY)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_payment_lines_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "payment_id"],
            ["payments.tenant_id", "payments.id"],
            name="fk_payment_lines_tenant_payment_payments",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_payment_lines_tenant_id_id"),
        CheckConstraint("quantity > 0", name="payment_lines_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="payment_lines_unit_price_non_negative"),
        CheckConstraint("line_total >= 0", name="payment_lines_line_total_non_negative"),
        Index("ix_payment_lines_payment_id", "payment_id"),
    )
