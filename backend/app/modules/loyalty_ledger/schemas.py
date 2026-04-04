from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class LedgerEntryResponse(BaseModel):
    ledger_entry_id: str
    entry_type: str
    direction: str | None
    amount: Decimal
    balance_after: Decimal
    payment_id: str | None
    reason_code: str | None
    currency_code: str
    created_at: datetime
    status: str


class LedgerFeedResponse(BaseModel):
    items: list[LedgerEntryResponse]
    next_cursor: str | None = None


class RedemptionQuoteRequest(BaseModel):
    patient_id: str
    visit_id: str
    payment_line_ids: list[str] = Field(default_factory=list)
    gross_amount: int = Field(ge=0)
    currency_code: str = Field(min_length=3, max_length=3)


class RedemptionQuoteResponse(BaseModel):
    available_balance: Decimal
    max_redeemable_amount: Decimal
    eligible_invoice_amount: Decimal
    redemption_cap_amount: Decimal
    policy_version_id: str
    warnings: list[str] = Field(default_factory=list)


class RedemptionCreateRequest(BaseModel):
    patient_id: str
    visit_id: str
    payment_id: str
    requested_amount: int = Field(ge=0)
    currency_code: str = Field(min_length=3, max_length=3)
    reason_text: str | None = None


class RedemptionCreateResponse(BaseModel):
    redemption_id: str
    ledger_entry_id: str
    applied_amount: int
    balance_after: int
