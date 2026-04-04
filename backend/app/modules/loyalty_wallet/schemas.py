from datetime import datetime
from decimal import Decimal

from typing import Literal

from pydantic import BaseModel, Field


class WalletSummaryResponse(BaseModel):
    patient_id: str
    available_balance: Decimal
    lifetime_accrued: Decimal
    lifetime_redeemed: Decimal
    lifetime_expired: Decimal
    currency_code: str
    updated_at: datetime | None


class BonusRulesResponse(BaseModel):
    program_name: str
    accrual_rate_display: str
    redemption_cap_display: str
    expiry_days: int
    exclusions_summary: list[str]
    faq_items: list[str]


class ManualAdjustmentRequest(BaseModel):
    amount: Decimal = Field(ge=Decimal("0.01"))
    direction: Literal["credit", "debit"]
    reason_code: str = Field(min_length=1, max_length=64)
    comment: str = Field(min_length=1, max_length=500)


class ManualAdjustmentResponse(BaseModel):
    adjustment_id: str
    patient_id: str
    wallet_id: str
    direction: str
    amount: Decimal
    balance_before: Decimal
    wallet_balance_after: Decimal
    reason_code: str
    comment: str
    ledger_entry_id: str
    audit_log_id: str
    applied_at: datetime
