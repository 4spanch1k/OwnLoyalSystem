from datetime import datetime, timedelta, timezone

from backend.app.modules.loyalty_ledger.schemas import (
    LedgerEntryResponse,
    LedgerFeedResponse,
    RedemptionQuoteRequest,
    RedemptionQuoteResponse,
)


class LoyaltyLedgerService:
    """Contract-first ledger service for API scaffolding."""

    def get_patient_ledger(self, patient_id: str) -> LedgerFeedResponse:
        now = datetime.now(timezone.utc)
        items = [
            LedgerEntryResponse(
                ledger_entry_id="ledger-accrual-1",
                operation_type="accrual",
                amount_delta=2000,
                balance_after=124000,
                effective_at=now - timedelta(days=10),
                expires_at=now + timedelta(days=170),
                reason_text="Начисление после подтверждённой оплаты.",
                related_visit_id="visit-1",
                related_payment_id="payment-1",
            )
        ]
        return LedgerFeedResponse(items=items)

    def quote_redemption(self, payload: RedemptionQuoteRequest) -> RedemptionQuoteResponse:
        redemption_cap_amount = payload.gross_amount * 20 // 100
        available_balance = 124000
        return RedemptionQuoteResponse(
            available_balance=available_balance,
            max_redeemable_amount=min(available_balance, redemption_cap_amount),
            eligible_invoice_amount=payload.gross_amount,
            redemption_cap_amount=redemption_cap_amount,
            policy_version_id="policy-v1",
            warnings=[],
        )
