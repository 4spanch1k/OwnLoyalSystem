from datetime import datetime

from pydantic import BaseModel, Field


class LoyaltyPolicyServiceRuleInput(BaseModel):
    match_type: str
    match_value: str
    accrual_allowed: bool = True
    redemption_allowed: bool = True
    accrual_rate_bps_override: int | None = None
    redemption_cap_bps_override: int | None = None
    priority: int = 100


class LoyaltyProgramSnapshotResponse(BaseModel):
    program_id: str
    program_name: str
    policy_version_id: str
    accrual_rate_bps: int
    promo_accrual_rate_bps: int | None
    redemption_cap_bps: int
    expiry_days: int
    currency_code: str
    updated_at: datetime


class LoyaltyProgramUpdateRequest(BaseModel):
    program_name: str = Field(min_length=1, max_length=255)
    accrual_rate_bps: int = Field(ge=0, le=10_000)
    promo_accrual_rate_bps: int | None = Field(default=None, ge=0, le=10_000)
    redemption_cap_bps: int = Field(ge=0, le=10_000)
    expiry_days: int = Field(ge=1, le=3650)
    base_currency_code: str = Field(min_length=3, max_length=3)
    service_rules: list[LoyaltyPolicyServiceRuleInput] = Field(default_factory=list)


class LoyaltyProgramUpdateResponse(BaseModel):
    program_id: str
    policy_version_id: str
    version_number: int
    effective_from: datetime | None
