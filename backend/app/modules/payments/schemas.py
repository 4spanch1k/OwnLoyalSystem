from datetime import datetime
from decimal import Decimal

from pydantic import AliasChoices, BaseModel, Field


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


class RedemptionQuoteResponse(BaseModel):
    payment_id: str
    eligible_subtotal: Decimal
    wallet_available: Decimal
    cap_amount: Decimal
    max_redeemable: Decimal
    currency_code: str
    denied_categories: list[str]
    policy_version_id: str


class ApplyRedemptionRequest(BaseModel):
    requested_amount: Decimal = Field(ge=Decimal("0.01"))
    client_request_id: str = Field(
        min_length=1,
        max_length=120,
        validation_alias=AliasChoices("client_request_id", "idempotency_key"),
    )


class ApplyRedemptionResponse(BaseModel):
    redemption_id: str
    approved_amount: Decimal
    wallet_balance_after: Decimal
    ledger_entry_id: str
    status: str
    idempotency_key: str
    already_processed: bool
