from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.shared.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin
from backend.app.shared.domain.enums import LedgerDirection, LoyaltyOperationType, RedemptionStatus


class LoyaltyLedgerEntry(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "loyalty_ledger_entries"

    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    wallet_id: Mapped[str] = mapped_column(String(36), ForeignKey("patient_wallets.id"), nullable=False, index=True)
    branch_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("branches.id"))
    visit_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("visits.id"))
    payment_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("payments.id"))
    redemption_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("loyalty_redemptions.id"))
    policy_version_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("loyalty_policy_versions.id"))
    operation_type: Mapped[LoyaltyOperationType] = mapped_column(Enum(LoyaltyOperationType), nullable=False)
    direction: Mapped[LedgerDirection] = mapped_column(Enum(LedgerDirection), nullable=False)
    amount_delta: Mapped[int] = mapped_column(BigInteger, nullable=False)
    balance_after: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    source_event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_event_id: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_code: Mapped[str | None] = mapped_column(String(64))
    reason_text: Mapped[str | None] = mapped_column(String(255))
    effective_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    created_by_type: Mapped[str] = mapped_column(String(32), nullable=False)


class LoyaltyRedemption(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "loyalty_redemptions"

    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    wallet_id: Mapped[str] = mapped_column(String(36), ForeignKey("patient_wallets.id"), nullable=False)
    visit_id: Mapped[str] = mapped_column(String(36), ForeignKey("visits.id"), nullable=False)
    payment_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("payments.id"))
    requested_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    approved_amount: Mapped[int | None] = mapped_column(BigInteger)
    applied_amount: Mapped[int | None] = mapped_column(BigInteger)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    redemption_status: Mapped[RedemptionStatus] = mapped_column(Enum(RedemptionStatus), nullable=False)
    requested_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    approved_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    applied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LoyaltyManualAdjustment(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_manual_adjustments"

    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    wallet_id: Mapped[str] = mapped_column(String(36), ForeignKey("patient_wallets.id"), nullable=False)
    adjustment_type: Mapped[LedgerDirection] = mapped_column(Enum(LedgerDirection), nullable=False)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_text: Mapped[str] = mapped_column(String(255), nullable=False)
    requested_by_user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    approved_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    applied_ledger_entry_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("loyalty_ledger_entries.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    applied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
