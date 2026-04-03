from datetime import datetime

from pydantic import BaseModel


class WalletSummaryResponse(BaseModel):
    patient_id: str
    wallet_id: str
    available_balance: int
    pending_balance: int
    currency_code: str
    next_expiry_at: datetime | None
    next_expiry_amount: int | None
    program_name: str


class BonusRulesResponse(BaseModel):
    program_name: str
    accrual_rate_display: str
    redemption_cap_display: str
    expiry_days: int
    exclusions_summary: list[str]
    faq_items: list[str]
