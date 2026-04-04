from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, money_column, utc_now


class LoyaltyManualAdjustment(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_manual_adjustments"

    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    wallet_id: Mapped[str] = mapped_column(String(36), nullable=False)
    ledger_entry_id: Mapped[str] = mapped_column(String(36), nullable=False)
    actor_user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    direction: Mapped[str] = mapped_column(String(16), nullable=False)
    amount: Mapped[Decimal] = money_column()
    balance_before: Mapped[Decimal] = money_column()
    balance_after: Mapped[Decimal] = money_column()
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(64), nullable=False)
    comment: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_manual_adjustments_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_loyalty_manual_adjustments_tenant_patient_patients",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "wallet_id"],
            ["patient_wallets.tenant_id", "patient_wallets.id"],
            name="fk_loyalty_manual_adjustments_tenant_wallet_patient_wallets",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "ledger_entry_id"],
            ["loyalty_ledger_entries.tenant_id", "loyalty_ledger_entries.id"],
            name="fk_loyalty_manual_adjustments_tenant_ledger_loyalty_ledger_entries",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "actor_user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_loyalty_manual_adjustments_tenant_actor_users",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_loyalty_manual_adjustments_tenant_id_id"),
        UniqueConstraint("tenant_id", "ledger_entry_id", name="uq_loyalty_manual_adjustments_tenant_ledger_entry"),
        CheckConstraint("amount >= 0", name="loyalty_manual_adjustments_amount_non_negative"),
        CheckConstraint("balance_before >= 0", name="loyalty_manual_adjustments_balance_before_non_negative"),
        CheckConstraint("balance_after >= 0", name="loyalty_manual_adjustments_balance_after_non_negative"),
        CheckConstraint("direction IN ('credit', 'debit')", name="loyalty_manual_adjustments_direction_valid"),
        Index("ix_loyalty_manual_adjustments_tenant_patient_created_at", "tenant_id", "patient_id", "created_at"),
    )
