from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import DateTime, MetaData, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

MONEY_PRECISION = 18
MONEY_SCALE = 2
ZERO_MONEY = Decimal("0.00")

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def money_column(*, nullable: bool = False, default: Decimal | None = None) -> Mapped[Decimal]:
    return mapped_column(Numeric(MONEY_PRECISION, MONEY_SCALE), nullable=nullable, default=default)


class Base(DeclarativeBase):
    metadata = metadata


class IdMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


class TenantScopedMixin:
    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
