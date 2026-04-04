from datetime import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Index, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base, IdMixin, TenantScopedMixin, utc_now


class AuditLog(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "audit_logs"

    actor_user_id: Mapped[str | None] = mapped_column(String(36))
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    payload_json: Mapped[dict[str, object] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_audit_logs_tenant_id_tenants"),
        ForeignKeyConstraint(
            ["tenant_id", "actor_user_id"],
            ["users.tenant_id", "users.id"],
            name="fk_audit_logs_tenant_actor_users",
        ),
        UniqueConstraint("tenant_id", "id", name="uq_audit_logs_tenant_id_id"),
        Index("ix_audit_logs_tenant_entity", "tenant_id", "entity_type", "entity_id"),
    )
