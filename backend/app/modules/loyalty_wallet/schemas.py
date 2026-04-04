from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


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
