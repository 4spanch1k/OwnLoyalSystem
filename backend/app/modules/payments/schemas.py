from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ConfirmPaymentResponse(BaseModel):
    payment_id: str
    status: str
    confirmed_at: datetime | None
    accrual_amount: Decimal
    wallet_balance: Decimal
    currency_code: str
    ledger_entry_id: str | None
    idempotency_key: str
    already_processed: bool
