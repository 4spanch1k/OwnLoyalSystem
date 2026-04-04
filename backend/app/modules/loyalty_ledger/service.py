from decimal import Decimal

from sqlalchemy.orm import Session

from backend.app.modules.loyalty_ledger.schemas import (
    LedgerFeedResponse,
    RedemptionQuoteRequest,
    RedemptionQuoteResponse,
)
from backend.app.services.loyalty.readers import get_patient_ledger_feed


class LoyaltyLedgerService:
    """Ledger read service for Slice 1."""

    def get_patient_ledger(self, db: Session, tenant_id: str, patient_id: str) -> LedgerFeedResponse:
        return get_patient_ledger_feed(db=db, tenant_id=tenant_id, patient_id=patient_id)

    def quote_redemption(self, payload: RedemptionQuoteRequest) -> RedemptionQuoteResponse:
        gross_amount = Decimal(payload.gross_amount)
        redemption_cap_amount = (gross_amount * Decimal("0.20")).quantize(Decimal("0.01"))
        available_balance = Decimal("124000.00")
        return RedemptionQuoteResponse(
            available_balance=available_balance,
            max_redeemable_amount=min(available_balance, redemption_cap_amount),
            eligible_invoice_amount=payload.gross_amount,
            redemption_cap_amount=redemption_cap_amount,
            policy_version_id="policy-v1",
            warnings=[],
        )
