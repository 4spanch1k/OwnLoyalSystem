from decimal import Decimal
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, ForeignKeyConstraint, Index, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin, ZERO_MONEY, money_column, utc_now


class LoyaltyProgram(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "loyalty_programs"

    branch_id: Mapped[str | None] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    active_policy_version_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("loyalty_policy_versions.id", use_alter=True, name="fk_loyalty_programs_active_policy_version_id"),
    )

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_programs_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_loyalty_programs_tenant_branch_branches",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_loyalty_programs_tenant_id_id"),
        Index("ix_loyalty_programs_tenant_id_status", "tenant_id", "status"),
    )


class LoyaltyPolicyVersion(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_policy_versions"

    program_id: Mapped[str] = mapped_column(String(36), nullable=False)
    version: Mapped[int] = mapped_column(nullable=False)
    accrual_rate_bps: Mapped[int] = mapped_column(nullable=False)
    redemption_cap_bps: Mapped[int] = mapped_column(nullable=False)
    bonus_ttl_days: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_policy_versions_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "program_id"],
            ["loyalty_programs.tenant_id", "loyalty_programs.id"],
            name="fk_loyalty_policy_versions_tenant_program_loyalty_programs",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_loyalty_policy_versions_tenant_id_id"),
        UniqueConstraint("tenant_id", "program_id", "version", name="uq_loyalty_policy_versions_program_version"),
        CheckConstraint("accrual_rate_bps >= 0", name="loyalty_policy_versions_accrual_rate_non_negative"),
        CheckConstraint("redemption_cap_bps >= 0", name="loyalty_policy_versions_redemption_cap_non_negative"),
        CheckConstraint("bonus_ttl_days > 0", name="loyalty_policy_versions_bonus_ttl_positive"),
    )


class LoyaltyPolicyServiceRule(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_policy_service_rules"

    policy_version_id: Mapped[str] = mapped_column(String(36), nullable=False)
    service_category: Mapped[str] = mapped_column(String(64), nullable=False)
    accrual_allowed: Mapped[bool] = mapped_column(default=True, nullable=False)
    redemption_allowed: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_policy_service_rules_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "policy_version_id"],
            ["loyalty_policy_versions.tenant_id", "loyalty_policy_versions.id"],
            name="fk_loyalty_policy_service_rules_tenant_policy_loyalty_policy_versions",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_loyalty_policy_service_rules_tenant_id_id"),
        UniqueConstraint(
            "tenant_id",
            "policy_version_id",
            "service_category",
            name="uq_loyalty_policy_service_rules_policy_category",
        ),
    )


class PatientWallet(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "patient_wallets"

    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    available_balance: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    lifetime_accrued: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    lifetime_redeemed: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    lifetime_expired: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_patient_wallets_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_patient_wallets_tenant_patient_patients",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_patient_wallets_tenant_id_id"),
        UniqueConstraint("tenant_id", "patient_id", name="uq_patient_wallets_tenant_patient"),
        CheckConstraint("available_balance >= 0", name="patient_wallets_available_balance_non_negative"),
        CheckConstraint("lifetime_accrued >= 0", name="patient_wallets_lifetime_accrued_non_negative"),
        CheckConstraint("lifetime_redeemed >= 0", name="patient_wallets_lifetime_redeemed_non_negative"),
        CheckConstraint("lifetime_expired >= 0", name="patient_wallets_lifetime_expired_non_negative"),
        Index("ix_patient_wallets_tenant_id_patient_id", "tenant_id", "patient_id"),
    )


class LoyaltyLedgerEntry(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_ledger_entries"

    patient_id: Mapped[str] = mapped_column(String(36), nullable=False)
    wallet_id: Mapped[str] = mapped_column(String(36), nullable=False)
    payment_id: Mapped[str | None] = mapped_column(String(36))
    payment_line_id: Mapped[str | None] = mapped_column(String(36))
    entry_type: Mapped[str] = mapped_column(String(32), nullable=False)
    amount: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    balance_after: Mapped[Decimal] = money_column(default=ZERO_MONEY)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="posted", nullable=False)
    policy_version_id: Mapped[str | None] = mapped_column(String(36))
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    reason_code: Mapped[str | None] = mapped_column(String(64))
    metadata_json: Mapped[dict[str, object] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_loyalty_ledger_entries_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "patient_id"],
            ["patients.tenant_id", "patients.id"],
            name="fk_loyalty_ledger_entries_tenant_patient_patients",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "wallet_id"],
            ["patient_wallets.tenant_id", "patient_wallets.id"],
            name="fk_loyalty_ledger_entries_tenant_wallet_patient_wallets",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "payment_id"],
            ["payments.tenant_id", "payments.id"],
            name="fk_loyalty_ledger_entries_tenant_payment_payments",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "payment_line_id"],
            ["payment_lines.tenant_id", "payment_lines.id"],
            name="fk_loyalty_ledger_entries_tenant_payment_line_payment_lines",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "policy_version_id"],
            ["loyalty_policy_versions.tenant_id", "loyalty_policy_versions.id"],
            name="fk_loyalty_ledger_entries_tenant_policy_loyalty_policy_versions",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_loyalty_ledger_entries_tenant_id_id"),
        UniqueConstraint("tenant_id", "idempotency_key", name="uq_loyalty_ledger_entries_tenant_idempotency_key"),
        CheckConstraint("amount >= 0", name="loyalty_ledger_entries_amount_non_negative"),
        CheckConstraint("balance_after >= 0", name="loyalty_ledger_entries_balance_after_non_negative"),
        Index("ix_loyalty_ledger_entries_tenant_patient_created_at", "tenant_id", "patient_id", "created_at"),
        Index("ix_loyalty_ledger_entries_payment_id", "payment_id"),
    )
