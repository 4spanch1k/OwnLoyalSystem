from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.shared.db.base import Base, IdMixin, TenantScopedMixin


class PatientWallet(Base, IdMixin, TenantScopedMixin):
    __tablename__ = "patient_wallets"

    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False, unique=True)
    program_id: Mapped[str] = mapped_column(String(36), ForeignKey("loyalty_programs.id"), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    available_balance: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    pending_balance: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    expired_balance_total: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    redeemed_balance_total: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    last_ledger_entry_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("loyalty_ledger_entries.id"))
