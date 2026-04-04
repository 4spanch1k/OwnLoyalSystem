from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, ZERO_MONEY, money_column, utc_now


class LoyaltyRedemption(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_redemptions"

    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    payment_id: Mapped[str] = mapped_column(String(36), nullable=False)
    wallet_id: Mapped[str] = mapped_column(String(36), nullable=False)
    policy_version_id: Mapped[str] = mapped_column(String(36), nullable=False)
    requested_amount: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    approved_amount: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_redemptions_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_loyalty_redemptions_tenant_patient_patients",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "payment_id"],
            ["payments.tenant_id", "payments.id"],
            name="fk_loyalty_redemptions_tenant_payment_payments",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "wallet_id"],
            ["patient_wallets.tenant_id", "patient_wallets.id"],
            name="fk_loyalty_redemptions_tenant_wallet_patient_wallets",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "policy_version_id"],
            ["loyalty_policy_versions.tenant_id", "loyalty_policy_versions.id"],
            name="fk_loyalty_redemptions_tenant_policy_loyalty_policy_versions",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_loyalty_redemptions_tenant_id_id"),
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_loyalty_redemptions_tenant_idempotency_key"),
        CheckConstraint("requested_amount >= 0", name="loyalty_redemptions_requested_amount_non_negative"),
        CheckConstraint("approved_amount >= 0", name="loyalty_redemptions_approved_amount_non_negative"),
        Index("ix_loyalty_redemptions_tenant_patient_created_at", "tenant_id", "patient_id", "created_at"),
        Index("ix_loyalty_redemptions_payment_id", "payment_id"),
    )
