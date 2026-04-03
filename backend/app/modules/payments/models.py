from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.shared.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin
from backend.app.shared.domain.enums import PaymentStatus


class Payment(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "payments"

    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey("branches.id"), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    visit_id: Mapped[str] = mapped_column(String(36), ForeignKey("visits.id"), nullable=False, index=True)
    payment_number: Mapped[str] = mapped_column(String(64), nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), nullable=False)
    gross_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    patient_paid_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(32), nullable=False)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    refunded_amount: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    refunded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class PaymentLine(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "payment_lines"

    payment_id: Mapped[str] = mapped_column(String(36), ForeignKey("payments.id"), nullable=False, index=True)
    visit_id: Mapped[str] = mapped_column(String(36), ForeignKey("visits.id"), nullable=False, index=True)
    service_code: Mapped[str] = mapped_column(String(64), nullable=False)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    service_category: Mapped[str] = mapped_column(String(64), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    gross_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    discount_amount: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    patient_paid_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_discounted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_financed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_insurance_paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
