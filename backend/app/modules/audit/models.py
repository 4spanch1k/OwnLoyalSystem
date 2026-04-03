from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.shared.db.base import Base, IdMixin, TenantScopedMixin


class AuditLog(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "audit_logs"

    branch_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("branches.id"))
    actor_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    actor_role_code: Mapped[str | None] = mapped_column(String(64))
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(36), nullable=False)
    action_code: Mapped[str] = mapped_column(String(64), nullable=False)
    before_json: Mapped[str | None] = mapped_column(Text)
    after_json: Mapped[str | None] = mapped_column(Text)
    reason_text: Mapped[str | None] = mapped_column(Text)
    request_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
