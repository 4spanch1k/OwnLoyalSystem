from sqlalchemy import Boolean, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin


class Tenant(Base, IdMixin, TimestampMixin):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    default_currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)

    __table_args__ = (
        UniqueConstraint("slug", name="uq_tenants_slug"),
    )


class Branch(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "branches"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    address_line: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(32))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_branches_tenant_id_tenants"),
        UniqueConstraint("tenant_id", "id", name="uq_branches_tenant_id_id"),
        UniqueConstraint("tenant_id", "code", name="uq_branches_tenant_code"),
        Index("ix_branches_tenant_id_is_active", "tenant_id", "is_active"),
    )
