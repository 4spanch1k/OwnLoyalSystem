from sqlalchemy.orm import Session

from backend.app.modules.payments.schemas import (
    ApplyRedemptionRequest,
    ApplyRedemptionResponse,
    ConfirmPaymentResponse,
    RedemptionQuoteResponse,
)
from backend.app.services.loyalty.accrual import confirm_payment as confirm_payment_accrual
from backend.app.services.loyalty.redemption import apply_redemption, quote_redemption


class PaymentService:
    def confirm_payment(
        self,
        db: Session,
        tenant_id: str,
        payment_id: str,
        actor_user_id: str | None = None,
    ) -> ConfirmPaymentResponse:
        result = confirm_payment_accrual(db=db, tenant_id=tenant_id, payment_id=payment_id, actor_user_id=actor_user_id)
        return ConfirmPaymentResponse(
            payment_id=result.payment_id,
            status=result.payment_status,
            confirmed_at=result.confirmed_at,
            accrual_amount=result.accrual_amount,
            wallet_balance=result.wallet_balance,
            currency_code=result.currency_code,
            ledger_entry_id=result.ledger_entry_id,
            idempotency_key=result.idempotency_key,
            already_processed=result.already_processed,
        )

    def quote_redemption(self, db: Session, tenant_id: str, payment_id: str) -> RedemptionQuoteResponse:
        result = quote_redemption(db=db, tenant_id=tenant_id, payment_id=payment_id)
        return RedemptionQuoteResponse(
            payment_id=result.payment_id,
            eligible_subtotal=result.eligible_subtotal,
            wallet_available=result.wallet_available,
            cap_amount=result.cap_amount,
            max_redeemable=result.max_redeemable,
            currency_code=result.currency_code,
            denied_categories=list(result.denied_categories),
            policy_version_id=result.policy_version_id,
        )

    def apply_redemption(
        self,
        db: Session,
        tenant_id: str,
        payment_id: str,
        payload: ApplyRedemptionRequest,
        actor_user_id: str | None = None,
    ) -> ApplyRedemptionResponse:
        result = apply_redemption(
            db=db,
            tenant_id=tenant_id,
            payment_id=payment_id,
            requested_amount=payload.requested_amount,
            client_request_id=payload.client_request_id,
            actor_user_id=actor_user_id,
        )
        return ApplyRedemptionResponse(
            redemption_id=result.redemption_id,
            approved_amount=result.approved_amount,
            wallet_balance_after=result.wallet_balance_after,
            ledger_entry_id=result.ledger_entry_id,
            status=result.status,
            idempotency_key=result.idempotency_key,
            already_processed=result.already_processed,
        )
