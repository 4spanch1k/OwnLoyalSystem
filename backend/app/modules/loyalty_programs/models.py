from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.shared.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin
from backend.app.shared.domain.enums import ProgramStatus


class LoyaltyProgram(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "loyalty_programs"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    program_status: Mapped[ProgramStatus] = mapped_column(Enum(ProgramStatus), nullable=False)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LoyaltyPolicyVersion(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_policy_versions"

    loyalty_program_id: Mapped[str] = mapped_column(String(36), ForeignKey("loyalty_programs.id"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    accrual_rate_bps: Mapped[int] = mapped_column(Integer, nullable=False)
    promo_accrual_rate_bps: Mapped[int | None] = mapped_column(Integer)
    redemption_cap_bps: Mapped[int] = mapped_column(Integer, nullable=False)
    expiry_days: Mapped[int] = mapped_column(Integer, nullable=False)
    base_currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    allow_same_day_redemption: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    policy_status: Mapped[ProgramStatus] = mapped_column(Enum(ProgramStatus), nullable=False)
    effective_from: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class LoyaltyPolicyServiceRule(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "loyalty_policy_service_rules"

    loyalty_policy_version_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("loyalty_policy_versions.id"),
        nullable=False,
        index=True,
    )
    match_type: Mapped[str] = mapped_column(String(32), nullable=False)
    match_value: Mapped[str] = mapped_column(String(64), nullable=False)
    accrual_allowed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    redemption_allowed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    accrual_rate_bps_override: Mapped[int | None] = mapped_column(Integer)
    redemption_cap_bps_override: Mapped[int | None] = mapped_column(Integer)
    priority: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
