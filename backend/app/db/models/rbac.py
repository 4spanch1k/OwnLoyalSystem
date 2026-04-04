from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKeyConstraint, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, TimestampMixin


class User(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_users_tenant_id_tenants"),
        UniqueConstraint("tenant_id", "id", name="uq_users_tenant_id_id"),
        UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),
    )


class UserMembership(Base, IdMixin, TenantScopedMixin, TimestampMixin):
    __tablename__ = "user_memberships"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    branch_id: Mapped[str | None] = mapped_column(String(36))
    role_code: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_user_memberships_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_user_memberships_tenant_user_users",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "branch_id"],
            ["branches.tenant_id", "branches.id"],
            name="fk_user_memberships_tenant_branch_branches",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_user_memberships_tenant_id_id"),
        Index("ix_user_memberships_tenant_id_user_id", "tenant_id", "user_id"),
    )
