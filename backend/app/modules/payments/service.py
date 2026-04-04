from sqlalchemy.orm import Session

from backend.app.modules.payments.schemas import ConfirmPaymentResponse
from backend.app.services.loyalty.accrual import confirm_payment as confirm_payment_accrual


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
