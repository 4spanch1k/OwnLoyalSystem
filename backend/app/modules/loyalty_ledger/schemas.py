from datetime import datetime

from pydantic import BaseModel, Field


class LedgerEntryResponse(BaseModel):
    ledger_entry_id: str
    operation_type: str
    amount_delta: int
    balance_after: int
    effective_at: datetime
    expires_at: datetime | None
    reason_text: str | None
    related_visit_id: str | None
    related_payment_id: str | None


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
    available_balance: int
    max_redeemable_amount: int
    eligible_invoice_amount: int
    redemption_cap_amount: int
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


class ManualAdjustmentCreateRequest(BaseModel):
    patient_id: str
    adjustment_type: str
    amount: int = Field(ge=0)
    currency_code: str = Field(min_length=3, max_length=3)
    reason_code: str
    reason_text: str


class ManualAdjustmentCreateResponse(BaseModel):
    adjustment_id: str
    ledger_entry_id: str
    balance_after: int
